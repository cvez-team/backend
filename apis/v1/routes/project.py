from typing import Annotated, Optional, AnyStr
from fastapi import APIRouter, Depends
from ..interfaces.project_interface import (
    ProjectsResponseInterface,
    ProjectResponseInterface,
    TypeGetAllProjects,
    CreateProjectInterface,
    UpdateProjectInterface,
    UpdateLastOpenedProjectInterface,
    UpdateMemberProjectInterface
)
from ..schemas.user_schema import UserSchema
from ..middlewares.auth_middleware import get_current_user
from ..controllers.project_controller import (
    get_all_projects_by_ids,
    get_project_by_id,
    create_new_project,
    update_current_project,
    update_member_project,
    delete_current_project,
    restore_current_project
)
from ..utils.response_fmt import jsonResponseFmt


router = APIRouter(prefix="/project", tags=["Project"])


@router.get("/", response_model=ProjectsResponseInterface)
async def get_projects(user: Annotated[UserSchema, Depends(get_current_user)], get_type: TypeGetAllProjects = "owned"):
    projects = get_all_projects_by_ids(user, get_type)
    return jsonResponseFmt([project.to_dict(include_id=True) for project in projects], f"Get {get_type} projects successfully")


@router.get("/{project_id}", response_model=ProjectResponseInterface)
async def get_project(project_id: AnyStr, user: Annotated[UserSchema, Depends(get_current_user)], use_alias: Optional[bool] = False):
    project = get_project_by_id(project_id, use_alias, user)
    return jsonResponseFmt(project.to_dict(include_id=True), f"Get project with id {project_id} successfully")


@router.post("/", response_model=ProjectResponseInterface)
async def create_project(data: CreateProjectInterface, user: Annotated[UserSchema, Depends(get_current_user)]):
    project = create_new_project(data, user)
    return jsonResponseFmt(project.to_dict(include_id=True), f"Project {project.id} created successfully")


@router.put("/{project_id}", response_model=ProjectResponseInterface)
async def update_project(project_id: str, data: UpdateProjectInterface, user: Annotated[UserSchema, Depends(get_current_user)]):
    update_current_project(project_id, data, user)
    return jsonResponseFmt(None, f"Project {project_id} updated successfully")


@router.put("/last/{project_id}", response_model=ProjectResponseInterface)
async def update_last_opened_project(project_id: str, data: UpdateLastOpenedProjectInterface, user: Annotated[UserSchema, Depends(get_current_user)]):
    update_current_project(project_id, data, user)
    return jsonResponseFmt(None, f"Project {project_id} last opened updated successfully")


@router.put("/share/{project_id}", response_model=ProjectResponseInterface)
async def share_project(project_id: str, data: UpdateMemberProjectInterface, user: Annotated[UserSchema, Depends(get_current_user)]):
    update_member_project(project_id, data, user)
    return jsonResponseFmt(None, f"Project {project_id} shared successfully")


@router.delete("/{project_id}")
async def delete_project(project_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    delete_current_project(project_id, user)
    return jsonResponseFmt(None, f"Delete project with id {project_id} successfully")


@router.put("/restore/{project_id}")
async def restore_project(project_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    restore_current_project(project_id, user)
    return jsonResponseFmt(None, f"Restore project with id {project_id} successfully")


@router.delete("/purge/{project_id}")
async def purge_project(project_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    delete_current_project(project_id, user, is_purge=True)
    return jsonResponseFmt(None, f"Purge project with id {project_id} successfully")
