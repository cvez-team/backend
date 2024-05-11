from pydantic import BaseModel, Field
from ..schemas.question_bank_schema import QuestionBankModel
from ..schemas.question_schema import QuestionModel


class QuestionBanksResponseInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: list[QuestionBankModel] = Field(...,
                                          description="Question bank data")


class QuestionBankResponseInterface(BaseModel):
    msg: str = Field(..., description="Message response")
    data: QuestionBankModel = Field(None, description="Question bank data")


class CreateQuestionInterface(BaseModel):
    name: str = Field(..., description="Question Bank Name")
    questions: list[QuestionModel] = Field([], description="Questions")


class UpdateQuestionInterface(BaseModel):
    name: str = Field("", description="Question Bank Name")
    questions: list[QuestionModel] = Field([], description="Questions")
