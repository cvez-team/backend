from typing import Dict, List
import datetime
from langchain.pydantic_v1 import Field, create_model
from ..schemas.criteria_schema import CriteriaSchema


def get_current_time() -> str:
    '''
    Get the current time in the string format.
    '''
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_pydantic_object(criterias: List[CriteriaSchema]):
    formated_dict = {}

    for criteria in criterias:
        description = f"Extracting keywords of {criteria.name} from the provided content. Example: {criteria.example}. This field only accept a list of string, not dictionary or any other types."
        field_value = Field(..., description=description)
        formated_dict[criteria.name] = (List, field_value)

    return create_model("Criteria", **formated_dict)
