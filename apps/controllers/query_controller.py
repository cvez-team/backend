from typing import Dict
import numpy.typing as npt
from ..providers.vectordb_provider import VectorDatabaseProvider
from ..utils.constants import WORD_EMBEDDING_DIM
from plugins.typing import LLMFmt

vector_database = VectorDatabaseProvider(size=WORD_EMBEDDING_DIM)


def query_control(tag: str, user_id: str, firebase_id: str, fmt: LLMFmt) -> Dict[str, npt.NDArray]:
    '''
    Query the vector database based on a specific tag, user_id, firebase_id.
    Return a list of tuples containing the id, payload, and vector.
    '''
    query_results = {}
    for key in fmt.keys():
        collection_name = f"{tag}_{key}_{user_id}"
        try:
            query_result = vector_database.query(
                collection_name=collection_name, key='id', value=firebase_id)
            query_results[key] = [item[2] for item in query_result]
        except Exception as e:
            query_results[key] = []

    return query_results
