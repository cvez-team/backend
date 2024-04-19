from typing import Annotated
from fastapi import APIRouter, Depends
from ..middlewares.guard_middleware import user_guard_middleware, GuardCondition
from ..middlewares.password_middleware import password_middleware
from ..controllers.utils_controller import clear_cache_control
from ..utils.response_fmt import jsonResponseFmt


router = APIRouter(prefix="/utils", tags=["Utils"])


admin_guard = GuardCondition(
    allow_emails=["quangminh57dng@gmail.com"]
)


@router.delete("/reset", dependencies=[Depends(password_middleware)])
async def reset_cache():
    '''
    Reset cache.
    '''
    clear_cache_control()
    return jsonResponseFmt(None, "Cache cleared.")
