from typing import Annotated
from fastapi import APIRouter, Depends
from ..schemas.user_schema import UserSchema
from ..interfaces.position_interface import (
    CreatePositionInterface,
    UpdatePositionInterface,
    PositionsResponseInterface,
    PositionResponseInterface,
)
from ..middlewares.auth_middleware import get_current_user
from ..controllers.position_controller import (
    get_all_positions_by_ids,
    get_position_by_id,
    create_new_position,
    update_current_position,
    close_current_position,
    open_current_position,
    delete_current_position,
)
from ..utils.response_fmt import jsonResponseFmt


router = APIRouter(prefix="/position", tags=["Position"])


@router.get("/{project_id}", response_model=PositionsResponseInterface)
async def get_positions(project_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    positions = get_all_positions_by_ids(project_id, user)
    return jsonResponseFmt([position.to_dict() for position in positions], "Get positions successfully")


@router.get("/{project_id}/{position_id}", response_model=PositionResponseInterface)
async def get_position(project_id: str, position_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    position = get_position_by_id(project_id, position_id, user)
    return jsonResponseFmt(position.to_dict(), f"Get position with id {position_id} successfully")


@router.post("/{project_id}", response_model=PositionResponseInterface)
async def create_position(project_id: str, data: CreatePositionInterface, user: Annotated[UserSchema, Depends(get_current_user)]):
    position = create_new_position(project_id, data, user)
    return jsonResponseFmt(position.to_dict(), f"Create position successfully")


@router.put("/{project_id}/{position_id}", response_model=PositionResponseInterface)
async def update_position(project_id: str, position_id: str, data: UpdatePositionInterface, user: Annotated[UserSchema, Depends(get_current_user)]):
    update_current_position(project_id, position_id, data, user)
    return jsonResponseFmt(None, f"Update position with id {position_id} successfully")


@router.put("/{project_id}/close/{position_id}", response_model=PositionResponseInterface)
async def close_position(project_id: str, position_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    close_current_position(project_id, position_id, user)
    return jsonResponseFmt(None, f"Close position with id {position_id} successfully")


@router.put("/{project_id}/open/{position_id}", response_model=PositionResponseInterface)
async def open_position(project_id: str, position_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    open_current_position(project_id, position_id, user)
    return jsonResponseFmt(None, f"Open position with id {position_id} successfully")


@router.delete("/{project_id}/{position_id}", response_model=PositionResponseInterface)
async def delete_position(project_id: str, position_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    delete_current_position(project_id, position_id, user)
    return jsonResponseFmt(None, f"Delete position with id {position_id} successfully")
