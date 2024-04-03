from typing import Dict
from pydantic import BaseModel, Field


class _MatchesResponseInterface(BaseModel):
    overall: int = Field(..., description="Match overall score")
    criteria: Dict[str, int] = Field(...,
                                     description="Match score in criteria")


class MatchesResponseInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: Dict[str,
               _MatchesResponseInterface] = Field(..., description="Matches data")
