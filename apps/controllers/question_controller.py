from typing import Any, Dict
import re
from plugins.typing import LLMFmt
from .extract_controller import extract_control
from .upload_vector_controller import upload_vector_control
from ..models.question_model import QuestionModel
from ..providers.db_provider import DatabaseProvider
from ..utils.system_prompt import system_prompt_question
from ..utils.constants import QUESTION_COLLECTION

# Define the database and vector database provider
database = DatabaseProvider(collection_name=QUESTION_COLLECTION)


def question_control(title: str, content: str, answer: str, user_id: str, fmt: LLMFmt) -> Dict[str, Any]:
    '''
    question_control is a function that controls the creation of a new question.

    Args:
    - title (str): The title of the question.
    - content (str): The content of the questions.
    - answer (str): The answer to the question.

    Returns:
    - question_data (dict): A dictionary containing the keywords extracted from the content.
    '''
    
    # Extract features from the raw text
    extraction, word_embeddings = extract_control(
        system_prompt=system_prompt_question, prompt=content, fmt=fmt
    )

    try:
        # Create a dictionary for the question data
        question_data = QuestionModel(
            title=title,
            content=content,
            answer=answer,
            extraction=extraction
        ).to_dict()

        # Upload the extraction to the database
        question_id = database.create(data=question_data)
        question_data["id"] = question_id

        # Create a payload for the vector database
        upload_vector_control(extraction=extraction, word_embeddings=word_embeddings,
                            tag="question", user_id=user_id, firebase_id=question_id)

    except Exception as e:
        question_data = {
            "error": str(e)
        }
    
    return question_data