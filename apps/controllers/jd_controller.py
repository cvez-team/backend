from typing import Any, Dict
import re
from plugins.typing import LLMFmt
from .extract_controller import extract_control
from .upload_vector_controller import upload_vector_control
from ..models.jd_model import JDModel
from ..providers.db_provider import DatabaseProvider
from ..utils.system_prompt import system_prompt_jd
from ..utils.constants import JD_COLLECTION

# Define the database and vector database provider
database = DatabaseProvider(collection_name=JD_COLLECTION)


def jd_control(title: str, content: str, user_id: str, fmt: LLMFmt) -> Dict[str, Any]:
    '''
    Extract the data from the JD file, and upload to the database.
    '''
    raw_text = re.sub(r"[^a-zA-z0-9\s]", "", content)

    # Extract features from the raw text
    extraction, word_embeddings = extract_control(
        system_prompt=system_prompt_jd, prompt=raw_text, fmt=fmt
    )

    # Format data to upload
    jd_data = JDModel(
        title=title,
        content=content,
        extraction=extraction
    ).to_dict()

    # Upload the extraction to the database
    data_id = database.create(data=jd_data)
    jd_data["id"] = data_id

    # Upload vector to the database
    upload_vector_control(extraction=extraction, word_embeddings=word_embeddings,
                          tag="jd", user_id=user_id, firebase_id=data_id)

    return jd_data