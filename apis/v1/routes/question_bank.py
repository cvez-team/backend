from typing import Annotated
from fastapi import APIRouter, Depends
from ..interfaces.question_bank_interface import (
    QuestionBankResponseInterface,
    QuestionBanksResponseInterface,
    CreateQuestionInterface,
    UpdateQuestionInterface
)
from ..schemas.user_schema import UserSchema
from ..middlewares.auth_middleware import get_current_user
from ..controllers.question_bank_controller import (
    get_all_question_banks,
    get_current_question_bank,
    create_new_question_bank,
    update_current_question_bank,
    delete_current_question_bank
)
from ..utils.response_fmt import jsonResponseFmt


router = APIRouter(prefix="/question_bank", tags=["QuestionBank"])


@router.get("/{project_id}/{position_id}", response_model=QuestionBanksResponseInterface)
async def get_question_banks(project_id: str, position_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    question_banks = get_all_question_banks(project_id, position_id, user)
    return jsonResponseFmt([question_bank.to_dict() for question_bank in question_banks])


@router.get("/{project_id}/{position_id}/{question_bank_id}", response_model=QuestionBankResponseInterface)
async def get_question_bank(project_id: str, position_id: str, question_bank_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    question_bank = get_current_question_bank(
        project_id, position_id, question_bank_id, user)
    return jsonResponseFmt(question_bank.to_dict())


@router.post("/{project_id}/{position_id}", response_model=QuestionBankResponseInterface)
async def create_question_bank(project_id: str, position_id: str, data: CreateQuestionInterface, user: Annotated[UserSchema, Depends(get_current_user)]):
    question_bank = create_new_question_bank(
        project_id, position_id, data, user)
    return jsonResponseFmt(question_bank.to_dict())


@router.put("/{project_id}/{position_id}/{question_bank_id}", response_model=QuestionBankResponseInterface)
async def update_question_bank(project_id: str, position_id: str, question_id: str, data: UpdateQuestionInterface, user: Annotated[UserSchema, Depends(get_current_user)]):
    update_current_question_bank(
        project_id, position_id, question_id, data, user)
    return jsonResponseFmt(None, f"Question Bank with ID {question_id} has been updated successfully.")


@router.delete("/{project_id}/{position_id}/{question_bank_id}", response_model=QuestionBankResponseInterface)
async def delete_question(project_id: str, position_id: str, question_bank_id: str, user: Annotated[UserSchema, Depends(get_current_user)]):
    delete_current_question_bank(
        project_id, position_id, question_bank_id, user)
    return jsonResponseFmt(None, f"Question Bank with ID {question_bank_id} has been deleted successfully.")
