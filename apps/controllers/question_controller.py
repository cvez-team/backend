from typing import Any, Dict, List
from .extract_controller import extract_control
from ..providers.db_provider import DatabaseProvider
from ..providers.vectordb_provider import VectorDatabaseProvider
from ..utils.system_prompt import system_prompt_question
from ..utils.mock import default_fmt, question_fmt
import re

# Define the database and vector database provider
database = DatabaseProvider(collection_name="Questions")
vector_database = VectorDatabaseProvider(size=768)

def question_control(title: str, content: str, answer: str) -> Dict[str, Any]:
    '''
    question_control is a function that controls the creation of a new question.
    
    Args:
    - content (List[str]): The content of the questions.
    
    Returns:
    - question_data (dict): A dictionary containing the keywords extracted from the content.
    '''
    # Retrieve the raw text
    raw_text = "\n".join(content)
    # Remove invalid characters from the raw text (only allow alphanumeric characters and spaces)
    raw_text = re.sub(r"[^a-zA-Z0-9\s]", "", raw_text)
    
    # Fetch extract criterias
    criteria = default_fmt

    # Extract features from the raw text
    extraction, word_embeddings = extract_control(
        system_prompt=system_prompt_question, prompt=raw_text, fmt=criteria
    )
    # Create a dictionary for the question data
    question_data = {
        "extraction": extraction
    }
    
    # Upload the extraction to the database
    question_id = database.create(data=question_data)
    
    # Create a payload for the vector database
    payload = {
        "id": question_id
    }
    
    for key, value in word_embeddings.items():
        # Get collection name
        collection_name = f"question_{key}_cvez"    
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