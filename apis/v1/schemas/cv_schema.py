from typing import AnyStr, Dict
import enum
from pydantic import BaseModel, Field
from .score_schema import ScoreSchema, ScoreModel
from ..providers import cv_db
from ..providers import storage_db
from ..utils.utils import get_current_time


class CVStatus(enum.Enum):
    applying = "APPLYING"
    accepted = "ACCEPTED"
    rejected = "REJECTED"
    interviewing = "INTERVIEWING"
    hired = "HIRED"


class CVModel(BaseModel):
    id: str = Field(None, title="CV ID")
    name: str = Field("", title="CV Name")
    path: str = Field("", title="CV Path")
    url: str = Field("", title="CV URL")
    score: ScoreModel = Field({}, title="CV Score")
    extraction: dict = Field({}, title="CV Extraction")
    summary: str = Field("", title="CV Summary")
    content: str = Field("", title="CV Content")
    status: CVStatus = Field(CVStatus.applying, title="CV Status")
    upload_at: str = Field("", title="CV Upload At")


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
        content: AnyStr = "",
        status: CVStatus = CVStatus.applying,
        upload_at: AnyStr = get_current_time()
    ):
        self.id = cv_id
        self.name = name
        self.path = path
        self.url = url
        self.score = score
        self.extraction = extraction
        self.summary = summary
        self.content = content
        self.status = status
        self.upload_at = upload_at

    def to_dict(self, include_id=True):
        data_dict = {
            "name": self.name,
            "path": self.path,
            "url": self.url,
            "score": self.score.to_dict(),
            "extraction": self.extraction,
            "summary": self.summary,
            "content": self.content,
            "status": self.status.value,
            "upload_at": self.upload_at
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
            content=data.get("content"),
            status=CVStatus(data.get("status")),
            upload_at=data.get("upload_at")
        )

    @staticmethod
    def find_by_ids(cv_ids: list[AnyStr]):
        return [CVSchema.from_dict(cv) for cv in cv_db.get_all_by_ids(cv_ids)]

    @staticmethod
    def find_by_id(cv_id: AnyStr):
        data = cv_db.get_by_id(cv_id)
        if not data:
            return None
        return CVSchema.from_dict(data)

    def create_cv(self):
        cv_id = cv_db.create(self.to_dict(include_id=False))
        self.id = cv_id
        return self

    def update_path_url(self, path: AnyStr, url: AnyStr):
        self.path = path
        self.url = url
        cv_db.update(self.id, {
            "path": path,
            "url": url
        })

    def update_extraction(self, extraction: Dict[str, AnyStr]):
        self.extraction = extraction
        cv_db.update(self.id, {
            "extraction": extraction
        })

    def download_content(self):
        try:
            return storage_db.download(self.path)
        except Exception as e:
            return None

    def delete_cv(self):
        cv_db.delete(self.id)
        storage_db.remove(self.path)

    def update_score(self, score_data: Dict[str, AnyStr]):
        self.score.update_score(score_data)
        cv_db.update(self.id, {
            "score": self.score.to_dict()
        })

    def update_content(self, content: AnyStr):
        self.content = content
        cv_db.update(self.id, {
            "content": content
        })

    def update_summary(self, summary: AnyStr):
        self.summary = summary
        cv_db.update(self.id, {
            "summary": summary
        })

    def update_status(self, status: CVStatus):
        self.status = status
        cv_db.update(self.id, {
            "status": status.value
        })
