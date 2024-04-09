from typing import Annotated
from fastapi import Depends, HTTPException, status
from ..schemas.user_schema import UserSchema
from ..middlewares.auth_middleware import get_current_user


class GuardCondition:
    def __init__(self, allow_emails: list[str] = []):
        self.allow_emails = allow_emails

    def check(self, user: UserSchema) -> bool:
        if user.email not in self.allow_emails:
            return False
        return True


def user_guard_middleware(guard_condition: GuardCondition):
    def _wrapper(user: Annotated[UserSchema, Depends(get_current_user)]):
        if not guard_condition.check(user):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not allowed to access this route",
            )
        return user

    return _wrapper
