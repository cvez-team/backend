from typing import AnyStr, List, Dict
from pydantic import BaseModel, Field
from ..providers import jd_db


class JDModel(BaseModel):
    id: str = Field(None, title="JD ID")
    content: str = Field("", title="JD Content")
    extraction: dict = Field({}, title="JD Extraction")


class JDSchema:
    '''
    Schema and Validation for JD.
    '''

    def __init__(
        self,
        jd_id: AnyStr = None,
        content: AnyStr = "",
        extraction: Dict[str, AnyStr] = {}
    ):
        self.id = jd_id
        self.content = content
        self.extraction = extraction

    def to_dict(self, include_id=True):
        data_dict = {
            "content": self.content,
            "extraction": self.extraction
        }
        if include_id:
            data_dict["id"] = self.id
        return data_dict

    @staticmethod
    def from_dict(data: Dict):
        return JDSchema(
            jd_id=data.get("id"),
            content=data.get("content"),
            extraction=data.get("extraction")
        )

    @staticmethod
    def find_by_id(jd_id: AnyStr):
        jd = jd_db.get_by_id(jd_id)
        if not jd:
            return None
        return JDSchema.from_dict(jd)

    def create_jd(self):
        jd_id = jd_db.create(self.to_dict(include_id=False))
        self.id = jd_id
        return self

    def update_extraction(self, extraction: Dict[str, AnyStr]):
        self.extraction = extraction
        jd_db.update(self.id, {
            "extraction": extraction
        })

    def update_content(self, content: AnyStr):
        self.content = content
        jd_db.update(self.id, {
            "content": content
        })
