from typing import Any, Dict
import re
from plugins.typing import LLMFmt
from .extract_controller import extract_control
from ..models.question_model import QuestionModel
from ..providers.db_provider import DatabaseProvider
from ..providers.vectordb_provider import VectorDatabaseProvider
from ..utils.system_prompt import system_prompt_question
from ..utils.constants import WORD_EMBEDDING_DIM, QUESTION_COLLECTION
from ..utils.mock import default_fmt

# Define the database and vector database provider
database = DatabaseProvider(collection_name=QUESTION_COLLECTION)
vector_database = VectorDatabaseProvider(size=WORD_EMBEDDING_DIM)


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
    # Retrieve the raw text
    raw_text = "\n".join(content)
    # Remove invalid characters from the raw text (only allow alphanumeric characters and spaces)
    raw_text = re.sub(r"[^a-zA-Z0-9\s]", "", raw_text)

    # Extract features from the raw text
    extraction, word_embeddings = extract_control(
        system_prompt=system_prompt_question, prompt=raw_text, fmt=fmt
    )
    # Create a dictionary for the question data
    question_data = QuestionModel(
        title=title,
        content=content,
        answer=answer,
        extraction=extraction
    ).to_dict()

    # Upload the extraction to the database
    question_id = database.create(data=question_data)

    # Create a payload for the vector database
    payload = {
        "id": question_id
    }

    for key, value in word_embeddings.items():
        # Get collection name
        collection_name = f"question_{key}_{user_id}"
        # If value is a list
        if isinstance(value, list):
            for item in value:
                vector_database.insert(
                    collection_name=collection_name, array=item, data=payload)

        elif isinstance(value, dict):
            for k, v in value.items():
                vector_database.insert(
                    collection_name=collection_name, array=v, data=payload)
        else:
            vector_database.insert(
                collection_name=collection_name, array=value, data=payload)
    return question_data
