def rank_candidates(candidates: list) -> list:
    """
    Input:
    [
        {"name": "Mohab",  "score": 72, "summary": "..."},
        {"name": "Nagar",   "score": 91, "summary": "..."},
        {"name": "Malak",   "score": 85, "summary": "..."},
    ]
    Output: same list sorted highest score first
    """
    if not candidates:
        return []
    
    ranked = sorted(candidates, key=lambda x: x["score"], reverse=True)
    
    # Add rank number to each candidate
    for i, candidate in enumerate(ranked):
        candidate["rank"] = i + 1
    
    return ranked


def get_top_candidates(candidates: list, top_n: int = 5) -> list:
    """Get only the top N candidates"""
    ranked = rank_candidates(candidates)
    return ranked[:top_n]


if __name__ == "__main__":
    print("Ranker ready")
