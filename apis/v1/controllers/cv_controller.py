from typing import AnyStr
from fastapi import UploadFile, HTTPException, status, BackgroundTasks
import uuid
import time
from ..schemas.user_schema import UserSchema
from ..schemas.cv_schema import CVSchema
from ..schemas.project_schema import ProjectSchema
from ..schemas.position_schema import PositionSchema
from ..schemas.embedding_schema import VectorEmbeddingSchema
from ..schemas.criteria_schema import CriteriaSchema
from ..providers import memory_cacher, storage_db, llm
from ..utils.extractor import get_cv_content
from ..utils.prompt import system_prompt_cv
from ..utils.utils import validate_file_extension, get_content_type


def _validate_permissions(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
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


def get_all_cvs(project_id: AnyStr, position_id: AnyStr, user: UserSchema):
    _, position = _validate_permissions(project_id, position_id, user)

    # Get CVs
    cvs = CVSchema.find_by_ids(position.cvs)
    return cvs


def get_cv_by_id(project_id: AnyStr, position_id: AnyStr, cv_id: AnyStr, user: UserSchema):
    _, _ = _validate_permissions(project_id, position_id, user)

    # Get CV
    cv = CVSchema.find_by_id(cv_id)
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found."
        )

    return cv


def _upload_cv_data(data: bytes, filename: AnyStr, watch_id: AnyStr, cv: CVSchema):
    # Get content type of file
    content_type = get_content_type(filename)
    path, url = storage_db.upload(data, filename, content_type)
    memory_cacher.get(watch_id)["percent"][filename] += 15
    cv.update_path_url(path, url)
    memory_cacher.get(watch_id)["percent"][filename] += 5


def _validate_llm_extraction(extraction: dict, criterias: list[CriteriaSchema]) -> dict:
    '''
    Sometimes, the extraction from LLM model may contain unwanted keywords.\n
    This function will filter out the unwanted keywords from the extraction.
    '''
    # Get criteria names
    criteria_names = [criteria.name for criteria in criterias]

    # If there is a field `properties` in the extraction, extract the keywords from it
    if "properties" in extraction:
        if isinstance(extraction["properties"], dict):
            for key, value in extraction["properties"].items():
                if key in criteria_names:
                    extraction[key] = value

    # Filter out unwanted keywords
    filtered_extraction = {}
    for key, value in extraction.items():
        if key in criteria_names:
            filtered_extraction[key] = value

    return filtered_extraction


def _analyze_cv_data(content: AnyStr, watch_id: AnyStr, filename: AnyStr, cv: CVSchema, position: PositionSchema):
    # Generate content
    generator = llm.construct(position.criterias)
    extraction = generator.generate(system_prompt_cv, content)
    extraction = _validate_llm_extraction(extraction, position.criterias)
    memory_cacher.get(watch_id)["percent"][filename] += 30

    # Update extraction
    cv.update_extraction(extraction)
    memory_cacher.get(watch_id)["percent"][filename] += 5

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
                    "id": cv.id,
                    "score": score,
                })
                values.append(keyword)
            vectors = VectorEmbeddingSchema.from_documents(values, payloads)

            # Upload to vector database
            vectors.upload(position.id, f"cv_{key}")
        memory_cacher.get(watch_id)["percent"][filename] += 25

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting keywords. {str(e)}"
        )


def _upload_cvs_data(cvs: list[bytes], filenames: list[AnyStr], watch_id: AnyStr, position: PositionSchema):
    for cv, filename in zip(cvs, filenames):
        memory_cacher.get(watch_id)["percent"][filename] = 0

        # Create CV document in database
        cv_instance = CVSchema(
            name=filename,
        ).create_cv()
        memory_cacher.get(watch_id)["percent"][filename] += 10

        # Upload to storage
        try:
            _upload_cv_data(
                cv, filename, watch_id, cv_instance)
        except Exception as e:
            memory_cacher.get(watch_id)["error"][filename] = str(e)
            continue

        # Save file to cache folder
        cache_file_path = memory_cacher.save_cache_file(cv, filename)
        cv_content = get_cv_content(cache_file_path)
        memory_cacher.remove_cache_file(filename)
        memory_cacher.get(watch_id)["percent"][filename] += 5

        # Analyze CV
        try:
            _analyze_cv_data(cv_content, watch_id, filename,
                             cv_instance, position)
        except Exception as e:
            memory_cacher.get(watch_id)["error"][filename] = str(e)
            continue

        # Update to position
        position.update_cv(cv_instance.id, is_add=True)
        memory_cacher.get(watch_id)["percent"][filename] += 5

    # Wait for 10 second to remove watch id
    time.sleep(10)

    # Delete cache file
    memory_cacher.remove(watch_id)


async def upload_cvs_data(project_id: AnyStr, position_id: AnyStr, user: UserSchema, cvs: list[UploadFile], bg_tasks: BackgroundTasks):
    # Validate permission
    _, position = _validate_permissions(project_id, position_id, user)

    # Validate criterias
    if len(position.criterias) == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No criteria to analyze."
        )

    # Create watch id
    watch_id = str(uuid.uuid4())

    # Read files
    files: list[bytes] = []
    filenames: list[AnyStr] = []
    for cv in cvs:
        file_content = await cv.read()
        files.append(file_content)
        filenames.append(cv.filename)

    # Initialize cache
    memory_cacher.set(watch_id, {
        "percent": {},
        "error": {}
    })

    # Upload CVs
    bg_tasks.add_task(_upload_cvs_data, files, filenames, watch_id, position)

    return watch_id


async def upload_cv_data(position_id: AnyStr, cv: UploadFile, bg_tasks: BackgroundTasks):
    # Validate extension
    validate_file_extension(cv.filename)

    # Get position
    position = PositionSchema.find_by_id(position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )

    if position.is_closed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Position is closed."
        )

    # Validate criterias
    if len(position.criterias) == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No criteria to analyze."
        )

    # Read files
    file_content = await cv.read()

    # Create watch id
    watch_id = str(uuid.uuid4())

    # Initialize cache
    memory_cacher.set(watch_id, {
        "percent": {},
        "error": {}
    })

    # Upload CV
    bg_tasks.add_task(_upload_cv_data, [file_content], [
                      cv.filename], watch_id, position)

    return watch_id


def get_upload_progress(watch_id: AnyStr):
    return memory_cacher.get(watch_id)


async def download_cv_content(project_id: AnyStr, position_id: AnyStr, cv_id: AnyStr, user: UserSchema) -> bytes:
    # Validate permission
    _, _ = _validate_permissions(project_id, position_id, user)

    # Get CV
    cv = CVSchema.find_by_id(cv_id)
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found."
        )

    cv_content = cv.download_content()
    if not cv_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV content not found."
        )

    return cv_content


def delete_cvs_by_ids(cv_ids: list[AnyStr]):
    for cv_id in cv_ids:
        cv = CVSchema.find_by_id(cv_id)
        if cv:
            cv.delete_cv()


def delete_current_cv(project_id: AnyStr, position_id: AnyStr, cv_id: AnyStr, user: UserSchema):
    # Validate permission
    _, position = _validate_permissions(project_id, position_id, user)

    # Get CV
    cv = CVSchema.find_by_id(cv_id)
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found."
        )

    # Remove CV from position
    position.update_cv(cv_id, is_add=False)

    # Delete vectors
    VectorEmbeddingSchema.from_query(
        collection=position_id,
        key="id",
        value=cv_id
    ).delete(position_id)

    # Delete CV
    cv.delete_cv()
