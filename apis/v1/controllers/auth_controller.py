from typing import AnyStr, List
import requests
from fastapi import HTTPException
from ..schemas.user_schema import UserSchema
from ..providers import cacher, jwt
from ..utils.constants import GOOGLE_VERIFY_URL


def login_control(access_token: AnyStr):
    # Get User information from Google API
    url = GOOGLE_VERIFY_URL + access_token
    response = requests.get(url, headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    })

    # Handle error and response
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Google API Error"
        )

    # Get user data from Google API
    google_data = response.json()

    # Check if user with email exists in Database
    user = UserSchema.find_by_email(google_data["email"])

    # If user does not exist, create a new user
    if not user:
        user = UserSchema(
            name=google_data["name"],
            email=google_data["email"],
            avatar=google_data["picture"]
        ).create_user()

    # Activate the user in cache
    active_users = cacher.get("active_users")
    if not active_users:
        active_users = []
    if user.id not in active_users:
        active_users.append(user.id)
        cacher.set("active_users", active_users)

    # Create JWT Token
    token = jwt.encrypt({
        "id": user.id,
    })

    return token


def logout_control(user: UserSchema):
    # Get active users from cache
    active_users: List | None = cacher.get("active_users")
    if not active_users:
        return
    if user.id in active_users:
        active_users.remove(user.id)
        cacher.set("active_users", active_users)
    return
