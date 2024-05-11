from typing import Dict
from pydantic import BaseModel, Field


class ScoreModel(BaseModel):
    overall: float = Field(None, title="Overall Score")


class ScoreSchema:
    def __init__(
        self,
        overall: float = None,
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

    def update_score(self, score_data: Dict[str, float]):
        self.overall = score_data["overall"]
        for key, value in score_data["criteria"].items():
            setattr(self, key, value)
