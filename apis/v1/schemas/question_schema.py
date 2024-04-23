from typing import AnyStr, Dict
from pydantic import BaseModel, Field


class _QuestionAnswerModel(BaseModel):
    a: str = Field("", title="Answer A")
    b: str = Field("", title="Answer B")
    c: str = Field("", title="Answer C")
    d: str = Field("", title="Answer D")


class QuestionModel(BaseModel):
    content: str = Field("", title="Question Content")
    answer: _QuestionAnswerModel = Field("", title="Question Answer")
    correct_answer: list[int] = Field([], title="Correct Answer")


class QuestionSchema:
    '''
    Schema and Validation for Question.
    '''

    def __init__(
        self,
        content: AnyStr = "",
        answer: Dict[str, str] = {},
        correct_answer: list[int] = [],
    ):
        self.content = content
        self.answer = answer
        self.correct_answer = correct_answer

    def to_dict(self):
        return {
            "content": self.content,
            "answer": self.answer,
            "correct_answer": self.correct_answer,
        }

    @staticmethod
    def from_dict(data: Dict):
        return QuestionSchema(
            content=data.get("content"),
            answer=data.get("answer"),
            correct_answer=data.get("correct_answer"),
        )
