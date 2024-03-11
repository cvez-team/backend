from fastapi import APIRouter, Depends
from ..models.news_model import CVUploadsModel, JDModel, QuestionModel
from ..models.user_model import UserModel
from ..controllers.cv_controller import cv_control
from ..controllers.question_controller import question_control
from ..middlewares.auth_middleware import get_current_user
from ..utils.response_fmt import jsonResponseFmt

# Define uploads_router
router = APIRouter(prefix="/new", tags=["new"])


# Route for Uploading CVs
@router.post("/cv")
async def create_cv(
    data: CVUploadsModel.files = CVUploadsModel.files_default,
    user: UserModel = Depends(get_current_user)
):

    return jsonResponseFmt(user.model_dump())


# Route for create new JD
@router.post("/jd")
async def create_jd(jd: JDModel):

    return jsonResponseFmt(jd.model_dump())


# Route for create new question
@router.post("/question")
async def create_question(question: QuestionModel):
    question = question_control(
        content=question.content)
    return jsonResponseFmt(data=question)
