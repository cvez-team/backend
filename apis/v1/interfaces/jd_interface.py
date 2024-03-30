from pydantic import BaseModel, Field
from fastapi import UploadFile, File
from ..schemas.jd_schema import JDModel


class JDResponseInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: JDModel = Field(..., description="JD data")


class JDUploadInterface:
    jd = UploadFile
    jd_default = File(..., description="JD file")
