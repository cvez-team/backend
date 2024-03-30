from typing import AnyStr, Dict
from pydantic import BaseModel, Field


class QuestionModel(BaseModel):
    content: str = Field("", title="Question Content")
    answer: str = Field("", title="Question Answer")
    level: int = Field(0, title="Question Level")


class QuestionSchema:
    '''
    Schema and Validation for Question.
    '''

    def __init__(
        self,
        content: AnyStr = "",
        answer: AnyStr = "",
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
