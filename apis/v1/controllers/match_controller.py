from typing import AnyStr
from fastapi import HTTPException, status, BackgroundTasks
from ..schemas.user_schema import UserSchema
from ..schemas.project_schema import ProjectSchema
from ..schemas.position_schema import PositionSchema
from ..schemas.cv_schema import CVSchema
from ..schemas.embedding_schema import VectorEmbeddingSchema
from ..providers.algorithm_provider import AlgorithmProvider, FormattedOutput


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


def _update_score_to_database(position: PositionSchema, scores: FormattedOutput):
    # Iterate over CVs
    for _id, score in scores.items():
        if _id not in position.cvs:
            continue

        # Get CV from _id
        cv = CVSchema.find_by_id(_id)
        if not cv:
            continue

        # Update score to CV
        cv.update_score(score)


def get_all_matches_cv(project_id: AnyStr, position_id: AnyStr, query_limit: int, threshold: float, user: UserSchema, bg_task: BackgroundTasks):
    # Validate permission
    _, position = _validate_permission(project_id, position_id, user)

    # Define providers
    algorithm = AlgorithmProvider(
        query_limit=query_limit, filter_threshold=threshold)

    fmt_output = {}

    # Iterate over criteria
    for criteria in position.criterias:
        # Fetch all JD embeddings
        vectors = VectorEmbeddingSchema.from_database(
            collection=position.id,
            space=f"jd_{criteria.name}"
        )

        records = vectors.search(
            collection=position.id,
            space=f"cv_{criteria.name}",
            limit=algorithm.query_limit
        )

        jd_keywords = [(jd_doc, jd_payload["score"])
                       for _, _, jd_doc, jd_payload in vectors]

        # Implement algorithm
        results = algorithm.implement(records, cv_ids=position.cvs,
                                      jd_keywords=jd_keywords)

        # Assign results to fmt_output
        fmt_output[criteria.name] = results

    score_result = algorithm.apply_criterias(
        position.cvs, position.criterias, fmt_output)

    # Save score results to database
    bg_task.add_task(_update_score_to_database, position, score_result)

    return score_result


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
