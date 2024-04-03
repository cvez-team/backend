from typing import Annotated
from fastapi import APIRouter, Depends
from ..interfaces.auth_interface import (
    AuthInterface,
    LoginResponseInterface,
)
from ..interfaces.user_interface import UserResponseInterface
from ..schemas.user_schema import UserSchema
from ..middlewares.auth_middleware import get_current_user
from ..controllers.auth_controller import login_control, logout_control
from ..utils.response_fmt import jsonResponseFmt


router = APIRouter(prefix="/auth", tags=["Auth"])


# Login route with Google Access Token
# @param: gtoken (str) - Google Access Token
# @return: token (str) - JWT Token
@router.post("/login", response_model=LoginResponseInterface)
async def login(data: AuthInterface):
    token = login_control(data.gtoken)
    return jsonResponseFmt({"token": token})


@router.get("/me", response_model=UserResponseInterface)
async def get_me(user: Annotated[UserSchema, Depends(get_current_user)]):
    return jsonResponseFmt(user.to_dict(include_id=True))


@router.post("/logout", response_model=LoginResponseInterface)
async def logout(user: Annotated[UserSchema, Depends(get_current_user)]):
    logout_control(user)
    return jsonResponseFmt(None, msg="Logged out")
