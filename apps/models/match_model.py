from pydantic import BaseModel, Field


class MatchCVModel(BaseModel):
    jd_id: str = Field(..., description="The id of the job description")


class MatchQuestionModel(BaseModel):
    cv_id: str = Field(..., description="The id of the cv")
