import re
from typing import Set, Tuple, List

def validate_citations(text: str, valid_finding_ids: Set[str]) -> Tuple[bool, List[str]]:
    """
    Extracts all finding identifiers (e.g. FIND-001) from text and validates
    that they exist in the verified CBOM database.
    Returns (is_grounded, list_of_hallucinated_ids).
    """
    cited_ids = set(re.findall(r"FIND-\d{3}", text))
    hallucinated = [fid for fid in cited_ids if fid not in valid_finding_ids]
    is_grounded = len(hallucinated) == 0
    return is_grounded, hallucinated

def sanitize_response(text: str, valid_finding_ids: Set[str]) -> str:
    """
    Flags and redacts hallucinated finding IDs from generated text.
    """
    is_grounded, hallucinated = validate_citations(text, valid_finding_ids)
    sanitized = text
    for fake_id in hallucinated:
        sanitized = sanitized.replace(fake_id, f"[REDACTED_INVALID_ID: {fake_id}]")
    return sanitized
