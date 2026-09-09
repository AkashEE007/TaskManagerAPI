from fastapi import Request, HTTPException, status, Depends
from src.utils.settings import settings
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from src.user.models import UserModel
from src.utils.db import get_db
from src.utils.security import security
from fastapi.security import HTTPAuthorizationCredentials

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
