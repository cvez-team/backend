from fastapi import APIRouter, Depends
from ..models.news_model import CVUploadsModel, JDModel, QuestionModel
from ..models.user_model import UserModel
from ..controllers.cv_controller import cv_control
from ..controllers.jd_controller import jd_control
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
    cv_datas = []
    for _data in data:
        # Read data bytes
        file_data = await _data.read()
        file_name = _data.filename
        # Process the file
        cv_data = cv_control(
            file=file_data, filename=file_name, user_id=user["id"])
        cv_datas.append(cv_data)

    return jsonResponseFmt(cv_datas)


# Route for create new JD
@router.post("/jd")
async def create_jd(jd: JDModel):

    jd = jd_control(jd.title,jd.content,"cvez")
    
    return jsonResponseFmt(jd.model_dump())


# Route for create new question
@router.post("/question")
async def create_question(question: QuestionModel):

    return jsonResponseFmt(question.model_dump())
