from typing import AnyStr, List
import time
from fastapi import HTTPException, status
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from ..schemas.criteria_schema import CriteriaSchema
from ..configs.llm_config import gpt_model, gemini_model
from ..utils.utils import create_pydantic_object
from ..utils.prompt import prompt_template
from ..utils.constants import DEFAULT_LLM_PROVIDER
from ..utils.logger import log_llm


class LLMGenerator:
    '''
    Wrapper module for LLM Chain.
    '''

    def __init__(self, chain):
        self.chain = chain

    def generate(self, system: AnyStr, prompt: AnyStr):
        try:
            _s = time.perf_counter()
            answer = self.chain.invoke({
                "system": system,
                "prompt": prompt
            })
            _e = time.perf_counter() - _s

            log_llm(f"{answer} [{_e:.2f}s]")

            return answer

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Large Language Model Error: {str(e)}"
            )


class LLMProvider:
    '''
    Provide common methods for LLM text generation.
    '''

    def __init__(self):
        self.providers = {
            "gpt": gpt_model,
            "gemini": gemini_model
        }

    def construct(self, criterias: List[CriteriaSchema], provider: AnyStr = DEFAULT_LLM_PROVIDER):
        # Create output parser
        parser = JsonOutputParser(
            pydantic_object=create_pydantic_object(criterias))

        # Define template for prompt
        template = PromptTemplate(
            template=prompt_template,
            input_variables=["system", "prompt"],
            partial_variables={
                "instruction": parser.get_format_instructions()
            }
        )

        # Get the model
        model = self.providers.get(
            provider, self.providers[DEFAULT_LLM_PROVIDER])

        # Create the chain
        chain = template | model | parser

        return LLMGenerator(chain=chain)
