# Qdrant vectors
WORD_EMBEDDING_DIM = 768

# Firebase collections
CV_COLLECTION = "CVs"
JD_COLLECTION = "JDs"
QUESTION_COLLECTION = "Questions"

# Firebase storage
CV_STORAGE = "CVs"

# Summarization FMT
SUMMARIZATION_FMT = {
    "JDSummarization": {
        "type": "string",
        "description": "Provide the concise, simple summarization of the content, keywords, extraction dictionaries of the provided Job Description. This field only accepts string value, not any other type."
    },
    "JDRequirements": {
        "type": "list",
        "description": "Provide a list of requirements that are mentioned, related, or extracted from the content, keywords, extraction dictionaries of the provided Job Description. This field only accepts list of string, not any other type."
    },
    "CVSummarization": {
        "type": "string",
        "description": "Provide the concise, simple summarization of the content, keywords, extraction dictionaries of the provided CV. This field only accepts string value, not any other type."
    },
    "CVFulfillments": {
        "type": "list",
        "description": "Provide a list of fulfillments the above Job description that are extracted from the content, keywords, extraction dictionaries of the provided CV. It's ok if this field is an empty list. This field only accepts list of string, not any other type."
    }
}
