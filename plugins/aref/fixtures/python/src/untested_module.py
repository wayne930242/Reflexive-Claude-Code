def compute_priority_score(severity: int, impact: int, confidence: float) -> int:
    raw = severity * impact * confidence
    if raw > 100:
        return 100
    if raw < 0:
        return 0
    return round(raw)
