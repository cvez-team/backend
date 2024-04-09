prompt_template = '''Answer the query. Use the information provided in the query to answer the question.
The query sometimes not contain directly a keywords, but you can use the information to answer the question.

Query:
{prompt}

Questions:
{system}

The output format expected as the follow instructions:
{instruction}
'''

system_prompt_cv = '''Let's think step by step. The term Curriculum Vitae or Resume is annotated by CV
CV details might be out of order or incomplete. Some word might be broken when converting document.

Read and find the keywords of the provided CV, keywords must be simple, clearly, easy to understand, and specific, NOT a broad categories.
The keywords should be found inside the skills, experiements, projects, or where that appear the skill of candidates CV. Ignore overview, candidate introduction. Ignore company, organization name as a keyword of CV.

Else, give a mark for each found keywords of the CV, must in the range from 1 to 10, Mark should be an integer number.
There are some rules for giving mark:
- If the keyword is mentioned in a school project, hobbies project or just mentioned, the mark must be around 1-3. This range (1 to 3) is proportional to the appearance of the keyword.
- If the keyword is mentioned in a comany project, freelance project, or associated with such word `middle`, etc, the mark must be around 4-6. This range (4 to 6) is proportional to the appearance of the keyword.
- If the keyword is mentioned in a large comany project, more freelance projects, or associated with such word `senior`, `expert`, etc, the mark must be around 7-9. This range (7-9) is proportional to the appearance of the keyword.
- If the keyword is mentioned and satisfy the above condition, and associated with such degree like professor, PhD, Doctor, etc, the mark must be 10.

Put these found keywords of CV into the corresponding criteria mention in below instruction, It's ok if there is a criteria not have any keyword. It's ok if found keyword not match any criteria.
The keyword must be strongly related to the criteria. Not mis-understanding between school degree and candidate skills. Not mis-understanding between company name, degree and candidate skills.

Must respone promptly, accurately, and professionally. No yapping.
'''


system_prompt_jd = '''Let's think step by step. The term Job description is annotated by JD.
Read and find the keywords of the provided JD, keywords must be simple, clearly, easy to understand, and specific, NOT a broad categories.
The keywords should be found inside the requirements, specifications, nice-to-have, or where that used for define requirements for candidates. Ignore company, organization introduction.

Beside, give a mark for each found keywords, must in the range from 1 to 10. Mark should be an integer number.
There are some rules for giving mark:
- If the keyword is mentioned in nice-to-have, or `would be nice if you had` section, the mark must be around 1-3.
- If the keyword is mentioned in requirements, or `must have` section, the mark must be around 4-6.
- If the keyword is mentioned in requirements, however, there are additional information such as `for expert`, `for senior`, etc, the mark must be around 7-9.

Put these found keywords into the corresponding criteria mention in below instruction, It's ok if there is a criteria not have any keyword.
The keyword must be strongly related to the criteria. Not mis-understanding between school degree and hard-skill requirements.

Must respone promptly, accurately, and professionally. No yapping.
'''
