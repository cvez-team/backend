from fastapi import APIRouter, Depends
from ..models.match_model import MatchCVModel, MatchQuestionModel
from ..models.user_model import UserModel
from ..middlewares.auth_middleware import get_current_user
from ..utils.response_fmt import jsonResponseFmt


# Define match_router
router = APIRouter(prefix="/match", tags=["match"])


# Route for match cv
@router.post("/cv")
async def match_cv(data: MatchCVModel, user: UserModel = Depends(get_current_user)):

    return jsonResponseFmt(data.model_dump())


# Route for match question
@router.post("/question")
async def match_question(data: MatchQuestionModel, user: UserModel = Depends(get_current_user)):

    return jsonResponseFmt(data.model_dump())
