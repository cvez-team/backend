from ..providers.db_provider import DatabaseProvider


cv_database = DatabaseProvider(collection_name="CVs")
jd_database = DatabaseProvider(collection_name="JDs")
question_database = DatabaseProvider(collection_name="Questions")


def get_all_cv_control():
    return cv_database.get_all()


def get_cv_by_id_control(cv_id: str):
    return cv_database.get_by_id(cv_id)


def get_all_jd_control():
    return jd_database.get_all()


def get_jd_by_id_control(jd_id: str):
    return jd_database.get_by_id(jd_id)


def get_all_question_control():
    return question_database.get_all()


def get_question_by_id_control(question_id: str):
    return question_database.get_by_id(question_id)
