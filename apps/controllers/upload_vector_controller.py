from typing import Dict, List, Union, Any
import numpy.typing as npt
from ..providers.vectordb_provider import VectorDatabaseProvider
from ..utils.constants import WORD_EMBEDDING_DIM


vector_database = VectorDatabaseProvider(size=WORD_EMBEDDING_DIM)


def __get_payload(firebase_id: str, content: str):
    return {
        "id": firebase_id,
        "content": content
    }


def upload_vector_control(
    extraction: Dict[str, Any],
    word_embeddings: Dict[str, Union[List[npt.NDArray], npt.NDArray]],
    tag: str,
    user_id: str,
    firebase_id: str
):
    for key, value in word_embeddings.items():
        # Get collection name
        collection_name = f"{tag}_{key}_{user_id}"
        # If value is a list
        if isinstance(value, list):
            for i, item in enumerate(value):
                vector_database.insert(
                    collection_name=collection_name, array=item, data=__get_payload(firebase_id, extraction[key][i]))

        # If value is a dictionary
        elif isinstance(value, dict):
            for k, v in value.items():
                vector_database.insert(
                    collection_name=collection_name, array=v, data=__get_payload(firebase_id, extraction[key][k]))

        # If value is a numpy array
        elif isinstance(value, str):
            vector_database.insert(
                collection_name=collection_name, array=value, data=__get_payload(firebase_id, value))

        # Continue if value is not a list, dictionary, or numpy array
        else:
            continue
