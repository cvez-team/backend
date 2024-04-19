from typing import AnyStr
from pydantic import BaseModel
from fastapi import HTTPException, status
from ..schemas.user_schema import UserSchema
from ..schemas.project_schema import ProjectSchema
from ..schemas.position_schema import PositionSchema
from ..schemas.criteria_schema import CriteriaSchema
from ..schemas.jd_schema import JDSchema
from ..controllers.cv_controller import delete_cvs_by_ids
from ..providers import vector_db


def _validate_permissions(project_id: AnyStr, user: UserSchema):
    '''
    Validate if user has access to the project.
    '''
    if project_id not in user.projects and project_id not in user.shared:
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

    return project


def get_all_positions_by_ids(project_id: AnyStr, user: UserSchema):
    '''
    Get all positions by the list of position ids.
    '''
    # Validate if user has access to the project
    project = _validate_permissions(project_id, user)

    # Get all positions by ids
    positions = PositionSchema.find_all_by_ids(project.positions)

    return positions


def get_position_by_id(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    '''
    Get position by id.
    '''
    # Validate if user has access to the project
    project = _validate_permissions(project_id, user)

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


def get_public_position_by_id(position_id: AnyStr):
    '''
    Get public position by id.
    '''
    # Get position by id
    position = PositionSchema.find_by_id(position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )

    # Get JD Data
    if not position.jd or position.jd == "":
        jd_instance = JDSchema().create_jd()
        # Update position
        position.update_jd(jd_instance.id)
    else:
        jd_instance = JDSchema.find_by_id(position.jd)
        if not jd_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="JD not found."
            )

    # Assign JD to position
    position.jd = jd_instance

    return position


def create_new_position(project_id: AnyStr, data: BaseModel, user: UserSchema):
    '''
    Create a new position.
    '''
    # Validate if user has access to the project
    project = _validate_permissions(project_id, user)

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
    # Validate if user has access to the project
    project = _validate_permissions(project_id, user)

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
    # Validate if user has access to the project
    project = _validate_permissions(project_id, user)

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
    # Validate if user has access to the project
    project = _validate_permissions(project_id, user)

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


def delete_positions_by_ids(position_ids: list[AnyStr]):
    # Iterate over all positions id
    for position_id in position_ids:
        # Find position by id
        position = PositionSchema.find_by_id(position_id)
        if position:
            # Delete position
            position.delete_position()
            # Delete vector database collection
            vector_db.delete_collection(position_id)
            # Delete JD by Id
            jd_instance = JDSchema.find_by_id(position.jd)
            if jd_instance:
                jd_instance.delete_jd()
            # Delete CVs by Ids
            delete_cvs_by_ids(position.cvs)


def delete_current_position(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    '''
    Delete current position.
    '''
    # Validate if user has access to the project
    project = _validate_permissions(project_id, user)

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

    # Delete postion from database
    position.delete_position()

    # Update position of project in database
    project.update_positions(position_id, is_add=False)

    # Delete vector database collection
    vector_db.delete_collection(position_id)

    # Delete JD by Id
    jd_instance = JDSchema.find_by_id(position.jd)
    if jd_instance:
        jd_instance.delete_jd()

    # Delete CVs by Ids
    delete_cvs_by_ids(position.cvs)
