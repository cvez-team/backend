from typing import Dict, List, Tuple
import numpy.typing as npt
import numpy as np
from plugins.typing import LLMFmt
from ..providers.vectordb_provider import VectorDatabaseProvider
from .query_controller import query_control
from ..utils.constants import WORD_EMBEDDING_DIM

vector_database = VectorDatabaseProvider(size=WORD_EMBEDDING_DIM)


def calculate_average_scores(scores: Dict[str, List[List[Tuple[str, float]]]], fmt: LLMFmt):
    average_scores = {}

    # Iterate over criteria
    for key, values in scores.items():
        # Add the criteria to the average_scores dictionary
        average_scores[key] = {}

        # If there are no scores, skip the criteria
        if len(values) == 0:
            continue
        if len(values[0]) == 0:
            continue

        # Convert values to numpy array. The value must have shape: (n, m, 2)
        # where n is the number of attribute in the criteria, m is the number of
        # vectors on that attribute, and 2 is the shape of the tuple
        scores_array = np.array(values)

        # Extract the id part of the tuple
        ids_plane = scores_array[:, :, 0]
        scores_plane = scores_array[:, :, 1]

        # Find all unique ids
        unique_ids = np.unique(ids_plane)

        # Iterate over unique ids
        for _id in unique_ids:
            # Find the indices of the id
            indices = np.where(ids_plane == _id)

            # Get the scores of the id
            _scores = scores_plane[indices].astype(np.float32)

            # Calculate the average score
            average_score = np.mean(_scores)

            # Add the average score to the average_scores dictionary
            if _id in average_scores[key]:
                average_scores[key][_id] += average_score
            else:
                average_scores[key][_id] = average_score

    # Format the average_scores dictionary
    fmt_average_scores = {}
    fmt_average_scores_deviation = {}

    # Iterate over the average_scores dictionary
    for key, values in average_scores.items():
        for _id, score in values.items():
            if _id in fmt_average_scores:
                fmt_average_scores[_id] += score * fmt[key]["weight"]
                fmt_average_scores_deviation[_id] += fmt[key]["weight"]
            else:
                fmt_average_scores[_id] = score * fmt[key]["weight"]
                fmt_average_scores_deviation[_id] = fmt[key]["weight"]

    # Divide the sum of scores by the sum of weights
    for _id in fmt_average_scores.keys():
        fmt_average_scores[_id] /= fmt_average_scores_deviation[_id]

    # Min-max normalization
    max_score = max(fmt_average_scores.values())
    min_score = min(fmt_average_scores.values())

    for _id in fmt_average_scores.keys():
        fmt_average_scores[_id] = (
            fmt_average_scores[_id] - min_score) / (max_score - min_score)

    return average_scores, fmt_average_scores


def find_match(collection_name: str, query_vector: npt.NDArray, limit: int) -> List[Tuple[str, float]]:
    try:
        match_result = vector_database.search(
            collection_name, query_vector, limit)
        # Chuyển đổi match_result thành một list các tuples
        return [(item[2]['id'], item[1]) for item in match_result]

    # In case the collection does not exist
    except Exception as e:
        return []


def query_match(target_tag: str, vectors: Dict[str, npt.NDArray], limit: int, user_id: str) -> Dict[str, List[Tuple[str, float]]]:
    match_results = {}
    for key, values in vectors.items():
        match_tuples = []
        collection_name = f"{target_tag}_{key}_{user_id}"

        for value in values:
            match_tuple = find_match(
                collection_name=collection_name, query_vector=value, limit=limit)
            match_tuples.append(match_tuple)

        match_results[key] = match_tuples

    return match_results


def match_cv_control(jd_id: str, limit: int, user_id: str, fmt: LLMFmt):
    # Query point that contains the JD ID
    vectors = query_control(tag="jd", user_id=user_id,
                            firebase_id=jd_id, fmt=fmt)

    # Find matched CVs
    match_results = query_match("cv", vectors, limit, user_id)

    return calculate_average_scores(match_results, fmt)[1]


def match_question_control(cv_id: str, limit: int, user_id: str, fmt: LLMFmt):
    # Query point that contains the JD ID
    vectors = query_control(tag="cv", user_id=user_id,
                            firebase_id=cv_id, fmt=fmt)

    # Find matched CVs
    match_results = query_match("question", vectors, limit, user_id)

    return calculate_average_scores(match_results, fmt)[1]


def MRR(scores: Dict[str, List[List[Tuple[str, float]]]], fmt: LLMFmt) -> Dict[str, float]:
    mrr = {}
    # Sort the scores
    scores
    print(scores)
    for key, values in scores.items():
        for value in values:
            for _id, score in value:
                # MRR (Mean Reciprocal Rank) measures the average position of the first relevant document
                # The smaller the MRR, the better the performance
                if _id in mrr:
                    mrr[_id] += 1 / (score * fmt[key]["weight"])
                else:
                    mrr[_id] = 1 / (score * fmt[key]["weight"])
    for _id in mrr.keys():
        mrr[_id] /= len(scores)
    return mrr
