from typing import Dict, List, AnyStr, Tuple, TypedDict
import numpy.typing as npt
import numpy as np
from qdrant_client.http.models import ScoredPoint
from ..schemas.criteria_schema import CriteriaSchema


class _ScoredOutputDetail(TypedDict):
    '''
    TypedDict for the output of the algorithm.
    '''
    overall: float
    detail: Dict[str, float]


class ScoredOutput(TypedDict):
    '''
    TypedDict for the output of the algorithm.
    '''
    overall: Dict[str, float]
    detail: Dict[str, Dict[str, _ScoredOutputDetail]]


class _FormattedOutput(TypedDict):
    '''
    TypedDict for the formatted output of the algorithm.
    '''
    overall: float
    criteria: Dict[str, float]


FormattedOutput = Dict[str, _FormattedOutput]


class AlgorithmProvider:
    '''
    Wrapper for algorithm implementations.
    '''

    def __init__(self, query_limit: int = 20, filter_threshold: float = 0.6):
        self.query_limit = query_limit
        self.filter_threshold = filter_threshold
        self.float_precision = 2

    def _calculate_single_score(self, score: float, cv_weight: int, jd_weight: int) -> float:
        '''
        Calculate the score for a single record.
        '''
        # If the score is below the threshold, set it to 0.0
        if score < self.filter_threshold:
            score = 0.0
        # Calculate the score
        score = (score * cv_weight) / jd_weight
        # If the score is above 1.0, set it to 1.0
        if score > 1.0:
            score = 1.0
        return score

    def _calculate_sum_and_tanh(self, scores: npt.ArrayLike) -> float:
        '''
        Calculate the sum of the scores and apply the hyperbolic tangent function.
        '''
        return np.tanh(np.sum(scores, axis=1))

    def implement(
        self,
        list_of_sps: List[List[ScoredPoint]],
        **kwargs
    ) -> ScoredOutput:
        # Get kwargs values
        cv_ids: List[AnyStr] = kwargs.get("cv_ids", [])
        jd_keywords: List[Tuple[AnyStr, int]] = kwargs.get("jd_keywords", [])

        # Format output data
        fmt_output: ScoredOutput = {
            "overall": {},
            "detail": {}
        }

        # If length of CV IDs is 0, return empty output
        if len(cv_ids) == 0:
            return fmt_output
        # If length of JD keywords is 0, return empty output
        if len(jd_keywords) == 0:
            return fmt_output

        # Create a placeholder matrix for the scores.
        # The matrix has shape (i, q, k)
        # where i is the number of keywords in the JD,
        # q is the number of queries, k is the number of CV IDs.
        scores = np.zeros(
            (len(jd_keywords), self.query_limit, len(cv_ids)))

        # Iterate over list of records to build the scores matrix
        for i, sps in enumerate(list_of_sps):
            jd_kw = jd_keywords[i][0]
            fmt_output["detail"][jd_kw] = {
                cv_id: {"overall": 0.0, "detail": {}} for cv_id in cv_ids}

            jdw = jd_keywords[i][1]
            for q, sp in enumerate(sps):
                cvw = sp.payload["payload"]["score"]
                cv_id = sp.payload["payload"]["id"]
                cv_kw = sp.payload["document"]
                # Get the index of the CV ID
                try:
                    k = cv_ids.index(cv_id)
                except ValueError:
                    continue
                # Calculate the score for the record
                _score = self._calculate_single_score(sp.score, cvw, jdw)
                scores[i, q, k] = _score
                fmt_output["detail"][jd_kw][cv_id]["detail"][cv_kw] = _score

        # Sum the scores and apply the hyperbolic tangent function
        tanh_scores = self._calculate_sum_and_tanh(scores)

        # Assign overall scores of each CV ID to formatted output
        for i, (jd_kw, _) in enumerate(jd_keywords):
            for j, cv_id in enumerate(cv_ids):
                fmt_output["detail"][jd_kw][cv_id]["overall"] = tanh_scores[i, j]

        # Calculate percent contribution of each JD keyword
        p = 100 / sum([x[1] for x in jd_keywords])
        jdws = np.array([[x[1] * p for x in jd_keywords]])

        # Calculate the overall score
        overall_score = np.sum(tanh_scores.T * jdws, axis=1)

        for i, cv_id in enumerate(cv_ids):
            fmt_output["overall"][cv_id] = overall_score[i]

        return fmt_output

    def apply_criterias(self, cvs: List[AnyStr], criterias: List[CriteriaSchema],
                        scores: Dict[str, ScoredOutput]) -> FormattedOutput:
        # Format output data
        fmt_output: FormattedOutput = {
            cv_id: {"overall": 0.0, "criteria": {}} for cv_id in cvs}

        # Iterate over criterias
        for criteria in criterias:
            # Get Score output by criteria name
            if criteria.name not in scores:
                continue
            scored_output = scores[criteria.name]["overall"]

            for k, v in scored_output.items():
                fmt_output[k]["overall"] += v * criteria.score
                fmt_output[k]["criteria"][criteria.name] = round(
                    v, self.float_precision)

        # Normalize the overall score
        total_weight = sum([criteria.score for criteria in criterias])
        for cv_id in cvs:
            fmt_output[cv_id]["overall"] = round(
                fmt_output[cv_id]["overall"] / total_weight, self.float_precision)

        return fmt_output
