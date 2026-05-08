import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume_reader import extract_text
from Scorer.scorer import score_resume


print("Reading CV...")
resume_text = extract_text("D:/Nour El-Rouby CV.pdf")
print("CV loaded successfully")

job_description = """
We are looking for an AI Engineer / LLM Specialist with:
- Strong Python programming skills
- Experience with Machine Learning and Deep Learning
- Knowledge of NLP and text processing
- Experience with data visualization tools
- Familiarity with REST APIs and web scraping
- Good communication skills
- Bachelor's degree in Computer Science or related field
"""

print("\nScoring your CV against the job...")
result = score_resume(resume_text, job_description)

print("\n=========> SCORING RESULT <=========")
print(f"Score:               {result['score']} / 100")
print(f"Experience Level:    {result['experience_level']}")
print(f"Recommended Action:  {result['recommended_action']}")
print(f"\nSummary:\n  {result['summary']}")

print("\nStrengths:")
for s in result["strengths"]:
    print(f"  + {s}")

print("\nWeaknesses:")
for w in result["weaknesses"]:
    print(f"  - {w}")

print("=====================================")