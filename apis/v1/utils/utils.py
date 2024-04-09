from typing import List
import datetime
from fastapi import HTTPException, status
from langchain.pydantic_v1 import Field, create_model
from ..schemas.criteria_schema import CriteriaSchema
from ..utils.constants import ALLOWED_EXTENSIONS


def get_current_time() -> str:
    '''
    Get the current time in the string format.
    '''
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_pydantic_object(criterias: List[CriteriaSchema]):
    formated_dict = {}

    for criteria in criterias:
        description = f"Extract keywords and the responding score of {criteria.name}. Eg: {criteria.example}. This field can be empty. This field is a dictionary contains a string as key a number as value, not any other types."
        field_value = Field(..., description=description)
        formated_dict[criteria.name] = (dict[str, int], field_value)

    return create_model("Criteria", **formated_dict)


def validate_file_extension(file_name: str, allowed_extensions: List[str] = ALLOWED_EXTENSIONS):
    '''
    Validate the file extension.
    '''
    if not file_name.lower().endswith(tuple(allowed_extensions)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File extension not allowed. Allowed extensions are {', '.join(allowed_extensions)}"
        )
