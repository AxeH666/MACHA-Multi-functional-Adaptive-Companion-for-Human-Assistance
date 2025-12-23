def detect_mode(user_input: str) -> str:
    text = user_input.lower()

    if any(k in text for k in ["fact check", "is it true", "research says"]):
        return "fact"

    if any(k in text for k in ["why do i", "pattern", "understand myself"]):
        return "reflect"

    if any(k in text for k in ["overwhelmed", "numb", "empty", "can't handle"]):
        return "support"

    return "support"
