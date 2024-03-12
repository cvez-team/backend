default_fmt = {
    "Degree": {
        "type": "list",
        "description": "Degree of the candidate. e.g. B.Tech, M.Tech, B.Sc, M.Sc"
    },
    "Experience": {
        "type": "list",
        "description": "Experience of the candidate in years."
    },
    "TechnicalSkills": {
        "type": "list",
        "description": "List of technical skills of the candidate."
    },
    "Responsibilities": {
        "type": "list",
        "description": "List of responsibilities of the candidate."
    },
    "Certifications": {
        "type": "list",
        "description": "List of certifications of the candidate."
    },
    "SoftSkills": {
        "type": "list",
        "description": "List of soft skills of the candidate."
    }
}

question_fmt = {
        "type": "list",
        "description": "Category of the keywords. e.g. Problem-solving, Leadership, Networking, etc.",
        "items": {
            "type": "string",
            "description": "Keywords extracted from the question."
            }
        }

    
    
            