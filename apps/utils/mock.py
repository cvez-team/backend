default_fmt = {
    "Experience": {
        "type": "list",
        "description": "Experience of the candidate in years.",
        "weight": 1.0
    },
    "TechnicalSkills": {
        "type": "list",
        "description": "List of technical skills of the candidate.",
        "weight": 2.0
    },
    "Certifications": {
        "type": "list",
        "description": "List of certifications of the candidate.",
        "weight": 1.0
    },
    "SoftSkills": {
        "type": "list",
        "description": "List of soft skills of the candidate.",
        "weight": 1.0
    },
    "Summary": {
        "type": "string",
        "description": "Summary of the extracted keywords."
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
    

    
    
            