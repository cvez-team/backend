from fastapi import APIRouter
from ..utils.response_fmt import jsonResponseFmt


# Define get_router
router = APIRouter(prefix="/get", tags=["get"])


# Define route for get all CVs
@router.get("/cv")
async def get_all_cvs():
    return jsonResponseFmt("Get all CVs")


# Define route for get CV by id
@router.get("/cv/{cv_id}")
async def get_cv_by_id(cv_id: str):
    return jsonResponseFmt(f"Get CV by id {cv_id}")


# Define route for get all JDs
@router.get("/jd")
async def get_all_jds():
    return jsonResponseFmt("Get all JDs")


# Define route for get JD by id
@router.get("/jd/{jd_id}")
async def get_jd_by_id(jd_id: str):
    return jsonResponseFmt(f"Get JD by id {jd_id}")


# Define route for get all questions
@router.get("/question")
async def get_all_questions():
    return jsonResponseFmt("Get all questions")


# Define route for get question by id
@router.get("/question/{question_id}")
async def get_question_by_id(question_id: str):
    return jsonResponseFmt(f"Get question by id {question_id}")
