from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.user import controller
from src.user.dtos import (
    AdminUpdateSchema,
    DeleteAllConfirmation,
    EmailUpdateSchema,
    LoginSchema,
    PasswordUpdateSchema,
    UserResponseSchema,
    UserSchema,
)
from src.user.models import UserModel
from src.utils.db import get_db
from src.utils.helpers import is_authenticated, require_admin

user_routes = APIRouter(prefix="/user", tags=["Users"])


@user_routes.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def register(body: UserSchema, db: Session=Depends(get_db)):
    return controller.register(body, db)


@user_routes.post("/login", status_code=status.HTTP_200_OK)
def login(body: LoginSchema, db: Session=Depends(get_db)):
    return controller.login_user(body, db)


@user_routes.get("/is_auth", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def is_auth(user: UserModel=Depends(is_authenticated), db: Session=Depends(get_db)):
    return user


@user_routes.post("/admin/users/delete-all", status_code=status.HTTP_204_NO_CONTENT)
def delete_all(body: DeleteAllConfirmation, db: Session=Depends(get_db), user: UserModel=Depends(require_admin)):
    return controller.delete_all_users(db, body)


@user_routes.get("/get_all_users", response_model= list[UserResponseSchema],status_code=status.HTTP_200_OK)
def get_all_users(db: Session=Depends(get_db), user: UserModel=Depends(require_admin)):
    return controller.get_all_users(db)


@user_routes.put("/update_user/{user_id}/make_admin", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def make_admin(body: AdminUpdateSchema, user_id: int, db: Session=Depends(get_db), user: UserModel=Depends(require_admin)):
    return controller.update_admin(body, user_id, db)


@user_routes.put("/update_password", status_code=status.HTTP_200_OK)
def update_password(body: PasswordUpdateSchema, user: UserModel=Depends(is_authenticated), db: Session=Depends(get_db)):
    return controller.update_password(user, body.new_password, db)


@user_routes.put("/update_email", status_code=status.HTTP_200_OK)
def update_email(body: EmailUpdateSchema, user: UserModel=Depends(is_authenticated), db: Session=Depends(get_db)):
    return controller.update_email(user, body.new_email, db)