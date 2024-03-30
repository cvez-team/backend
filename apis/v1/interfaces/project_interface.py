from typing import Literal
from pydantic import BaseModel, Field
from ..schemas.project_schema import ProjectModel


TypeGetAllProjects = Literal["owned", "shared", "deleted"]


class ProjectResponseInterface(BaseModel):
    msg: str = Field(..., title="Message")
    data: ProjectModel = Field(None, title="Project Data")


class ProjectsResponseInterface(BaseModel):
    msg: str = Field(..., title="Message")
    data: list[ProjectModel] = Field(..., title="Projects Data")


class CreateProjectInterface(BaseModel):
    name: str = Field(..., title="Project Name")
    alias: str = Field(..., title="Project Alias")
    description: str = Field(None, title="Project Description")


class UpdateProjectInterface(BaseModel):
    name: str = Field(None, title="Project Name")
    alias: str = Field(None, title="Project Alias")
    description: str = Field(None, title="Project Description")


class UpdateLastOpenedProjectInterface(BaseModel):
    last_open: str = Field(..., title="Last Opened Time")


class UpdateMemberProjectInterface(BaseModel):
    members: list[str] = Field(..., title="Project Members")
    is_add: bool = Field(True, title="Add or Remove Member")
