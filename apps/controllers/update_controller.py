from ..providers.db_provider import DatabaseProvider
from ..utils.constants import CV_COLLECTION, JD_COLLECTION, QUESTION_COLLECTION

cv_database = DatabaseProvider(collection_name=CV_COLLECTION)
jd_database = DatabaseProvider(collection_name=JD_COLLECTION)
question_database = DatabaseProvider(collection_name=QUESTION_COLLECTION)


def update_cv_content_control(cv_id: str, new_content: str):
    return cv_database.update(cv_id, new_content)


def update_jd_content_control(jd_id: str, new_content: str):
    return jd_database.update(jd_id, new_content)


def update_question_content_control(question_id: str, new_content: str):
    return question_database.update(question_id, new_content)
