default_fmt = {
    "Experience": {
        "type": "list",
        "description": "Extracting experiments that be mentioned or related to the provided contents. The experiments must be concise, precise, easy to understand. This field only accept a list of string, not dictionary or any other types.",
        "weight": 3.5
    },
    "TechnicalSkills": {
        "type": "list",
        "description": "Extracting the technical keywords that be mentioned or related to the provided contents. The technical skills must be a phrase or a word. This field only accept a list of string, not dictionary or any other types.",
        "weight": 3.5
    },
    "Certifications": {
        "type": "list",
        "description": "Find the certifications that be mentioned, related or required to the provided contents. The certifications must be simple as a phrase, concise. This field only accept a list of string, not dictionary or any other types.",
        "weight": 1.0
    },
    "SoftSkills": {
        "type": "list",
        "description": "Extracting the softskill keywords that be mentioned, related or required to the provided contents. The softskills must be a phrase or a word. This field only accept a list of string, not dictionary or any other types.",
        "weight": 2.0
    },
    "Summary": {
        "type": "string",
        "description": "Provide a simple, concise summarization about the provided contents. This summarization is about the extracted keywords from above. This field must be a string, not a dictionary or any other types.",
        "weight": 1.0
    }
}

question_fmt = {
    "Experience": {
        "type": "list",
        "description": "Required if the question is about the experience of the candidate.",
        "weight": 1.0
    },
    "TechnicalSkills": {
        "type": "list",
        "description": "Required if the question is about the technical skills of the candidate.",
        "weight": 2.0
    },
    "Certifications": {
        "type": "list",
        "description": "Required if the question is about the certifications of the candidate.",
        "weight": 1.0
    },
    "SoftSkills": {
        "type": "list",
        "description": "If the question is about the soft skills of the candidate.",
        "weight": 1.0
    },
    "Summary": {
        "type": "string",
        "description": "Summary of the extracted keywords."
    }
}
