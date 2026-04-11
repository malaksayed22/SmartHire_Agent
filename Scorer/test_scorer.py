from resume_reader import extract_text
from scorer import score_resume

#Read CV
print("Reading CV...")
resume_text = extract_text("D:/Nour El-Rouby CV.pdf")
print("CV loaded successfully")

#Define a job description
job_description = """
We are looking for a AI Engineer with:
- Strong Python programming skills
- Experience with Machine Learning and Deep Learning
- Knowledge of NLP and text processing
- Experience with data visualization tools
- Familiarity with REST APIs and web scraping
- Good communication skills
- Bachelor's degree in Computer Science or related field
"""

#Score the resume
print("\n(Scoring your CV against the job)")
result = score_resume(resume_text, job_description)

#result
print("\n==========> SCORING RESULT <==========")
print(f"Score:    {result['score']} / 100")
print(f"\nSummary:  {result['summary']}")
print("\nStrengths:")
for s in result['strengths']:
    print(f"  + {s}")
print("\nWeaknesses:")
for w in result['weaknesses']:
    print(f"  - {w}")
print("=====================================")