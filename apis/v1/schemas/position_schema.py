from typing import AnyStr, List, Dict
from pydantic import BaseModel, Field
from .criteria_schema import CriteriaSchema, CriteriaModel
from ..providers import position_db
from ..utils.utils import get_current_time


class PositionModel(BaseModel):
    id: str = Field(None, title="Position ID")
    name: str = Field("", title="Position Name")
    description: str = Field("", title="Position Description")
    alias: str = Field("", title="Position Alias")
    is_closed: bool = Field(False, title="Position is Closed")
    start_date: str = Field(get_current_time(), title="Position Start Date")
    end_date: str = Field(None, title="Position End Date")
    cvs: list[str] = Field([], title="CVs")
    jd: str = Field("", title="Job Description")
    question_banks: list[str] = Field([], title="Question Banks")
    criterias: list[CriteriaModel] = Field([], title="Criterias")
    re_analyzing: bool = Field(False, title="Re-analyzing")


class PositionSchema:
    '''
    Schema and Validation for Position.
    '''

    def __init__(
        self,
        position_id: AnyStr = None,
        name: AnyStr = "",
        description: AnyStr = "",
        alias: AnyStr = "",
        is_closed: bool = False,
        start_date: AnyStr = get_current_time(),
        end_date: AnyStr = None,
        cvs: List[AnyStr] = [],
        jd: AnyStr = "",
        question_banks: List[AnyStr] = [],
        criterias: List[CriteriaSchema] = [],
        re_analyzing: bool = False,
    ):
        self.id = position_id
        self.name = name
        self.description = description
        self.alias = alias
        self.is_closed = is_closed
        self.start_date = start_date
        self.end_date = end_date
        self.cvs = cvs
        self.jd = jd
        self.question_banks = question_banks
        self.criterias = criterias
        self.re_analyzing = re_analyzing

    def to_dict(self, include_id=True):
        data_dict = {
            "name": self.name,
            "description": self.description,
            "alias": self.alias,
            "is_closed": self.is_closed,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "cvs": self.cvs,
            "jd": self.jd,
            "question_banks": self.question_banks,
            "criterias": [criteria.to_dict() for criteria in self.criterias],
            "re_analyzing": self.re_analyzing,
        }
        if include_id:
            data_dict["id"] = self.id
        return data_dict

    @staticmethod
    def from_dict(data: Dict):
        return PositionSchema(
            position_id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            alias=data.get("alias"),
            is_closed=data.get("is_closed"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            cvs=data.get("cvs"),
            jd=data.get("jd"),
            question_banks=data.get("question_banks"),
            criterias=[CriteriaSchema.from_dict(
                criteria) for criteria in data.get("criterias")],
            re_analyzing=data.get("re_analyzing"),
        )

    @staticmethod
    def find_all_by_ids(position_ids: List[AnyStr]):
        '''
        Find all positions by list of position ids.
        '''
        positions = position_db.get_all_by_ids(position_ids)
        return [PositionSchema.from_dict(position) for position in positions]
