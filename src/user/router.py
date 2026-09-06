from fastapi import FastAPI, APIRouter, Depends, status, Request
from src.user.dtos import UserSchema, UserResponseSchema, LoginSchema
from src.utils.db import get_db
from sqlalchemy.orm import Session
from src.user import controller

user_routes = APIRouter(prefix="/user")


@user_routes.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def register(body: UserSchema, db: Session=Depends(get_db)):
    return controller.register(body, db)


@user_routes.post("/login", status_code=status.HTTP_200_OK)
def login(body: LoginSchema, db: Session=Depends(get_db)):
    return controller.login_user(body, db)


@user_routes.get("/is_auth", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def is_auth(request:Request, db: Session=Depends(get_db)):
    return controller.is_authenticated(request, db)