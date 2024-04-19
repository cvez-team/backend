from typing import AnyStr
from fastapi import HTTPException, status
import numpy as np
from ..schemas.user_schema import UserSchema
from ..schemas.project_schema import ProjectSchema
from ..schemas.position_schema import PositionSchema
from ..schemas.cv_schema import CVSchema
from ..schemas.embedding_schema import VectorEmbeddingSchema


def _validate_permission(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    # Check project_id and position_id in user's projects
    if project_id not in user.projects and project_id not in user.shared:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to access this project"
        )

    # Get project from project_id
    project = ProjectSchema.find_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Check position_id in project's positions
    if position_id not in project.positions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to access this position"
        )

    # Get position from position_id
    position = PositionSchema.find_by_id(position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found"
        )

    return project, position


def get_all_matches_cv(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    # Validate permission
    _, position = _validate_permission(project_id, position_id, user)

    score_results = {}
    format_results = {}

    # Iterate over criteria
    for criteria in position.criterias:
        score_results[criteria.name] = {}

        # Fetch all JD embeddings
        vectors = VectorEmbeddingSchema.from_database(
            collection=position.id,
            space=f"jd_{criteria.name}"
        )

        records = vectors.search(
            collection=position.id,
            space=f"cv_{criteria.name}",
            limit=20
        )

        formated_records = []
        if len(vectors.vectors) == 0:
            continue
        gap = 100 / len(vectors.vectors)

        for i, _records in enumerate(records):
            jd_weight = vectors.payloads[i]["score"]

            formated_records.append([])
            for _record in _records:
                # Get data from record
                score = _record.score
                _id = _record.payload["payload"]["id"]
                cv_weight = _record.payload["payload"]["score"]
                # Format score
                if score < 0.6:
                    score = 0.0
                score = (score * cv_weight) / jd_weight
                if score > 1.0:
                    score = 1.0
                score *= gap
                formated_records[-1].append([_id, score])

        # Continue if no records
        if len(formated_records) == 0:
            continue
        if len(formated_records[0]) == 0:
            continue

        # Calculate by numpy
        mat = np.array(formated_records)
        id_mat = mat[:, :, 0]
        for _id in np.unique(id_mat):
            # Append to format_results
            if _id not in format_results:
                format_results[_id] = {
                    "overall": 0,
                    "criteria": {}
                }

            mask = np.zeros_like(id_mat, dtype=bool)
            mask[np.where(id_mat == _id)] = True
            fmat = np.where(mask, mat[:, :, 1], 0).astype(float)
            count_non_zero = np.sum(mask, axis=1) + 1
            score_results[criteria.name][_id] = round(
                (fmat.sum(axis=1) / count_non_zero).sum(), 2)

    # Iterate over score_results to get format_results
    for i, (criteria, scores) in enumerate(score_results.items()):
        for _id, score in scores.items():
            format_results[_id]["criteria"][criteria] = score

    # Iterate over format_results to get overall score
    for _id, scores in format_results.items():
        overall = 0
        for name, score in scores["criteria"].items():
            weight = position.find_criteria_by_name(name).score
            if not weight:
                weight = 1
            overall += score * weight
        overall /= position.get_total_criteria_score()
        format_results[_id]["overall"] = round(overall, 2)

    # Iterate over format_results to save to database
    for _id, score_data in format_results.items():
        # Check if id in position cv
        if _id not in position.cvs:
            continue

        # Find cv by id
        cv = CVSchema.find_by_id(_id)
        if not cv:
            continue

        # Update cv score
        cv.update_score(score_data)

    return format_results


def get_all_matches_question(project_id: AnyStr, position_id: AnyStr, cv_id: AnyStr, user: UserSchema):
    return {
        "1": {
            "overall": 100,
            "criteria": {
                "Education": 100,
                "Experience": 100,
                "Skill": 100
            }
        }
    }
