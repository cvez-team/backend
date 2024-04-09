from typing import AnyStr, List, Dict
from pydantic import BaseModel, Field
from .question_schema import QuestionSchema, QuestionModel


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
