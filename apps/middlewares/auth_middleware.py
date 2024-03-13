from ..models.user_model import UserModel
from ..utils.mock import default_fmt


# Get the auth token from the request header,
# parse token to get user data, and return the user data.
def get_current_user():
    return UserModel("cvez", default_fmt)
