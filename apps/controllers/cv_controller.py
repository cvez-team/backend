from typing import Any, Dict
from .extract_controller import extract_control
from ..providers.db_provider import DatabaseProvider
from ..providers.vectordb_provider import VectorDatabaseProvider
from ..utils.system_prompt import system_prompt_cv
from ..utils.mock import default_fmt


# Define the database and vector database provider
database = DatabaseProvider(collection_name="CVs")
vector_database = VectorDatabaseProvider(size=96)


def cv_control(file: bytes, filename: str, user_id: str) -> Dict[str, Any]:
    '''
    Extract the data from the CV file, and upload to the database.
    '''
    # Load bytes as a files with filename

    # Upload file to Firebase storage

    # Convert the file to raw text
    raw_text = filename

    # Fetch extract criterias
    criteria = default_fmt

    # Extract features from the raw text
    extraction, word_embeddings = extract_control(
        system_prompt=system_prompt_cv, prompt=raw_text, fmt=criteria
    )

    # Format data to upload
    cv_data = {
        "extraction": extraction,
    }

    # Upload the extraction to the database
    # data_id = database.create(data=cv_data)

    # Upload vector to the database
    payload = {
        "id": "test_id",
    }
    for key, value in word_embeddings.items():
        # Get collection name
        collection_name = f"cv_{key}_{user_id}"
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

    return cv_data
