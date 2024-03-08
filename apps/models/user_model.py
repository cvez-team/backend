from pydantic import BaseModel, Field


class UserModel(BaseModel):
    id: str = Field(..., description="The user's id")
