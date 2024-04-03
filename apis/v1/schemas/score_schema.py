from typing import Dict
from pydantic import BaseModel, Field


class ScoreModel(BaseModel):
    overall: float = Field(0.0, title="Overall Score")


class ScoreSchema:
    def __init__(
        self,
        overall: float = 0.0,
        **kwargs,
    ):
        self.overall = overall
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        data_dict = {}
        for key, value in self.__dict__.items():
            data_dict[key] = value
        return data_dict

    @staticmethod
    def from_dict(data: Dict):
        return ScoreSchema(**data)
