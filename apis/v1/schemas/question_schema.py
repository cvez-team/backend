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
    level: int = Field(0, title="Question Level")


class QuestionSchema:
    '''
    Schema and Validation for Question.
    '''

    def __init__(
        self,
        content: AnyStr = "",
        answer: Dict[str, str] = {},
        level: int = 0,
    ):
        self.content = content
        self.answer = answer
        self.level = level

    def to_dict(self):
        return {
            "content": self.content,
            "answer": self.answer,
            "level": self.level,
        }

    @staticmethod
    def from_dict(data: Dict):
        return QuestionSchema(
            content=data.get("content"),
            answer=data.get("answer"),
            level=data.get("level"),
        )
