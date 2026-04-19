from typing import List

def calculate_signal_score(competitor_matches: List[str], negative_matches: List[str]) -> int:
    """Calculates a confidence score (0-100) based on found keywords."""
    if not competitor_matches or not negative_matches:
        return 0
    
    base_score = 40
    keyword_bonus = len(negative_matches) * 20
    
    total_score = base_score + keyword_bonus
    return max(0, min(total_score, 100)) # Ensure score stays between 0 and 100