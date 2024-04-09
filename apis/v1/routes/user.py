from typing import Annotated
from fastapi import APIRouter, Depends
from ..schemas.user_schema import UserSchema
from ..interfaces.user_interface import (
    UsersResponseInterface,
    UserResponseInterface,
    UsersMinimalResponseInterface
)
from ..middlewares.auth_middleware import get_current_user
from ..middlewares.guard_middleware import user_guard_middleware, GuardCondition
from ..controllers.user_controller import (
    get_all_users,
    get_user_by_id,
    find_user_by_query
)
from ..utils.response_fmt import jsonResponseFmt


router = APIRouter(prefix="/user", tags=["User"])


admin_guard = GuardCondition(
    allow_emails=["quangminh57dng@gmail.com"]
)


@router.get("/", response_model=UsersResponseInterface)
async def get_users(user: Annotated[UserSchema, Depends(user_guard_middleware(admin_guard))]):
    users = get_all_users(user)
    return jsonResponseFmt([user.to_dict() for user in users])


@router.get("/find", response_model=UsersMinimalResponseInterface)
async def find_users(query: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    users = find_user_by_query(query, user)
    return jsonResponseFmt([user.to_dict(minimal=True) for user in users])


@router.get("/{user_id}", response_model=UserResponseInterface)
async def get_user(user_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    current_user = get_user_by_id(user_id, user)
    return jsonResponseFmt(current_user.to_dict())
