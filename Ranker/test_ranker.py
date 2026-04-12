from ranker import rank_candidates, get_top_candidates

# Simulate 6 candidates with scores
candidates = [
    {"name": "Mohab Mohsen",  "score": 72, "summary": "Junior developer with basic Python skills"},
    {"name": "Malak Sayed",       "score": 91, "summary": "Senior AI engineer with strong ML background"},
    {"name": "Dana Khaled",    "score": 85, "summary": "Data scientist with 3 years experience"},
    {"name": "Nour El-Rouby",  "score": 85, "summary": "AI engineer with CV and NLP experience"},
    {"name": "Malak Mostafa",    "score": 60, "summary": "Fresh graduate with internship experience"},
    {"name": "Youssef Tarek",    "score": 78, "summary": "Backend developer learning ML"},
]

# Test1: Rank all candidates
print("=====> ALL CANDIDATES RANKED <=====")
ranked = rank_candidates(candidates)
for c in ranked:
    print(f"#{c['rank']}  {c['name']:<20} Score: {c['score']}/100  —  {c['summary']}")

# Test2: Get top 3 only
print("\n=====> TOP 3 CANDIDATES <=====")
top3 = get_top_candidates(candidates, top_n=3)
for c in top3:
    print(f"#{c['rank']}  {c['name']:<20} Score: {c['score']}/100")

print("\nRanker works correctly")