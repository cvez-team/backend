from fastapi import APIRouter
from ..models.uploads_model import UploadsModel
from ..utils.response_fmt import jsonResponseFmt

# Define uploads_router
router = APIRouter(prefix="/uploads", tags=["uploads"])


# Define route for uploads
@router.post("/")
async def create_upload(data: UploadsModel):
    return jsonResponseFmt(data.model_dump_json())
