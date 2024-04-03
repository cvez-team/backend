from typing import AnyStr
from fastapi import UploadFile
from ..schemas.user_schema import UserSchema
from ..schemas.cv_schema import CVSchema


def get_all_cvs(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    return [CVSchema()]


def get_cv_by_id(project_id: AnyStr, position_id: AnyStr, cv_id: AnyStr, user: UserSchema):
    return CVSchema()


async def upload_cvs_data(project_id: AnyStr, position_id: AnyStr, user: UserSchema, cvs: list[UploadFile]):
    return "watching-id"


async def upload_cv_data(project_id: AnyStr, position_id: AnyStr, cv: UploadFile):
    return None


def get_upload_progress(progress_id: AnyStr):
    return {
        "percent": {
            "1": 10,
        },
        "uploaded_bytes": {
            "1": 1000,
        },
        "total_bytes": {
            "1": 10000,
        },
        "analyzed": {
            "1": False,
        }
    }


async def download_cv_content(project_id: AnyStr, position_id: AnyStr, cv_id: AnyStr, user: UserSchema) -> bytes:
    return None


def delete_current_cv(project_id: AnyStr, position_id: AnyStr, cv_id: AnyStr, user: UserSchema):
    return None
