from fastapi import APIRouter, Depends
from ..models.match_model import MatchCVModel, MatchQuestionModel
from ..models.user_model import UserModel
from ..middlewares.auth_middleware import get_current_user
from ..controllers.match_controller import match_cv_control, match_question_control
from ..utils.response_fmt import jsonResponseFmt


# Define match_router
router = APIRouter(prefix="/match", tags=["match"])


# Route for match cv
@router.post("/cv")
async def match_cv(data: MatchCVModel, user: UserModel = Depends(get_current_user)):
    match_results = match_cv_control(data.jd_id, 100, user.id, user.fmt)
    return jsonResponseFmt(match_results)


# Route for match question
@router.post("/question")
async def match_question(data: MatchQuestionModel, user: UserModel = Depends(get_current_user)):
    match_results = match_question_control(
        data.cv_id, data.limit, user.id, user.fmt)
    return jsonResponseFmt(match_results)
