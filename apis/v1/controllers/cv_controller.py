from typing import AnyStr
from fastapi import UploadFile, HTTPException, status
import uuid
import asyncio
from ..schemas.user_schema import UserSchema
from ..schemas.cv_schema import CVSchema
from ..schemas.project_schema import ProjectSchema
from ..schemas.position_schema import PositionSchema
from ..schemas.embedding_schema import VectorEmbeddingSchema
from ..providers import memory_cacher, storage_db, llm
from ..utils.extractor import get_cv_content
from ..utils.prompt import system_prompt_cv
from ..utils.utils import validate_file_extension, get_content_type


loop = asyncio.get_event_loop()


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


async def _upload_cv_data(data: bytes, filename: AnyStr, watch_id: AnyStr, cv: CVSchema):
    # Get content type of file
    content_type = get_content_type(filename)
    path, url = storage_db.upload(data, filename, content_type)
    memory_cacher.get(watch_id)["percent"][filename] += 15
    cv.update_path_url(path, url)
    memory_cacher.get(watch_id)["percent"][filename] += 5


async def _analyze_cv_data(content: AnyStr, watch_id: AnyStr, filename: AnyStr, cv: CVSchema, position: PositionSchema):
    # Generate content
    generator = llm.construct(position.criterias)
    extraction = generator.generate(system_prompt_cv, content)
    memory_cacher.get(watch_id)["percent"][filename] += 20

    # Update extraction
    cv.update_extraction(extraction)
    memory_cacher.get(watch_id)["analyzed"][filename] = True
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
            memory_cacher.get(watch_id)["percent"][filename] += 20

            # Upload to vector database
            vectors.upload(position.id, f"cv_{key}")
            memory_cacher.get(watch_id)["percent"][filename] += 15

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting keywords. {str(e)}"
        )


async def _upload_cvs_data(cvs: list[bytes], filenames: list[AnyStr], watch_id: AnyStr, position: PositionSchema):
    for cv, filename in zip(cvs, filenames):
        memory_cacher.get(watch_id)["percent"][filename] = 0

        # Create CV document in database
        cv_instance = CVSchema(
            name=filename,
        ).create_cv()
        memory_cacher.get(watch_id)["percent"][filename] += 10

        # Update to position
        position.update_cv(cv_instance.id, is_add=True)
        memory_cacher.get(watch_id)["percent"][filename] += 5

        # Upload to storage
        await _upload_cv_data(
            cv, filename, watch_id, cv_instance)

        # Save file to cache folder
        cache_file_path = memory_cacher.save_cache_file(cv, filename)
        cv_content = get_cv_content(cache_file_path)
        memory_cacher.remove_cache_file(filename)
        memory_cacher.get(watch_id)["percent"][filename] += 5

        # Analyze CV
        await _analyze_cv_data(cv_content, watch_id, filename,
                               cv_instance, position)


async def upload_cvs_data(project_id: AnyStr, position_id: AnyStr, user: UserSchema, cvs: list[UploadFile]):
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
        "analyzed": {}
    })

    # Upload CVs
    _coroutine = _upload_cvs_data(files, filenames, watch_id, position)
    _task = asyncio.create_task(_coroutine)
    _task.add_done_callback(lambda _: memory_cacher.remove(watch_id))

    return watch_id


async def upload_cv_data(position_id: AnyStr, cv: UploadFile):
    # Validate extension
    validate_file_extension(cv.filename)

    # Get position
    position = PositionSchema.find_by_id(position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found."
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
        "analyzed": {}
    })

    await _upload_cvs_data([file_content], [cv.filename], watch_id, position)
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

    # Delete CV
    cv.delete_cv()

    # Delete vectors
    VectorEmbeddingSchema.from_query(
        collection=position_id,
        key="id",
        value=cv_id
    ).delete(position_id)
