from typing import Any, Dict
import re
from plugins.typing import LLMFmt
from .extract_controller import extract_control
from .upload_vector_controller import upload_vector_control
from ..models.question_model import QuestionModel
from ..providers.db_provider import DatabaseProvider
from ..utils.system_prompt import system_prompt_question
<<<<<<< HEAD
from ..utils.constants import WORD_EMBEDDING_DIM, QUESTION_COLLECTION
from ..utils.mock import question_fmt
=======
from ..utils.constants import QUESTION_COLLECTION

>>>>>>> 5a768e8eab427d344af00c173fd762081f580cfc

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
<<<<<<< HEAD
    # Retrieve the raw text
    raw_text = title + " \n" + content + " \n" + answer
    # Remove invalid characters from the raw text (only allow alphanumeric characters and spaces)
    raw_text = re.sub(r"[^a-zA-Z0-9\s]", "", raw_text)

    # Fetch extract criterias
    criteria = question_fmt
=======
    # Remove invalid characters from the raw text (only allow alphanumeric characters and spaces)
    raw_text = re.sub(r"[^a-zA-Z0-9\s]", "", content)
>>>>>>> 5a768e8eab427d344af00c173fd762081f580cfc

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
    question_data["id"] = question_id

    # Create a payload for the vector database
<<<<<<< HEAD
    payload = {
        "id": question_id,
        "summary": extraction["Summary"]
    }
=======
    upload_vector_control(extraction=extraction, word_embeddings=word_embeddings,
                          tag="question", user_id=user_id, firebase_id=question_id)
>>>>>>> 5a768e8eab427d344af00c173fd762081f580cfc

    return question_data
