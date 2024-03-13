from ..providers.db_provider import DatabaseProvider

cv_database = DatabaseProvider(collection_name="CVs")
jd_database = DatabaseProvider(collection_name="JDs")
question_database = DatabaseProvider(collection_name="Questions")


def update_cv_content_control(cv_id: str, new_content: str):
    return cv_database.update(cv_id, new_content)


def update_jd_content_control(jd_id: str, new_content: str):
    return jd_database.update(jd_id, new_content)


def update_question_content_control(question_id: str, new_content: str):
    return question_database.update(question_id, new_content)
