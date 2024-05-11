from typing import AnyStr, List
from fastapi import HTTPException, status
from ..schemas.user_schema import UserSchema


def get_all_users(user: UserSchema):
    users = UserSchema.find_all()
    return users


def get_all_users_by_ids(ids: List[AnyStr], user: UserSchema):
    if len(ids) == 0:
        return []

    members = UserSchema.find_all_by_ids(ids)

    return members


def get_user_by_id(user_id: str, user: UserSchema):
    current_user = UserSchema.find_by_id(user_id)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return current_user


def find_user_by_query(query: AnyStr, user: UserSchema):
    users = UserSchema.find_user_by_substring(query)
    return users
