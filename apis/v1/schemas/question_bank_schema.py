from typing import AnyStr, List, Dict
from pydantic import BaseModel, Field
from .question_schema import QuestionSchema, QuestionModel
from ..providers import question_db


class QuestionBankModel(BaseModel):
    id: str = Field(None, title="Question Bank ID")
    name: str = Field("", title="Question Bank Name")
    summary: str = Field("", title="Question Bank Summary")
    questions: list[QuestionModel] = Field([], title="Questions")


class QuestionBankSchema:
    '''
    Schema and Validation for Question Bank.
    '''

    def __init__(
        self,
        question_bank_id: AnyStr = None,
        name: AnyStr = "",
        summary: AnyStr = "",
        questions: List[QuestionSchema] = [],
    ):
        self.id = question_bank_id
        self.name = name
        self.summary = summary
        self.questions = questions

    def to_dict(self, include_id=True):
        data_dict = {
            "name": self.name,
            "summary": self.summary,
            "questions": [question.to_dict() for question in self.questions],
        }
        if include_id:
            data_dict["id"] = self.id
        return data_dict

    @staticmethod
    def from_dict(data: Dict):
        return QuestionBankSchema(
            question_bank_id=data.get("id"),
            name=data.get("name"),
            summary=data.get("summary"),
            questions=[QuestionSchema.from_dict(
                question) for question in data.get("questions")],
        )

    @staticmethod
    def find_by_ids(question_bank_ids: List[AnyStr]):
        banks = question_db.get_all_by_ids(question_bank_ids)
        return [QuestionBankSchema.from_dict(bank) for bank in banks]

    @staticmethod
    def find_by_id(question_bank_id: AnyStr):
        data = question_db.get_by_id(question_bank_id)
        if data:
            return QuestionBankSchema.from_dict(data)
        return None

    def create_question_bank(self):
        question_bank_id = question_db.create(self.to_dict(include_id=False))
        self.id = question_bank_id
        return self

    def update_bank(self, data: Dict):
        question_db.update(self.id, data)

    def delete_question_bank(self):
        question_db.delete(self.id)
