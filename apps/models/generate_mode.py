from pydantic import BaseModel, Field


class GenerateModel(BaseModel):
    cv_id: str = Field(..., title="CV ID")
    jd_id: str = Field(..., title="JD ID")
