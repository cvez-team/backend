from typing import AnyStr
from ..schemas.user_schema import UserSchema


def get_all_matches_cv(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    return {
        "1": {
            "overall": 100,
            "criteria": {
                "Education": 100,
                "Experience": 100,
                "Skill": 100
            }
        }
    }


def get_all_matches_question(project_id: AnyStr, position_id: AnyStr, cv_id: AnyStr, user: UserSchema):
    return {
        "1": {
            "overall": 100,
            "criteria": {
                "Education": 100,
                "Experience": 100,
                "Skill": 100
            }
        }
    }
