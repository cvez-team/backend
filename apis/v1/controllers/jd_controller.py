from typing import AnyStr
from pydantic import BaseModel
from fastapi import HTTPException, status
from ..schemas.user_schema import UserSchema
from ..schemas.project_schema import ProjectSchema
from ..schemas.position_schema import PositionSchema
from ..schemas.jd_schema import JDSchema
from ..schemas.embedding_schema import VectorEmbeddingSchema
from ..providers import llm
from ..utils.prompt import system_prompt_jd
from ..utils.extractor import get_jd_content


def _validate_permission(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    # Validate project id in user's projects
    if project_id not in user.projects and project_id not in user.shared:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this project."
        )

    # Get project
    project = ProjectSchema.find_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )

    # Validate position id in project's positions
    if position_id not in project.positions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this position."
        )

    # Get position
    position = PositionSchema.find_by_id(position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )

    return project, position


def get_current_jd(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    _, position = _validate_permission(project_id, position_id, user)

    # Return null if no JD
    if not position.jd or position.jd == "":
        jd_instance = JDSchema().create_jd()

        # Update position
        position.update_jd(jd_instance.id)
        return jd_instance

    # Get JD
    jd = JDSchema.find_by_id(position.jd)
    if not jd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="JD not found."
        )

    return jd


def _analyse_jd_content(content: AnyStr, jd: JDSchema, position: PositionSchema):
    # Generate content
    generator = llm.construct(position.criterias)
    extraction = generator.generate(system_prompt_jd, content)

    # Update JD extraction
    jd.update_extraction(extraction)

    # Extract keywords
    criteria_names = [criteria.name for criteria in position.criterias]
    try:
        for key, value in extraction.items():
            # Check key in criterias
            if key not in criteria_names:
                continue

            # Get vectors and payloads
            payloads = []
            values = []
            for keyword, score in value.items():
                payloads.append({
                    "id": jd.id,
                    "score": score,
                })
                values.append(keyword)
            vectors = VectorEmbeddingSchema.from_documents(values, payloads)

            # Upload to vector database
            vectors.upload(position.id, f"jd_{key}")

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting keywords. {str(e)}"
        )


def _upload_jd_content(content: AnyStr, position: PositionSchema):
    # Get current JD
    jd_instance = JDSchema.find_by_id(position.jd)
    if not jd_instance:
        # Create instance
        jd_instance = JDSchema(
            content=content
        ).create_jd()
    else:
        # Update content
        jd_instance.update_content(content)

    # Update position
    if not position.jd or position.jd == "":
        position.update_jd(jd_instance.id)

    # Parse content
    content = get_jd_content(content)

    # Analyse JD content
    _analyse_jd_content(content, jd_instance, position)


def update_current_jd(project_id: AnyStr, position_id: AnyStr, data: BaseModel, user: UserSchema):
    # Validate permission
    _, position = _validate_permission(project_id, position_id, user)

    # Upload JD content
    if data.content == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="JD content is required or not be empty."
        )

    _upload_jd_content(data.content, position)
