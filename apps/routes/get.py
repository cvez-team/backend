from fastapi import APIRouter
from ..controllers.get_controller import (
    get_all_cv_control,
    get_cv_by_id_control,
    get_all_jd_control,
    get_jd_by_id_control,
    get_all_question_control,
    get_question_by_id_control,
)
from ..utils.response_fmt import jsonResponseFmt


# Define get_router
router = APIRouter(prefix="/get", tags=["get"])


# Define route for get all CVs
@router.get("/cv")
async def get_all_cvs():
    cvs = get_all_cv_control()
    return jsonResponseFmt(cvs)


# Define route for get CV by id
@router.get("/cv/{cv_id}")
async def get_cv_by_id(cv_id: str):
    cv = get_cv_by_id_control(cv_id)
    return jsonResponseFmt(cv)


# Define route for get all JDs
@router.get("/jd")
async def get_all_jds():
    jds = get_all_jd_control()
    return jsonResponseFmt(jds)


# Define route for get JD by id
@router.get("/jd/{jd_id}")
async def get_jd_by_id(jd_id: str):
    jd = get_jd_by_id_control(jd_id)
    return jsonResponseFmt(jd)


# Define route for get all questions
@router.get("/question")
async def get_all_questions():
    questions = get_all_question_control()
    return jsonResponseFmt(questions)


# Define route for get question by id
@router.get("/question/{question_id}")
async def get_question_by_id(question_id: str):
    question = get_question_by_id_control(question_id)
    return jsonResponseFmt(question)
