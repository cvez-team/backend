from typing import AnyStr, Dict
from fastapi import HTTPException, status
from .user_controller import get_all_users_by_ids
from ..interfaces.project_interface import TypeGetAllProjects
from ..schemas.user_schema import UserSchema
from ..schemas.project_schema import ProjectSchema


def get_all_projects_by_ids(user: UserSchema, get_type: TypeGetAllProjects):
    '''
    Get all projects by the list of project ids.
    '''
    if get_type == "owned":
        if len(user.projects) == 0:
            return []

        projects = ProjectSchema.find_all_by_ids(user.projects)

        # Fetch member data for each project
        for project in projects:
            project.members = get_all_users_by_ids(project.members, user)

    elif get_type == "shared":
        if len(user.shared) == 0:
            return []

        projects = ProjectSchema.find_all_by_ids(user.shared)

        # Fetch member data for each project
        for project in projects:
            project.members = get_all_users_by_ids(project.members, user)

    elif get_type == "deleted":
        if len(user.trash) == 0:
            return []

        projects = ProjectSchema.find_all_by_ids(user.trash)

        # Fetch member data for each project
        for project in projects:
            project.members = get_all_users_by_ids(project.members, user)

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid get type",
        )

    return projects


# Get project by project id
# If the use_alias is True, get project by alias and check permission
# If the use_alias is False, check permission and get project by id
def get_project_by_id(project_id: AnyStr, use_alias: bool, user: UserSchema):
    '''
    Get project by id.
    '''
    # If use alias is True, fetch user and check permission
    if use_alias:
        project = ProjectSchema.find_by_alias(project_id)

        # If project not found, return 404
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        # Check permission
        if project.id not in user.projects and project.id not in user.shared:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access permission to this project",
            )

    # If use alias is False, check permission and get project by id
    else:
        # Reject if project_id not in user's projects
        if project_id not in user.projects and project_id not in user.shared:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access permission to this project",
            )

        project = ProjectSchema.find_by_id(project_id)

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

    return project


# Create new project
# Update project id to user's projects in cache
# Update projects list in cache
def create_new_project(data: Dict, user: UserSchema):
    '''
    Create new project.
    '''
    # Create new project in database
    project = ProjectSchema(
        name=data.name,
        alias=data.alias,
        description=data.description,
        owner=user.id,
    ).create_project()

    # Update user in database
    user.update_user_projects(project.id, is_add=True)

    return project


# Update project name, alias, and description
def update_current_project(project_id: AnyStr, data: Dict, user: UserSchema):
    '''
    Update current project.
    '''
    # Check if user has access to the project
    if project_id not in user.projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project."
        )

    # Get project by id
    project = ProjectSchema.find_by_id(project_id)

    # Check if project exists
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )
    # Update project in database
    update = ProjectSchema(
        name=data.name,
        alias=data.alias,
        description=data.description,
        owner=user.id,
    ).update_project()

    # Update user in database
    user.update_user_projects(project.id, is_add=True)

    return update

# Update last opened timestamp of the project
def update_last_opened_project(project_id: AnyStr, data: Dict, user: UserSchema):
    ...


# Update member permission of the project
def update_member_project(project_id: AnyStr, data: Dict, user: UserSchema):
    ...


# Delete project
def delete_current_project(project_id: AnyStr, user: UserSchema, is_purge: bool = False):
    '''
    Delete current project.
    ''' 
    # Check if user has access to the project
    if project_id not in user.projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project."
        )

    # Get project by id
    project = ProjectSchema.find_by_id(project_id)

    # Check if project exists
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )
    # Update project in database
    delete = ProjectSchema.delete_project(project_id, is_purge)

    # Update user in database
    user.update_user_projects(project.id, is_add=True)

    return delete

# Restore project
def restore_current_project(project_id: AnyStr, user: UserSchema):
    ...
