from agent import run_agent

JOB_DESCRIPTION = """
Job Title: AI Engineer
Company: TechCorp Egypt
Requirements:
- 2+ years Python experience
- Machine Learning and NLP knowledge
- REST API experience
- Computer Science degree
Salary: 15,000 - 25,000 EGP
Remote: Hybrid
"""

print("=" * 50)
print("Test 1  Score a real resume")
print("=" * 50)
result1 = run_agent(
    "score",
    file_path="D:/Nour El-Rouby CV.pdf",
    job_description=JOB_DESCRIPTION
)
print(f"\nFinal Score: {result1['result']['score']}/100")
print(f"Summary: {result1['result']['summary']}")

print("\n" + "=" * 50)
print("Test 2 Rank candidates")
print("=" * 50)
candidates = [
    {"name": "Nour El-Rouby", "score": 85, "summary": "AI engineer"},
    {"name": "Mohamed Elnaggar",      "score": 91, "summary": "Senior ML engineer"},
    {"name": "Mohab Mohsen", "score": 72, "summary": "Junior developer"},
    {"name": "Malak Sayed",   "score": 80, "summary": "Backend developer"},
]
result2 = run_agent("rank", candidates=candidates, top_n=3)
print("\nTop 3 Candidates:")
for c in result2['result']:
    print(f"  #{c['rank']} {c['name']} — {c['score']}/100")

print("\n" + "=" * 50)
print("TEST 3 — Chat about the job")
print("=" * 50)
result3 = run_agent(
    "chat",
    job_description=JOB_DESCRIPTION,
    question="What is the salary for this position?"
)
print(f"\nAnswer: {result3['result']['answer']}")

print("\n" + "=" * 50)
print("All Agent Tests Passed")
print("=" * 50)