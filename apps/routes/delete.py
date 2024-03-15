from fastapi import APIRouter
from ..controllers.delete_controller import (
    delete_jd_by_id_control,
    delete_cv_by_id_control,
    delete_question_by_id_control,
)
from ..utils.response_fmt import jsonResponseFmt


# Define delete_router
router = APIRouter(prefix="/delete", tags=["delete"])


# Define route for delete CV by id
@router.delete("/cv/{cv_id}")
async def delete_cv_by_id(cv_id: str):
    delete_cv_by_id_control(cv_id)
    return jsonResponseFmt(cv_id)


# Define route for delete JD by id
@router.delete("/jd/{jd_id}")
async def get_jd_by_id(jd_id: str):
    delete_jd_by_id_control(jd_id)
    return jsonResponseFmt(jd_id)


# Define route for delete question by id
@router.delete("/question/{question_id}")
async def delete_question_by_id(question_id: str):
    delete_question_by_id_control(question_id)
    return jsonResponseFmt(question_id)
