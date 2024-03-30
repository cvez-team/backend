from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from ..schemas.user_schema import UserSchema
from ..providers import cacher, jwt


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

    # Get user Id in token
    uid = data["id"]

    # Check if user is active
    active_users = cacher.get("active_users")
    if not active_users or uid not in active_users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
        )

    # Get user data
    user = UserSchema.find_by_id(uid)

    return user
