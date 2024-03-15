from fastapi import APIRouter, Depends
from ..models.generate_mode import GenerateModel
from ..models.user_model import UserModel
from ..middlewares.auth_middleware import get_current_user
from ..controllers.generate_controller import generate_control
from ..utils.response_fmt import jsonResponseFmt


# Define generate_router
router = APIRouter(prefix="/generate", tags=["generate"])


@router.post("/cv")
def generate_cv(data: GenerateModel, user: UserModel = Depends(get_current_user)):
    summarization = generate_control(data.cv_id, data.jd_id, user.id, user.fmt)
    return jsonResponseFmt(summarization)
