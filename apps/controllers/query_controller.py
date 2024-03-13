from typing import Any, Tuple, List
from ..providers.vectordb_provider import VectorDatabaseProvider
from ..utils.constants import WORD_EMBEDDING_DIM
from ..utils.mock import default_fmt

vector_database = VectorDatabaseProvider(size=WORD_EMBEDDING_DIM)
tag = {
    "cv": "cv",
    "jd": "jd",
    "questions": "questions"
}


def query_controller(tag: str, user_id: str, id_filebase: str, fmt=default_fmt) -> List[Tuple[str, Any, Any]]:
    '''
    Query the vector database based on a specific tag, user_id, id_filebase.
    Return a list of tuples containing the id, payload, and vector.
    '''
    key = fmt.keys()
    if tag not in tag:
        raise ValueError(f"Tag '{tag}' is not defined.")

    collection = f"{tag}_{key}_{user_id}"
    for collection_name in collection:
        query_results = vector_database.query(
            collection_name=collection_name, key='id', value=id_filebase)

    return query_results
