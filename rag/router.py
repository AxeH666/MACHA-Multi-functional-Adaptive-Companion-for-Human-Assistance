STABLE_FACT_TRIGGERS = [
    "what is",
    "explain",
    "define",
    "meaning of",
    "how does",
    "difference between"
]

VOLATILE_FACT_TRIGGERS = [
    "latest",
    "current",
    "today",
    "right now",
    "recent",
    "news",
    "update",
    "rate",
    "statistics",
    "percentage"
]

def classify_query(text: str) -> str:
    t = text.lower()

    if any(x in t for x in VOLATILE_FACT_TRIGGERS):
        return "volatile_fact"
    if any(x in t for x in STABLE_FACT_TRIGGERS):
        return "stable_fact"
    return "opinion_or_reflection"


def should_use_api(query_type: str) -> bool:
    """
    Decide whether to call external APIs (e.g., news/wikipedia) based on query type.
    """
    return query_type in ["stable_fact", "volatile_fact"]
