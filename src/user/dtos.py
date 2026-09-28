from pydantic import BaseModel, ConfigDict, Field


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
    password: str = Field(
        ...,
        min_length=5,
        max_length=30,
        description="Enter a strong password"
    )
    email: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description="Enter your email"
    )


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
    new_password: str