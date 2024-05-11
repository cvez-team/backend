from typing import AnyStr, Dict
from pydantic import BaseModel, Field


class CriteriaModel(BaseModel):
    name: AnyStr = Field("", title="Criteria Name")
    example: AnyStr = Field("", title="Criteria Example")
    score: int = Field(None, title="Criteria Score")


class CriteriaSchema:
    '''
    Schema and Validation for Criteria.
    '''

    def __init__(
        self,
        name: AnyStr = "",
        example: AnyStr = "",
        score: int = None,
    ):
        self.name = name
        self.example = example
        self.score = score

    def to_dict(self):
        return {
            "name": self.name,
            "example": self.example,
            "score": self.score,
        }

    @staticmethod
    def from_dict(data: Dict):
        return CriteriaSchema(
            name=data.get("name"),
            example=data.get("example"),
            score=data.get("score"),
        )
