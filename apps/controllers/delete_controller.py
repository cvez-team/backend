from ..providers.db_provider import DatabaseProvider
from ..providers.storage_provider import StorageProvider
from ..providers.vectordb_provider import VectorDatabaseProvider
from ..utils.constants import CV_COLLECTION, JD_COLLECTION, QUESTION_COLLECTION, CV_STORAGE, WORD_EMBEDDING_DIM


cv_database = DatabaseProvider(collection_name=CV_COLLECTION)
jd_database = DatabaseProvider(collection_name=JD_COLLECTION)
question_database = DatabaseProvider(collection_name=QUESTION_COLLECTION)
cv_storage = StorageProvider(directory=CV_STORAGE)
vector_database = VectorDatabaseProvider(size=WORD_EMBEDDING_DIM)


def delete_jd_by_id_control(jd_id: str):
    # Remove vectors from vector database
    vector_collections = vector_database.get_collections()
    vector_collections = [
        collection for collection in vector_collections if "jd" in collection]
    for collection in vector_collections:
        vector_ids = vector_database.query(collection, "id", jd_id)
        vector_ids = [vector_id[0] for vector_id in vector_ids]
        if len(vector_ids) > 0:
            vector_database.delete(collection, vector_ids)

    # Delete collection from firebase
    return jd_database.delete(jd_id)


def delete_cv_by_id_control(cv_id: str):
    # Remove file from firebase storage
    cv_data = cv_database.get_by_id(cv_id)
    cv_storage.remove(cv_data["path"])

    # Remove vectors from vector database
    vector_collections = vector_database.get_collections()
    vector_collections = [
        collection for collection in vector_collections if "cv" in collection]
    for collection in vector_collections:
        vector_ids = vector_database.query(collection, "id", cv_id)
        vector_ids = [vector_id[0] for vector_id in vector_ids]
        if len(vector_ids) > 0:
            vector_database.delete(collection, vector_ids)

    # Delete collection from firebase
    return cv_database.delete(cv_id)


def delete_question_by_id_control(question_id: str):
    # Remove vectors from vector database
    vector_collections = vector_database.get_collections()
    vector_collections = [
        collection for collection in vector_collections if "question" in collection]
    for collection in vector_collections:
        vector_ids = vector_database.query(collection, "id", question_id)
        vector_ids = [vector_id[0] for vector_id in vector_ids]
        if len(vector_ids) > 0:
            vector_database.delete(collection, vector_ids)

    # Delete collection from firebase
    return question_database.delete(question_id)
