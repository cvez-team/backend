from typing import Annotated
from fastapi import APIRouter, Depends
from ..interfaces.match_interface import (
    MatchesResponseInterface
)
from ..schemas.user_schema import UserSchema
from ..middlewares.auth_middleware import get_current_user
from ..controllers.match_controller import (
    get_all_matches_cv,
    get_all_matches_question
)
from ..utils.response_fmt import jsonResponseFmt


router = APIRouter(prefix="/match", tags=["Match"])


@router.get("/match_cv_jd/{project_id}/{position_id}", response_model=MatchesResponseInterface)
async def get_matches_cv(project_id: str, position_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    matches = get_all_matches_cv(project_id, position_id, user)
    return jsonResponseFmt(matches)


@router.get("/match_question_bank/{project_id}/{position_id}/{cv_id}", response_model=MatchesResponseInterface)
async def get_matches_question(project_id: str, position_id: str, cv_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    matches = get_all_matches_question(project_id, position_id, cv_id, user)
    return jsonResponseFmt(matches)
