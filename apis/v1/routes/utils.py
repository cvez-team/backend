from typing import Annotated
from fastapi import APIRouter, Depends
from ..schemas.user_schema import UserSchema
from ..middlewares.guard_middleware import user_guard_middleware, GuardCondition
from ..controllers.utils_controller import clear_cache_control
from ..utils.response_fmt import jsonResponseFmt


router = APIRouter(prefix="/utils", tags=["Utils"])


admin_guard = GuardCondition(
    allow_emails=["quangminh57dng@gmail.com"]
)


@router.delete("/reset")
async def reset_cache(
    user: Annotated[UserSchema, Depends(user_guard_middleware(admin_guard))]
):
    '''
    Reset cache.
    '''
    clear_cache_control(user)
    return jsonResponseFmt(None, "Cache cleared.")
