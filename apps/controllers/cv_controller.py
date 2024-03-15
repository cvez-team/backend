from typing import Any, Dict
from plugins.typing import LLMFmt
from .extract_controller import extract_control
from .cv_extracter import get_cv_content
from .upload_vector_controller import upload_vector_control
from ..models.cv_model import CVModel
from ..providers.db_provider import DatabaseProvider
from ..providers.storage_provider import StorageProvider
from ..providers.cache_provider import CacheProvider
from ..utils.system_prompt import system_prompt_cv
from ..utils.constants import CV_COLLECTION, CV_STORAGE


# Define the database and vector database provider
database = DatabaseProvider(collection_name=CV_COLLECTION)
storage = StorageProvider(directory=CV_STORAGE)
cacher = CacheProvider()


def cv_control(file: bytes, filename: str, user_id: str, fmt: LLMFmt) -> Dict[str, Any]:
    '''
    Extract the data from the CV file, and upload to the database.
    '''
    # Upload file to Firebase storage
    path, url = storage.upload(file, filename)

    # Convert the file to raw text. Save and remove the cache file
    cache_file_path = cacher.save_cache_file(file, filename)
    raw_text = get_cv_content(cache_file_path)
    cacher.remove_cache_file(filename)

    # Extract features from the raw text
    extraction, word_embeddings = extract_control(
        system_prompt=system_prompt_cv, prompt=raw_text, fmt=fmt
    )

    # Format data to upload
    cv_data = CVModel(
        name=filename,
        path=path,
        url=url,
        extraction=extraction
    ).to_dict()

    # # Upload the extraction to the database
    # data_id = database.create(data=cv_data)
    # cv_data["id"] = data_id

    # # Upload vector to the database
    # upload_vector_control(extraction=extraction, word_embeddings=word_embeddings,
    #                       tag="cv", user_id=user_id, firebase_id=data_id)

    return cv_data
