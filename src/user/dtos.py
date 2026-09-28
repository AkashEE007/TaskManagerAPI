from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.utils.helpers import check_password_strength, email_validation

PasswordStrength = Annotated[str, Field(
    ..., 
    min_length=5,
    max_length=30,
    description="Enter a strong password"
    )]

EmailCheck = Annotated[str, Field(
        ...,
        min_length=5,
        max_length=325,
        description="Enter your email"
    )]

class UserSchema(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=10,
        description="Name of user"
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=10,
        description="Username should be unique"
    )

    @field_validator("password")
    @classmethod
    def password_strength(cls, pwd: str):
        return check_password_strength(pwd)
    
    password: PasswordStrength
    email: EmailCheck
    @field_validator("email")
    @classmethod
    def email_validator(cls, email: str):
        return email_validation(email)


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    username: str
    email: str
    id: int
    is_admin: bool


class LoginSchema(BaseModel):
    username: str
    password: str


class AdminUpdateSchema(BaseModel):
    is_admin: bool


class PasswordUpdateSchema(BaseModel):
    new_password: PasswordStrength

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, pwd: str):
        return check_password_strength(pwd)


class EmailUpdateSchema(BaseModel):
    new_email: EmailCheck
    @field_validator("new_email")
    @classmethod
    def email_validator(cls, email: str):
        return email_validation(email)
    
