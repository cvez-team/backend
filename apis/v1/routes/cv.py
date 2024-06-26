from typing import Annotated
from io import BytesIO
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from ..schemas.user_schema import UserSchema
from ..interfaces.cv_interface import (
    UploadCVInterface,
    CVsResponseInterface,
    CVResponseInterface,
    CVSummaryResponseInterface,
    CVUploadProgressInterface,
    CVUploadResponseInterface,
    CVDetailResponseInterface
)
from ..middlewares.auth_middleware import get_current_user
from ..controllers.cv_controller import (
    get_all_cvs,
    get_cv_by_id,
    upload_cvs_data,
    upload_cv_data,
    get_upload_progress,
    download_cv_content,
    get_cv_summary_control,
    get_cv_detail_control,
    delete_current_cv
)
from ..utils.response_fmt import jsonResponseFmt


router = APIRouter(prefix="/cv", tags=["CV"])


@router.get("/{project_id}/{position_id}", response_model=CVsResponseInterface)
async def get_cvs(project_id: str, position_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    cvs = get_all_cvs(project_id, position_id, user)
    return jsonResponseFmt([cv.to_dict() for cv in cvs])


@router.get("/{project_id}/{position_id}/{cv_id}", response_model=CVResponseInterface)
async def get_cv(project_id: str, position_id: str, cv_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    cv = get_cv_by_id(project_id, position_id, cv_id, user)
    return jsonResponseFmt(cv.to_dict())


@router.post("/{project_id}/{position_id}/uploads", response_model=CVUploadResponseInterface)
async def upload_cvs(
    project_id: str,
    position_id: str,
    user: Annotated[UserSchema, Depends(get_current_user)],
    cvs: Annotated[UploadCVInterface.cvs, UploadCVInterface.cv_default],
    bg_tasks: BackgroundTasks,
):
    upload_id = await upload_cvs_data(project_id, position_id, user, cvs, bg_tasks)
    return jsonResponseFmt({"progress_id": upload_id})


@router.post("/{position_id}/upload", response_model=CVResponseInterface)
async def upload_cv(
    position_id: str,
    cv: Annotated[UploadCVInterface.cv, UploadCVInterface.cv_default],
    bg_tasks: BackgroundTasks
):
    await upload_cv_data(position_id, cv, bg_tasks)
    return jsonResponseFmt(None, "CV uploaded successfully")


@router.get("/{watch_id}", response_model=CVUploadProgressInterface)
async def get_progress(watch_id: str):
    progress = get_upload_progress(watch_id)
    return jsonResponseFmt(progress)


@router.get("/{project_id}/{position_id}/{cv_id}/download", response_class=StreamingResponse)
async def download_cv(project_id: str, position_id: str, cv_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    cv_content = await download_cv_content(project_id, position_id, cv_id, user)
    return StreamingResponse(BytesIO(cv_content), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={cv_id}.pdf"})


@router.get("/{project_id}/{position_id}/{cv_id}/summary", response_model=CVSummaryResponseInterface)
async def ai_summary_cv(project_id: str, position_id: str, cv_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    cv_summary = get_cv_summary_control(project_id, position_id, cv_id, user)
    return jsonResponseFmt(cv_summary)


@router.get("/{project_id}/{position_id}/{cv_id}/detail", response_model=CVDetailResponseInterface)
async def get_detail_cv(project_id: str, position_id: str, cv_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    cv_detail = get_cv_detail_control(project_id, position_id, cv_id, user)
    return jsonResponseFmt(cv_detail)


@router.delete("/{project_id}/{position_id}/{cv_id}", response_model=CVResponseInterface)
async def delete_cv(project_id: str, position_id: str, cv_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    delete_current_cv(project_id, position_id, cv_id, user)
    return jsonResponseFmt(None, f"CV {cv_id} deleted successfully")
