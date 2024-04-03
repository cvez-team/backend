from typing import AnyStr, List, Dict
from pydantic import BaseModel, Field


class JDModel(BaseModel):
    id: str = Field(None, title="JD ID")
    content: str = Field("", title="JD Content")
    extraction: dict = Field({}, title="JD Extraction")
    summary: str = Field("", title="JD Summary")
    requirements: list[str] = Field([], title="Requirements")


class JDSchema:
    '''
    Schema and Validation for JD.
    '''

    def __init__(
        self,
        jd_id: AnyStr = None,
        content: AnyStr = "",
        extraction: Dict[str, AnyStr] = {},
        summary: AnyStr = "",
        requirements: List[AnyStr] = [],
    ):
        self.id = jd_id
        self.content = content
        self.extraction = extraction
        self.summary = summary
        self.requirements = requirements

    def to_dict(self, include_id=True):
        data_dict = {
            "content": self.content,
            "extraction": self.extraction,
            "summary": self.summary,
            "requirements": self.requirements,
        }
        if include_id:
            data_dict["id"] = self.id
        return data_dict

    @staticmethod
    def from_dict(data: Dict):
        return JDSchema(
            jd_id=data.get("id"),
            content=data.get("content"),
            extraction=data.get("extraction"),
            summary=data.get("summary"),
            requirements=data.get("requirements"),
        )
