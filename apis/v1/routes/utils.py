from typing import Annotated
from fastapi import APIRouter, Depends, File, UploadFile
from ..middlewares.password_middleware import password_middleware
from ..controllers.utils_controller import clear_cache_control, extract_content_control
from ..utils.extractor import get_cv_content
from ..utils.response_fmt import jsonResponseFmt


router = APIRouter(prefix="/utils", tags=["Utils"])


@router.delete("/reset", dependencies=[Depends(password_middleware)])
async def reset_cache():
    '''
    Reset cache.
    '''
    clear_cache_control()
    return jsonResponseFmt(None, "Cache cleared.")


@router.post("/extract-content")
async def extract_content(file: Annotated[UploadFile, File(...)]):
    '''
    Extract the content of the CV file.
    '''
    # Read the content of the file
    filedata = await file.read()
    return jsonResponseFmt(extract_content_control(filedata=filedata, filename=file.filename))
