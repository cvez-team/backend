from plugins.typing import LLMFmt
from plugins.llm import LLMGenerator
from .query_controller import query_control
from .match_controller import query_match, calculate_average_scores
from ..providers.db_provider import DatabaseProvider
from ..utils.system_prompt import system_cv_generation
from ..utils.constants import CV_COLLECTION, JD_COLLECTION, SUMMARIZATION_FMT


cv_database = DatabaseProvider(collection_name=CV_COLLECTION)
jd_database = DatabaseProvider(collection_name=JD_COLLECTION)
generator = LLMGenerator(SUMMARIZATION_FMT)


def generate_control(cv_id: str, jd_id: str, user_id: str, fmt: LLMFmt):
    # Fetch CV and JD content from firebase
    cv_data = cv_database.get_by_id(cv_id)
    jd_data = jd_database.get_by_id(jd_id)

    # Format the prompt
    prompt = f"CV JSON extraction data: {cv_data['extraction']}\nJD JSON extraction data: {jd_data['extraction']}"

    # Prompt LLM to generate summarization
    summarization = generator.generate(system_cv_generation, prompt)

    # Querry scores
    vectors = query_control(tag="jd", user_id=user_id,
                            firebase_id=jd_id, fmt=fmt)
    match_results = query_match("cv", vectors, 1, user_id)
    average_scores = calculate_average_scores(match_results, fmt)[0]
    fmt_average_scores = {}
    # Convert float32 to float
    for key, values in average_scores.items():
        if cv_id in values:
            fmt_average_scores[key] = float(values[cv_id])
        else:
            fmt_average_scores[key] = 0.0

    # Return the summarization
    return {
        "score": fmt_average_scores,
        "summarize": summarization,
    }
