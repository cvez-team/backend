from typing import AnyStr
from ..schemas.user_schema import UserSchema
from ..schemas.question_bank_schema import QuestionBankSchema


def get_all_question_banks(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    return [QuestionBankSchema()]


def get_current_question_bank(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    return QuestionBankSchema()


def create_new_question_bank(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    return QuestionBankSchema()


def update_current_question_bank(project_id: AnyStr, position_id: AnyStr, question_id: AnyStr, user: UserSchema):
    return None


def delete_current_question_bank(project_id: AnyStr, position_id: AnyStr, question_id: AnyStr, user: UserSchema):
    return None
