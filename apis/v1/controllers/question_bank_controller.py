from typing import AnyStr
from pydantic import BaseModel
from fastapi import HTTPException, status
from ..schemas.user_schema import UserSchema
from ..schemas.project_schema import ProjectSchema
from ..schemas.position_schema import PositionSchema
from ..schemas.question_bank_schema import QuestionBankSchema


def _validate_permissions(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    # Validate project id in user's projects
    if project_id not in user.projects and project_id not in user.shared:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this project."
        )

    # Get project
    project = ProjectSchema.find_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )

    # Validate position id in project's positions
    if position_id not in project.positions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this position."
        )

    # Get position
    position = PositionSchema.find_by_id(position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )

    return project, position


def get_all_question_banks(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    # Validate permissions
    _, position = _validate_permissions(project_id, position_id, user)

    question_banks = QuestionBankSchema.find_by_ids(position.question_banks)

    return question_banks


def get_current_question_bank(project_id: AnyStr, position_id: AnyStr, question_bank_id: AnyStr, user: UserSchema):
    # Validate permissions
    _, position = _validate_permissions(project_id, position_id, user)

    if question_bank_id not in position.question_banks:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this question bank."
        )

    # Get question bank by id
    question_bank = QuestionBankSchema.find_by_id(question_bank_id)
    if not question_bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question Bank not found."
        )

    return question_bank


def create_new_question_bank(project_id: AnyStr, position_id: AnyStr, data: BaseModel, user: UserSchema):
    # Validate permissions
    _, position = _validate_permissions(project_id, position_id, user)

    # Create new question bank
    question_bank = QuestionBankSchema(
        name=data.name,
        questions=data.questions
    ).create_question_bank()

    # Add question bank to position
    position.update_question_bank(question_bank.id)

    return question_bank


def update_current_question_bank(project_id: AnyStr, position_id: AnyStr, question_id: AnyStr, data: BaseModel, user: UserSchema):
    # Validate permissions
    _, position = _validate_permissions(project_id, position_id, user)

    if question_id not in position.question_banks:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this question bank."
        )

    # Update question bank
    question_bank = QuestionBankSchema.find_by_id(question_id)
    if not question_bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question Bank not found."
        )

    question_bank.update_bank(data.model_dump(exclude_defaults=True))


def delete_current_question_bank(project_id: AnyStr, position_id: AnyStr, question_id: AnyStr, user: UserSchema):
    # Validate permissions
    _, position = _validate_permissions(project_id, position_id, user)

    if question_id not in position.question_banks:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this question bank."
        )

    # Delete question bank
    question_bank = QuestionBankSchema.find_by_id(question_id)
    if not question_bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question Bank not found."
        )

    # Delete question bank from position
    position.update_question_bank(question_id, is_add=False)

    question_bank.delete_question_bank()
