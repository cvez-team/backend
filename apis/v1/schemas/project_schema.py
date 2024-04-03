from typing import Dict, AnyStr, List
from pydantic import BaseModel, Field
from ..schemas.user_schema import UserSchema, UserMinimalModel
from ..providers import project_db
from ..utils.utils import get_current_time


class ProjectModel(BaseModel):
    id: str = Field(..., title="Project ID")
    name: str = Field(..., title="Project Name")
    description: str = Field(..., title="Project Description")
    alias: str = Field(..., title="Project Alias")
    owner: str = Field(..., title="Project Owner")
    members: list[UserMinimalModel] = Field(..., title="Project Members")
    positions: list[str] = Field(..., title="Project Positions")
    last_opened: str = Field(..., title="Project Last Opened")


class ProjectSchema:
    '''
    Schema and Validation for Project.
    '''

    def __init__(
        self,
        project_id: AnyStr = None,
        name: AnyStr = "",
        description: AnyStr = "",
        alias: AnyStr = "",
        owner: AnyStr = "",
        members: List[AnyStr] | List[UserSchema] = [],
        positions: List[AnyStr] = [],
        last_opened: AnyStr = get_current_time(),
    ):
        self.id = project_id
        self.name = name
        self.description = description
        self.alias = alias
        self.owner = owner
        self.members = members
        self.positions = positions
        self.last_opened = last_opened

    def to_dict(self, include_id=True):
        data_dict = {
            "name": self.name,
            "description": self.description,
            "alias": self.alias,
            "owner": self.owner,
            "members": [member.to_dict(minimal=True) if isinstance(member, UserSchema) else member for member in self.members],
            "positions": self.positions,
            "last_opened": self.last_opened,
        }
        if include_id:
            data_dict["id"] = self.id
        return data_dict

    @staticmethod
    def from_dict(data: Dict):
        return ProjectSchema(
            project_id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            alias=data.get("alias"),
            owner=data.get("owner"),
            members=data.get("members"),
            positions=data.get("positions"),
            last_opened=data.get("last_opened"),
        )

    @staticmethod
    def find_by_alias(alias: AnyStr):
        # Get in cache
        queries = project_db.cacher.get(
            f"{project_db.collection_name}:{alias}")
        if not queries:
            queries = project_db.query_equal("alias", alias)
            if len(queries) == 0:
                return None
            # Save to cache
            project_db.cacher.set(
                f"{project_db.collection_name}:{alias}", queries)
        return ProjectSchema.from_dict(queries[0])

    @staticmethod
    def find_by_id(project_id: AnyStr):
        data = project_db.get_by_id(project_id)
        if not data:
            return None
        return ProjectSchema.from_dict(data)

    @staticmethod
    def find_all_by_ids(project_ids: List[AnyStr]):
        projects = project_db.get_all_by_ids(ids=project_ids)
        return [ProjectSchema.from_dict(project) for project in projects]

    def create_project(self):
        project_id = project_db.create(self.to_dict(include_id=False))
        self.id = project_id
        # Add data to cache
        project_db.cacher.set(
            f"{project_db.collection_name}:{project_id}", self.to_dict(include_id=True))
        return self
    
    def update_positions(self, positions_id: AnyStr, is_add: bool = True):
        if is_add:
            self.positions.append(positions_id)
        else:
            self.positions.remove(positions_id)
        # Add data to cache
        project_db.update(self.id, {"positions": self.positions})
        return self  
    