from typing import AnyStr, List
from ..schemas.user_schema import UserSchema


def get_all_users(user: UserSchema):
    ...


def get_all_users_by_ids(ids: List[AnyStr], user: UserSchema):
    if len(ids) == 0:
        return []

    members = UserSchema.find_all_by_ids(ids)

    return members


def get_user_by_id(user_id: str, user: UserSchema):
    ...


def find_user_by_query(query: AnyStr, user: UserSchema):
    ...
