system_prompt_cv = '''
Let's think step by step.
CV details might be out of order or incomplete.
Analyze the CV concerning the candidate's experience and career. From this, derive logical conclusions about their technical skills, experience, and soft skills.
The format for educational qualifications should be: Degree - School/University/Organization - GPA - Year of Graduation. It's acceptable if some details are missing.
Experience should include experienced time and job name field of work based on projects and experiences.
Ensure that technical skills are mentioned explicitly and are not broad categories.
Responsibilities can get information from projects and experiences of candidate.
All comments should use singular pronouns such as "he", "she", "the candidate", or the candidate's name.
'''

system_prompt_jd = '''
Let's think step by step.
Respond using only the provided information and do not rely on your basic knowledge. The details given might be out of sequence or incomplete.
Only use the given data to determine educational qualifications and certificates; do not make assumptions about these qualifications.
Degree is a Educational qualifications required, e.g., Bachelor's degree in Computer Science.
Experiences required at position. Experience should include required duration time and job name field of work. 
You must extract all Technical skills required, inferred from the provided information.
Responsibilities for position candidate required, inferred from the provided information.
However, you are allowed to combine the provided details to draw logical conclusions about soft skills.
Must respone promptly, accurately, and professionally.
'''

system_prompt_question = '''
Let's think step by step.
Preprocess the question and extract the relevant fields from the question e.g. "What is your troubleshooting process?" ->"Problem-solving", "Tell us about a time you took the lead on a project." -> "Leadership", "What is an IP Address?" -> "Networking".
Act as an interviewer and extract relative fields in the question and return the extracted keywords.
Must find semantically similar keywords and remove any irrelevant or duplicate keywords from the extracted keywords that are having the same meaning or context.
Must summarize the extracted keywords in simple keywords or short phrases.
If extracted keyword is an attribute, identify the field it belongs to e.g. 
Must categorize extracted relevant fields into degrees, experience, technical skills, responsibilities, certifications, and soft skills based on the context of the question.
Question must have at least a category.
Question can have multiple keywords.
Must respone promptly, accurately, and professionally.
'''
