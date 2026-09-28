from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from src.user.dtos import AdminUpdateSchema, LoginSchema, UserSchema, DeleteAllConfirmation
from src.user.models import UserModel
from src.utils.logger import logger
from src.utils.settings import settings

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def register(body: UserSchema, db: Session):
    """
        1. Username Validation
        2. Email Validation
    """
    logger.info("Register request – username=%s, email=%s", body.username, body.email)
    try:
        is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
        if is_user:
            raise HTTPException(400, detail="Username already exists!")

        is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
        if is_user:
            raise HTTPException(400, detail="Email already exists!") 

        hash_password = get_password_hash(body.password)

        new_user = UserModel(
            name = body.name,
            username = body.username,
            hash_password = hash_password,
            email = body.email
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info("User created – id=%s, username=%s", new_user.id, new_user.username)
        return new_user

    except Exception as exc:
        logger.error("Error during registration for username=%s: %s", body.username, exc, exc_info=True)
        db.rollback()
        raise


def login_user(body: LoginSchema, db: Session):
    logger.info("Login attempt – username=%s", body.username)
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()

    if not is_user:
        logger.warning("Login failed – unknown username: %s", body.username)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong username!")

    if not verify_password(body.password, is_user.hash_password):
        logger.warning("Login failed – bad password for user id=%s", is_user.id)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Password!")

    exp_time = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.EXP_TIME)

    token = jwt.encode({"_id": is_user.id, "exp":exp_time.timestamp()}, settings.SECRET_KEY, settings.ALGORITHM)

    exp_local = exp_time.astimezone()  # convert to the system’s local tz
    logger.info(
        "Login success – user_id=%s, token_expires=%s (local)",
        is_user.id,
        exp_local.isoformat()
    )
    return {
        "token": token
    }


def get_all_users(db: Session):
    logger.debug("Fetching all users from DB")
    users = db.query(UserModel).all()
    logger.info("Retrieved %d users", len(users))
    return users


def delete_all_users(db: Session, body: DeleteAllConfirmation):
    logger.warning("Deleting all users – admin action")
    try:
        if not body.confirm:
            raise HTTPException(status_code=400, detail="Confirmation required")
        
        db.query(UserModel).delete()
        db.commit()
        logger.info("All users removed successfully")

    except Exception as exc:
        logger.error("Failed to delete all users: %s", exc, exc_info=True)
        db.rollback()
        raise


def update_admin(body: AdminUpdateSchema, user_id: int, db: Session):
    logger.info("Admin flag update – user_id=%s, set_is_admin=%s", user_id, body.is_admin)
    try:
        user = db.query(UserModel).get(user_id)
        if not user:
            logger.warning("Admin update failed – user %s not found", user_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

        user.is_admin = body.is_admin
        db.add(user)
        db.commit()
        db.refresh(user)

        logger.info("Admin flag updated – user_id=%s, is_admin=%s", user_id, user.is_admin)
        return user

    except Exception as exc:
        logger.error("Error updating admin flag for user %s: %s", user_id, exc, exc_info=True)
        db.rollback()
        raise


def update_password(user: UserModel, new_password: str, db: Session):
    logger.info("Password change request – user_id=%s", user.id)
    try:
        if verify_password(new_password, user.hash_password):
            logger.warning(
                "Password change rejected – new password equals current for user_id=%s", user.id
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New Password must be different from the current password."
            )
        user.hash_password = get_password_hash(new_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info("Password updated successfully – user_id=%s", user.id)

    except Exception as exc:
        logger.error("Password update failed for user_id=%s: %s", user.id, exc, exc_info=True)
        db.rollback()
        raise


def update_email(user: UserModel, new_email: str, db: Session):
    try:
        email_exist = db.query(UserModel).filter(UserModel.email == new_email).first()
        if user.email == new_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please enter a new email"
            )
        if email_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        user.email = new_email
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except Exception:
        db.rollback()
        raise