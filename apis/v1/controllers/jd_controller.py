from typing import AnyStr
from ..schemas.user_schema import UserSchema
from ..schemas.jd_schema import JDSchema


def get_current_jd(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    return JDSchema()


def update_current_jd(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    return None


async def extract_jd_content(project_id: AnyStr, position_id: AnyStr, user: UserSchema, jd: AnyStr):
    return JDSchema()
