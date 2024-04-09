from typing import AnyStr
from pydantic import BaseModel
from fastapi import HTTPException, status
from ..schemas.user_schema import UserSchema
from ..schemas.project_schema import ProjectSchema
from ..schemas.position_schema import PositionSchema
from ..schemas.criteria_schema import CriteriaSchema
from ..providers import vector_db


def get_all_positions_by_ids(project_id: AnyStr, user: UserSchema):
    '''
    Get all positions by the list of position ids.
    '''
    # Check if user has access to the project
    if project_id not in user.projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project."
        )

    # Get project by id
    project = ProjectSchema.find_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )

    # Get all positions by ids
    positions = PositionSchema.find_all_by_ids(project.positions)

    return positions


def get_position_by_id(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    '''
    Get position by id.
    '''
    # Check if user has access to the project
    if project_id not in user.projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project."
        )

    # Get project by id
    project = ProjectSchema.find_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )

    # Check if position exists
    if position_id not in project.positions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )

    # Get position by id
    position = PositionSchema.find_by_id(position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )

    return position


def create_new_position(project_id: AnyStr, data: BaseModel, user: UserSchema):
    '''
    Create a new position.
    '''
    # Check if user has access to the project
    if project_id not in user.projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project."
        )

    # Get project by id
    project = ProjectSchema.find_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )

    # Create new position in database
    position = PositionSchema(
        name=data.name,
        alias=data.alias,
        description=data.description,
        start_date=data.start_date,
        end_date=data.end_date,
        criterias=[CriteriaSchema.from_dict(
            criteria) for criteria in data.criterias]
    ).create_position()

    # Update position of project in database
    project.update_positions(position.id, is_add=True)

    # Create new vector database collection
    vector_db.create_collection(position.id)

    return position


def update_current_position(project_id: AnyStr, position_id: AnyStr, data: BaseModel, user: UserSchema):
    '''
    Update current position.
    '''
    # Check if user has access to the project
    if project_id not in user.projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project."
        )

    # Get project by id
    project = ProjectSchema.find_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )

    # Check if position exists
    if position_id not in project.positions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )

    # Get position by id
    position = PositionSchema.find_by_id(position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )

    # Update position in database
    position.update_position(data=data.model_dump(exclude_defaults=True))


def update_criteria_position(project_id: AnyStr, position_id: AnyStr, data: BaseModel, user: UserSchema):
    '''
    Update current position criteria.
    '''
    # Check if user has access to the project
    if project_id not in user.projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project."
        )

    # Get project by id
    project = ProjectSchema.find_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )

    # Check if position exists
    if position_id not in project.positions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )

    # Get position by id
    position = PositionSchema.find_by_id(position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )

    # Create new criteria in database
    for criteria in data.criterias:
        CriteriaSchema.from_dict(criteria)


def update_status_current_position(project_id: AnyStr, position_id: AnyStr, user: UserSchema, is_closed: bool):
    '''
    Open or Close current position.
    '''
    # Check if user has access to the project
    if project_id not in user.projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project."
        )

    # Get project by id
    project = ProjectSchema.find_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )

    # Check if position exists
    if position_id not in project.positions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )

    # Get position by id
    position = PositionSchema.find_by_id(position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )

    # Update position in database
    if is_closed:
        position.close_position()
    else:
        position.open_position()


def delete_current_position(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    '''
    Delete current position.
    '''
    # Check if user has access to the project
    if project_id not in user.projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project."
        )

    # Get project by id
    project = ProjectSchema.find_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )

    # Check if position exists
    if position_id not in project.positions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )

    # Get position by id
    position = PositionSchema.find_by_id(position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )

    # Update position of project in database
    position.delete_position()
    project.update_positions(position_id, is_add=False)
    vector_db.delete_collection(position_id)
