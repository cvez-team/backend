from pydantic import BaseModel, Field
from typing import List
from fastapi import UploadFile, File


class CVUploadsModel:
    files = List[UploadFile]
    files_default = File(..., description="List of CV files to upload")


class JDModel(BaseModel):
    title: str = Field(..., description="The title of the job description")
    content: str = Field(..., description="The content of the job description")


class QuestionModel(BaseModel):
    # title: str = Field(..., description="The title of the question")
    content: List[str] = Field(..., description="The content of the question")
    # answer: str = Field(..., description="The answer of the question")
