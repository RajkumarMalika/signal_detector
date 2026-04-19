import re
from typing import Optional, Dict, Any, Tuple, List
from datetime import datetime, timezone
from utils.scoring import calculate_signal_score

# 1. The rules for what we are looking for
COMPETITORS = ["hackerrank", "hirevue", "codility", "testdome"]

PAIN_POINTS_MAP = {
    "expensive": "Cost",
    "slow process": "Efficiency",
    "bias": "Fairness",
    "terrible": "Customer Experience",
    "awful": "Customer Experience",
    "waste": "Efficiency",
    "bad": "General Grievance",
    "hate": "General Grievance",
    "lazy": "Efficiency",          # ADDED for this thread
    "disrespectful": "Fairness",   # ADDED for this thread
    "red flag": "General Grievance"
}

# 2. Pre-compile Regex for fast, exact-word matching
COMPILED_NEGATIVES = {
    phrase: re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE)
    for phrase in PAIN_POINTS_MAP.keys()
}

def process_grievance_signal(raw_data_record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Analyzes text and outputs a structured signal JSON if rules are met."""
    content = raw_data_record.get("content", "").lower()
    
    if not content:
        return None
        
    # 3. Find competitors
    found_competitors = [comp for comp in COMPETITORS if comp in content]
    
    # 4. Find negative pain points
    found_negatives = []
    mapped_pain_points = set()
    
    for phrase, pattern in COMPILED_NEGATIVES.items():
        if pattern.search(content):
            found_negatives.append(phrase)
            mapped_pain_points.add(PAIN_POINTS_MAP[phrase])
            
    # 5. Gatekeeper: Only proceed if BOTH exist
    if not found_competitors or not found_negatives:
        return None 
        
    # 6. Format the final output
    score = calculate_signal_score(found_competitors, found_negatives)
    
    return {
        "company": raw_data_record.get("company_name"),
        "signal_type": "competitor_grievance",
        "source_url": raw_data_record.get("source_url"),
        "matched_keywords": found_competitors + found_negatives,
        "signal_score": score,
        "detected_at": datetime.now(timezone.utc).isoformat(),
        "reason": f"Negative feedback about {', '.join(found_competitors)} regarding {', '.join(mapped_pain_points)}",
        "extracted_pain_points": list(mapped_pain_points)
    }