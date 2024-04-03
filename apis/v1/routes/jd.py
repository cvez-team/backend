from typing import Annotated
from fastapi import APIRouter, Depends
from ..interfaces.jd_interface import JDResponseInterface, JDUploadInterface
from ..schemas.user_schema import UserSchema
from ..middlewares.auth_middleware import get_current_user
from ..controllers.jd_controller import (
    get_current_jd,
    update_current_jd,
    extract_jd_content
)
from ..utils.response_fmt import jsonResponseFmt


router = APIRouter(prefix="/jd", tags=["JD"])


@router.get("/{project_id}/{position_id}", response_model=JDResponseInterface)
async def get_jd(project_id: str, position_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    jd = get_current_jd(project_id, position_id, user)
    return jsonResponseFmt(jd.to_dict())


@router.put("/{project_id}/{position_id}", response_model=JDResponseInterface)
async def update_jd(project_id: str, position_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    update_current_jd(project_id, position_id, user)
    return jsonResponseFmt(None, "JD updated successfully")


@router.post("/{project_id}/{position_id}/extract", response_model=JDResponseInterface)
async def extract_jd(
    project_id: str,
    position_id: str,
    user: Annotated[UserSchema, Depends(get_current_user)],
    jd: Annotated[JDUploadInterface.jd, JDUploadInterface.jd_default]
):
    extract_jd = await extract_jd_content(project_id, position_id, user, jd)
    return jsonResponseFmt(extract_jd.to_dict())
