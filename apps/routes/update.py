from fastapi import APIRouter
from ..utils.response_fmt import jsonResponseFmt
from ..controllers.update_controller import (
    update_cv_content_control,
    update_jd_content_control,
    update_question_content_control,
)

# Define get_router
router = APIRouter(prefix="/update", tags=["update"])

# Define route for update CV content by id
@router.put("/cv/{cv_id}")
async def update_cv_content(cv_id: str, new_content: dict):
    updated_cv = update_cv_content_control(cv_id, new_content)
    return jsonResponseFmt(updated_cv)

# Define route for update JD content by id
@router.put("/jd/{jd_id}")
async def update_jd_content(jd_id: str, new_content: dict):
    updated_jd = update_jd_content_control(jd_id, new_content)
    return jsonResponseFmt(updated_jd)


# Define route for update question content by id
@router.put("/question/{question_id}")
async def update_question_content(question_id: str, new_content: dict):
    updated_question = update_question_content_control(question_id, new_content)
    return jsonResponseFmt(updated_question)



