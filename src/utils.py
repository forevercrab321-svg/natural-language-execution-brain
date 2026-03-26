"""Utility functions for intent parsing."""

import re
from typing import List, Set, Tuple


def contains_any_keyword(text: str, keywords: List[str], case_sensitive: bool = False) -> bool:
    """Check if text contains any of the keywords."""
    if not case_sensitive:
        text = text.lower()
        keywords = [k.lower() for k in keywords]
    return any(kw in text for kw in keywords)


def extract_keywords(text: str, keywords: List[str], case_sensitive: bool = False) -> List[str]:
    """Extract keywords found in text."""
    if not case_sensitive:
        text = text.lower()
        keywords = [k.lower() for k in keywords]
    found = [kw for kw in keywords if kw in text]
    seen: Set[str] = set()
    result = []
    for kw in found:
        if kw not in seen:
            seen.add(kw)
            result.append(kw)
    return result


def find_pattern_matches(text: str, pattern: str, flags: int = re.IGNORECASE) -> List[str]:
    """Find all matches of a regex pattern."""
    matches = re.findall(pattern, text, flags=flags)
    return matches if matches else []


def detect_emotional_language(text: str) -> Tuple[bool, List[str]]:
    """Detect emotional or frustrated language markers."""
    emotional_patterns = [
        r"别|别老|不要|不再",
        r"直接|马上|立刻|现在",
        r"方向不对|跑偏|没理解|没听懂",
        r"就是|都|一直|老是",
    ]
    
    markers = []
    for pattern in emotional_patterns:
        matches = find_pattern_matches(text, pattern)
        markers.extend(matches)
    
    is_emotional = len(markers) > 0
    return is_emotional, list(set(markers))


def normalize_text(text: str) -> str:
    """Normalize text for processing."""
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_quoted_content(text: str) -> List[str]:
    """Extract content within quotes."""
    patterns = [
        r'"([^"]*)"',
        r"'([^']*)'",
        r'「([^」]*)」',
        r'『([^』]*)』',
        r'"([^"]*)"',
        r'"([^"]*)"',
    ]
    
    content = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        content.extend(matches)
    return content


def is_approval_needed(text: str, keywords: List[str]) -> bool:
    """Check if approval is needed based on keywords."""
    return any(kw in text for kw in keywords)


def infer_urgency(text: str) -> str:
    """Infer urgency level from text."""
    high_urgency_patterns = [
        r"立刻|马上|现在|urgent|asap|immediately",
        r"紧急|紧急的",
    ]
    
    for pattern in high_urgency_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return "high"
    
    return "normal"


def infer_confidence(
    explicit_requests: int,
    implied_goals: int,
    ambiguity_count: int,
) -> float:
    """Infer confidence in interpretation."""
    base = min(0.95, 0.70 + explicit_requests * 0.05)
    alignment_bonus = implied_goals * 0.02 if implied_goals > 0 else 0
    ambiguity_penalty = ambiguity_count * 0.08
    
    confidence = max(0.5, min(1.0, base + alignment_bonus - ambiguity_penalty))
    return round(confidence, 2)


def split_sentence_blocks(text: str) -> List[str]:
    """Split text into logical sentence blocks."""
    blocks = re.split(r'[。！？!?；;]\s*', text)
    return [b.strip() for b in blocks if b.strip()]


def count_negations(text: str) -> int:
    """Count negation markers."""
    negation_patterns = [
        r"别|别老|别再|不要|不会|不能",
        r"没有|没有|没",
    ]
    count = 0
    for pattern in negation_patterns:
        matches = find_pattern_matches(text, pattern)
        count += len(matches)
    return count


def detect_approval_keywords_in_text(text: str, keywords: List[str]) -> List[str]:
    """Detect and return approval-related keywords found in text."""
    found = []
    for kw in keywords:
        if kw in text:
            found.append(kw)
    seen = set()
    result = []
    for item in found:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
