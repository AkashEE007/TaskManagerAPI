from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    name: str
    username: str
    password: str
    email: str
    is_admin: bool = False


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
    