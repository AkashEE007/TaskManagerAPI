from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from src.user.dtos import AdminUpdateSchema, LoginSchema, UserSchema
from src.user.models import UserModel
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

        return new_user

    except Exception:
        db.rollback()
        raise


def login_user(body: LoginSchema, db: Session):
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not is_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong username!")

    if not verify_password(body.password, is_user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Password!")

    exp_time = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.EXP_TIME)

    token = jwt.encode({"_id": is_user.id, "exp":exp_time.timestamp()}, settings.SECRET_KEY, settings.ALGORITHM)

    return {
        "token": token
    }


def get_all_users(db: Session):
    users = db.query(UserModel).all()
    return users


def delete_all_users(db: Session):
    try:
        db.query(UserModel).delete()
        db.commit()

    except Exception:
        db.rollback()
        raise


def update_admin(body: AdminUpdateSchema, user_id: int, db: Session):
    try:
        user = db.query(UserModel).get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

        user.is_admin = body.is_admin
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except Exception:
        db.rollback()
        raise


def update_password(user: UserModel, new_password: str, db: Session):
    try:
        if verify_password(new_password, user.hash_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New Password must be different from the current password."
            )
        user.hash_password = get_password_hash(new_password)
        db.add(user)
        db.commit()
        db.refresh(user)

    except Exception as e:
        db.rollback()
        raise

    