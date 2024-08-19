from typing import Annotated
import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from ..schemas.user_schema import UserSchema
from ..providers import jwt


security = HTTPBearer()


# Get the auth token from the request header,
# parse token to get user data, and return the user data.
def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    # Get token
    token = credentials.credentials

    # If Authorization is not provided, return Un-authorized.
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization Token is required",
        )

    # Decrypted token to get user data.
    data = jwt.decrypt(token)

    # Handle if data is None
    if not data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
        )

    # Get user Id, Expiration time in token
    uid = data["id"]
    exp = data["exp"]

    # Check if user is active
    if datetime.datetime.fromtimestamp(exp, tz=datetime.timezone.utc) < datetime.datetime.now(tz=datetime.timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired Token",
        )

    # Get user data
    user = UserSchema.find_by_id(uid)

    # If user is not found, return Un-authorized.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
