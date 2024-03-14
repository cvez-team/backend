from typing import Dict, List, Tuple
import numpy.typing as npt
from plugins.typing import LLMFmt
from ..providers.vectordb_provider import VectorDatabaseProvider
from .query_controller import query_control
from ..utils.constants import WORD_EMBEDDING_DIM

vector_database = VectorDatabaseProvider(size=WORD_EMBEDDING_DIM)


def calculate_average_scores(scores: Dict[str, List[List[Tuple[str, float]]]], fmt: LLMFmt) -> Dict[str, List[Tuple[str, float]]]:
    average_scores = {}
    _average_scores = {}
    _average_scores_count = {}

    for key, values in scores.items():
        for value in values:
            for _id, score in value:
                if _id not in _average_scores:
                    _average_scores[_id] = score
                    _average_scores_count[_id] = 1
                else:
                    _average_scores[_id] += score
                    _average_scores_count[_id] += 1
        # Save the average score for each id
        for _id in _average_scores:
            if _id not in average_scores:
                average_scores[_id] = _average_scores[_id] / \
                    _average_scores_count[_id] * fmt[key]["weight"]
            else:
                average_scores[_id] += _average_scores[_id] / \
                    _average_scores_count[_id] * fmt[key]["weight"]
        # Reset the count
        _average_scores_count = {}
        _average_scores = {}

    # Return the average scores if there are no scores
    if len(average_scores) == 0:
        return average_scores

    # Get the deviation of the scores
    deviation = 0
    for key, _fmt in fmt.items():
        deviation += _fmt.get("weight", 0)

    # Normalize the scores
    for _id in average_scores:
        average_scores[_id] = average_scores[_id] / deviation

    return average_scores


def find_match(collection_name: str, query_vector: npt.NDArray, limit: int = 100) -> List[Tuple[str, float]]:
    try:
        match_result = vector_database.search(
            collection_name, query_vector, limit)
        # Chuyển đổi match_result thành một list các tuples
        return [(item[2]['id'], item[1]) for item in match_result]
    except Exception as e:
        return []


def match_cv_control(jd_id: str, user_id: str, fmt: LLMFmt):
    # Query point that contains the JD ID
    vectors = query_control(tag="jd", user_id=user_id,
                            firebase_id=jd_id, fmt=fmt)

    # Find matched CVs
    match_results = {}
    for key, values in vectors.items():
        match_tuples = []
        collection_name = f"cv_{key}_{user_id}"

        for value in values:
            match_tuple = find_match(
                collection_name=collection_name, query_vector=value)
            match_tuples.append(match_tuple)

        match_results[key] = match_tuples

    return calculate_average_scores(match_results, fmt)


def match_question_control(cv_id: str, user_id: str, fmt: LLMFmt):
    # Query point that contains the JD ID
    vectors = query_control(tag="cv", user_id=user_id,
                            firebase_id=cv_id, fmt=fmt)

    # Find matched CVs
    match_results = {}
    for key, values in vectors.items():
        match_tuples = []
        collection_name = f"question_{key}_{user_id}"

        for value in values:
            match_tuple = find_match(
                collection_name=collection_name, query_vector=value)
            match_tuples.append(match_tuple)

        match_results[key] = match_tuples

    return calculate_average_scores(match_results, fmt)
