from typing import List, Dict
from fastapi import UploadFile, File
from pydantic import BaseModel, Field
from ..schemas.cv_schema import CVModel


class CVsResponseInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: list[CVModel] = Field(..., description="List of CVs")


class CVResponseInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: CVModel = Field(None, description="CV data")


class CVSummaryResponseInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: str = Field(..., description="CV summary")


class CVDetailResponseInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: Dict[str, Dict[str, float]] = Field(..., description="CV detail")


class _CVUploadResponseInterface(BaseModel):
    progress_id: str = Field(...,
                             description="Progress ID for watching upload progress")


class CVUploadResponseInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: _CVUploadResponseInterface = Field(None, description="CV data")


class _CVUploadProgressInterface(BaseModel):
    percent: Dict[str, int] = Field(..., description="Upload percentage")
    error: Dict[str, str] = Field(..., description="Error status")


class CVUploadProgressInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: _CVUploadProgressInterface | None = Field(...,
                                                    description="Upload progress")


class UploadCVInterface:
    cv = UploadFile
    cvs = List[UploadFile]
    cv_default = File(..., description="CV files to upload")
