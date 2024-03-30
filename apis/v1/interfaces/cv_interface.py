from typing import List, Dict
from fastapi import UploadFile, File
from pydantic import BaseModel, Field
from ..schemas.criteria_schema import CriteriaModel


class CVsResponseInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: list[CriteriaModel] = Field(..., description="List of CVs")


class CVResponseInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: CriteriaModel = Field(None, description="CV data")


class _CVUploadResponseInterface(BaseModel):
    progress_id: str = Field(...,
                             description="Progress ID for watching upload progress")


class CVUploadResponseInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: _CVUploadResponseInterface = Field(None, description="CV data")


class _CVUploadProgressInterface(BaseModel):
    percent: Dict[str, int] = Field(..., description="Upload percentage")
    uploaded_bytes: Dict[str, int] = Field(..., description="Uploaded bytes")
    total_bytes: Dict[str, int] = Field(..., description="Total bytes")
    analyzed: Dict[str, bool] = Field(..., description="Analyzed status")


class CVUploadProgressInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: _CVUploadProgressInterface = Field(...,
                                             description="Upload progress")


class UploadCVInterface:
    cv = UploadFile
    cvs = List[UploadFile]
    cv_default = File(..., description="CV files to upload")
