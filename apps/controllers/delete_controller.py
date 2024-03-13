from ..providers.db_provider import DatabaseProvider


cv_database = DatabaseProvider(collection_name="CVs")
jd_database = DatabaseProvider(collection_name="JDs")
question_database = DatabaseProvider(collection_name="Questions")


def delete_jd_by_id_control(jd_id: str):
    return jd_database.delete(jd_id)

def delete_cv_by_id_control(cv_id: str):
    return cv_database.delete(cv_id)

def delete_question_by_id_control(question_id: str):
    return question_database.delete(question_id)
