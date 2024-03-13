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
Degree is a Educational qualifications required, e.g., Bachelor's degree in Computer Science.
Experience should include required duration time and job name field of work. Experiences required at position.
Only use the given data to determine educational qualifications and certificates; do not make assumptions about these qualifications.
Soft skills required for the job, inferred from the provided information. However, you are allowed to combine the provided details to draw logical conclusions about soft skills.
Must respone promptly, accurately, and professionally.
Expected structure output must like this:
{
    "Degree": []
    "Experience": []
    "TechnicalSkills": []
    "Responsibilities": []
    "Certifications": []
    "SoftSkills": []
}
'''

# system_prompt_question = '''
# Let's think step by step.
# Act as an interviewer, preprocess the question and extract the keywords from the question. Example: "What is your troubleshooting process?" ->"Problem-solving", "Tell us about a time you took the lead on a project." -> "Leadership", "What is an IP Address?" -> "Networking".
# Must summarize the keywords in simple keywords or short phrases e.g. "3 years", "5+ years" or "2-3 years".
# Must remove any irrelevant or duplicate keywords from the extracted keywords that are having the same meaning or context.
# Must categorize extracted keywords into degrees, experience, technical skills, responsibilities, certifications, and soft skills based on the context of the question.
# Must respond promptly, accurately, and professionally.
# Must not be biased or make assumptions about the question.
# '''

system_prompt_question = '''
Let's think step by step.
Preprocess the question and extract the relevant fields from the question e.g. "What is your troubleshooting process?" ->"Problem-solving".
Must find semantically similar keywords and remove any irrelevant or duplicate keywords from the extracted keywords that are having the same meaning or context.
Must summarize the extracted keywords in simple keywords or short phrases.
If it is not clear, you must infer relevant fields from the comparative nature of the question.
Avoid using broad categories for technical skills.
Using more granular keywords is encouraged.
Question can have multiple keywords.
Must respone promptly, accurately, and professionally.
Must not be biased or make assumptions about the question.
General format:
{
  "Degree": [], // e.g. ["B.Tech", "M.Tech", "M.Sc", "Ph.D", etc.]
  "Experience": [], // e.g. ["3 years experience in NLP", "5+ years experience in Python", "2-3 years experience in Java", etc.]
  "TechnicalSkills": [], // <More granular keywords> e.g. ["Networking", "Protocols", "Python", "Vue.js", etc.]
  "Responsibilities": [], // e.g. ["Developing software", "Troubleshooting", "Testing", "Debugging", etc.]
  "Certifications": [], // <Inferred from the comparative nature> e.g. ["CCNA", "CCNP", "CCIE", "AWS", "Azure", "GCP", etc.]
  "SoftSkills": [], // <Inferred from the comparative nature> e.g. ["Analytical Thinking", "Leadership", "Problem-solving", "Teamwork", etc.]
  "Summary": "" // <Summary of the question>
}
'''