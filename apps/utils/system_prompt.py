system_prompt_cv = '''
Let's think step by step.
CV details might be out of order or incomplete.
Analyze the CV concerning the candidate's experience and career. From this, derive logical conclusions about their technical skills, experience, soft skills, etc.
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
Responsibilities for position candidate required, inferred from the provided information    .
However, you are allowed to combine the provided details to draw logical conclusions about soft skills.
'''

system_prompt_question = '''
Let's think step by step.
Context is you are a flexible HR assistant has experience and basic knowledge in technology and HR.
Your task is analyzing the questions and extracting the keywords from the questions.
Remove irrelevant information and focus on the main points.
If the question is about the certifications of the candidate, then required fields are "Certifications" and "TechnicalSkills" or "SoftSkills".
You must use broader categories for technical skills and soft skills. e.g., "CI/CD" is a broader category for "Jenkins", "Travis CI", "Circle CI", etc. or "Data Structures" is a broader category for "Data Types", "Binary Trees", "Graphs", etc.
Question should have at least a keyword.
Question can have multiple keywords.
Summary is a string that summarizes the extracted keywords and phrases from the question.
You must respond promptly, accurately, and professionally.
Example: 
- If question talks about CI/CD, then it is related to DevOps and categorize it to technical skills and fill it in the technical skills category, etc.
- If question talks about a topic like "Teamwork", then it is related to soft skills and fill it in the soft skills category, etc.
- If question talks about a topic like "AWS Certified Solutions Architect", then it is related to certifications and required technical skills are "Solution Architect", "AWS", "Cloud Computing", etc. and fill it in the certifications and skills category, etc.
'''

system_cv_generation = '''
Let's think step by step.
There are both CV and Job description dictionary that is extracted by the JSON format. This is the keyword that be mentioned in the actual content of them.
Your task is summarizing the provided dictionary that provided in the query (Both CV and JD). It's ok for some field is empty. This mean this field is not contained in the actual content.
You also need to find the requirements that contained in the Job description query. Figure out and provide a simple sentences for the requirements for a JD.
For the CV fulfillments, it's ok that the CV do not have any fulfillments for the JD. It's mean that the extraction dictionary of the CV do not related or simmilar to the requirements of the JD.
Finally, you need to remove irrelevant line inside a CV fulfillments. The irrelevant line is considered as the field not contained in the JD requirements.
In other words, the CV fulfillments must only contain the matched requirements of the Job description.
You must respond promptly, accurately, and professionally.

Example:
- If the JD is Software development, then the requirements are "Experimented 6+ Python", "2+ Java", "C++", etc.
  If the CV is related to the JD, then the fulfillments are "Experimented 6+ Python", "2+ Java", etc.

- If the JD is Data Science, then the requirements are "Experimented 6+ Python", "2+ Java", "C++", etc.
  If the CV is not related to the JD, then the fulfillments are empty.
'''
