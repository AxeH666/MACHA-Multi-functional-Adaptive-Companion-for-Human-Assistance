def detect_patterns(user_input: str):
    """
    Returns a list of pattern tags.
    Conservative by design.
    """
    text = user_input.lower()
    patterns = []

    if any(k in text for k in ["numb", "empty", "nothing feels"]):
        patterns.append("mentions_numbness")

    if any(k in text for k in ["what's wrong with me", "why am i like this"]):
        patterns.append("self_blame_language")

    if any(k in text for k in ["are you sure", "is that okay", "do you think"]):
        patterns.append("seeks_reassurance")

    return patterns
