from typing import AnyStr, List, Dict
from pydantic import BaseModel, Field
from .score_schema import ScoreSchema, ScoreModel


class CVModel(BaseModel):
    id: str = Field(None, title="CV ID")
    name: str = Field("", title="CV Name")
    path: str = Field("", title="CV Path")
    url: str = Field("", title="CV URL")
    score: ScoreModel = Field({}, title="CV Score")
    extraction: dict = Field({}, title="CV Extraction")
    summary: str = Field("", title="CV Summary")
    fulfillments: list[str] = Field([], title="Fulfillments")


class CVSchema:
    '''
    Schema and Validation for CV.
    '''

    def __init__(
        self,
        cv_id: AnyStr = None,
        name: AnyStr = "",
        path: AnyStr = "",
        url: AnyStr = "",
        score: ScoreSchema = ScoreSchema(),
        extraction: Dict[str, AnyStr] = {},
        summary: AnyStr = "",
        fulfillments: List[AnyStr] = [],
    ):
        self.id = cv_id
        self.name = name
        self.path = path
        self.url = url
        self.score = score
        self.extraction = extraction
        self.summary = summary
        self.fulfillments = fulfillments

    def to_dict(self, include_id=True):
        data_dict = {
            "name": self.name,
            "path": self.path,
            "url": self.url,
            "score": self.score.to_dict(),
            "extraction": self.extraction,
            "summary": self.summary,
            "fulfillments": self.fulfillments,
        }
        if include_id:
            data_dict["id"] = self.id
        return data_dict

    @staticmethod
    def from_dict(data: Dict):
        return CVSchema(
            cv_id=data.get("id"),
            name=data.get("name"),
            path=data.get("path"),
            url=data.get("url"),
            score=ScoreSchema.from_dict(data.get("score")),
            extraction=data.get("extraction"),
            summary=data.get("summary"),
            fulfillments=data.get("fulfillments"),
        )
