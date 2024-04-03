from pydantic import BaseModel, Field
from ..schemas.question_bank_schema import QuestionBankModel


class QuestionBanksResponseInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: list[QuestionBankModel] = Field(...,
                                          description="Question bank data")


class QuestionBankResponseInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: QuestionBankModel = Field(None, description="Question bank data")
