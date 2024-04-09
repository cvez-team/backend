from pydantic import BaseModel, Field
from ..schemas.user_schema import UserModel, UserMinimalModel


class UsersResponseInterface(BaseModel):
    msg: str = Field(..., title="Message")
    data: list[UserModel] = Field(..., title="Users")


class UserResponseInterface(BaseModel):
    msg: str = Field(..., title="Message")
    data: UserModel = Field(..., title="User")


class UsersMinimalResponseInterface(BaseModel):
    msg: str = Field(..., title="Message")
    data: list[UserMinimalModel] = Field(..., title="Users")


class UserMinimalResponseInterface(BaseModel):
    msg: str = Field(..., title="Message")
    data: UserMinimalModel = Field(None, title="User")
