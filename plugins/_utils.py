from langchain.pydantic_v1 import Field
from ._interface import LLMFmt, PydanticFmt


prompt_template = '''
Answer the query using the given information only. Do not rely on your basic knowledge. The details given might be out of sequence or incomplete.
{system}

{instruction}

Here is the information you need to answer the query:
{prompt}
'''


def get_type_by_type_literal(type_literal: str) -> type:
    if type_literal == "string":
        return str
    elif type_literal == "integer":
        return int
    elif type_literal == "float":
        return float
    elif type_literal == "boolean":
        return bool
    elif type_literal == "list":
        return list
    elif type_literal == "dictionary":
        return dict
    else:
        raise ValueError(f"Unknown type literal: {type_literal}")


def create_pydantic_dict(fmt: LLMFmt) -> PydanticFmt:
    formated_dict: PydanticFmt = {}

    # Add fields to the dictionary
    for key, value in fmt.items():
        field_type = get_type_by_type_literal(value['type'])
        field_value = Field(..., description=value['description'])
        formated_dict[key] = (field_type, field_value)

    return formated_dict
