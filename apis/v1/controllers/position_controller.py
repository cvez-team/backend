from typing import AnyStr, Dict
from fastapi import HTTPException, status
from ..schemas.user_schema import UserSchema
from ..schemas.project_schema import ProjectSchema
from ..schemas.position_schema import PositionSchema


def get_all_positions_by_ids(project_id: AnyStr, user: UserSchema):
    '''
    Get all positions by the list of position ids.
    '''
    # if len(user.positions) == 0:
    #     return []

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

    # Get all positions by ids
    position_ids = project.positions

    positions = PositionSchema.find_all_by_ids(position_ids)

    return positions


def get_position_by_id(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    '''
    Get position by id.
    '''
    # if len(user.positions) == 0:
    #     return []

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

    # Get position by id
    position = PositionSchema.find_by_id(position_id)

    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )
    
    return position


def create_new_position(project_id: AnyStr, data: Dict, user: UserSchema):
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

    # Check if project exists
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
        start_date = data.start_date,
        end_date= data.end_date,
    ).create_position()   

    # Update position of project in database
    project.update_positions(position.id)

    return position
    

def update_current_position(project_id: AnyStr, position_id: AnyStr, data: Dict, user: UserSchema):
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

    # Check if project exists
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )
    # Create new project in database
    position = PositionSchema.find_by_id(position_id)

    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )
    data = {
        "name" : data.name,
        "alias" :data.alias,
        "description" : data.description,
        "start_date" : data.start_date,
        "end_date" : data.end_date
    }
    position.update_position(data)
    return position
    
def close_current_position(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    '''
    Close current position.
    '''
 
def open_current_position(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    '''
    Open current position.
    '''

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

    # Check if project exists
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )

    delete = project.update_positions(position_id, is_add=False)
    return delete
