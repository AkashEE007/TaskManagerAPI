import re

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from src.user.models import UserModel
from src.utils.db import get_db
from src.utils.security import security
from src.utils.settings import settings


def is_authenticated(
        credentials: HTTPAuthorizationCredentials = Depends(security), 
        db: Session = Depends(get_db)):
    try:
        # token = request.headers.get("authorization")
        token = credentials.credentials
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized!")
        # token = token.split(" ")[-1]

        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

        user_id = data.get("_id")
        
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized!")

        return user

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized!")


def require_admin(user: UserModel = Depends(is_authenticated)):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access is required for this action"
        )
    return user


def check_password_strength(pwd: str) -> str:
    """
        Validate that a password contains at least:
        • one uppercase letter
        • one digit
        • one special character
    """
    if not re.search(r"[A-Z]", pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Password must contain an uppercase character")
    if not re.search(r"[0-9]", pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Password must contain an Integer")
    if not re.search(r"[^A-Za-z0-9]", pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Password must contain a special character")
    return pwd


def email_validation(email_id):
    """
        Validate an email address according to the custom constraints:

        * Exactly one ``@`` character.
        * Local part (the part before ``@``) must be 3‑55 characters long.
        * Domain part (the part after ``@``) must be 5‑255 characters long
        * this range already includes the “.com” (or any other TLD) suffix.
    """

    if email_id.count("@") != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email can contain only one @ character")

    local_part, domain_part = email_id.split("@", 1)

    if not (3 <= len(local_part) <= 55):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number characters before @ should be between 3 and 55"
        )

    if not (5 <= len(domain_part) <= 255):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of characters after should be between 5 and 255"
        )

    if not re.fullmatch(r"[^\s]+", email_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email cannot contain spaces"
        )

    return email_id
