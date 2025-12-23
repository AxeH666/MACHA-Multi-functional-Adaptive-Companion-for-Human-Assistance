from typing import List, Dict


def should_refuse(is_fact_query: bool, rag_chunks: List[Dict[str, str]]) -> bool:
    """
    Refuse if a fact query has no supporting retrieval context.
    """
    if not is_fact_query:
        return False
    return len(rag_chunks) == 0


def uncertainty_response() -> str:
    return (
        "I don't have enough reliable information on that. "
        "Please verify with up-to-date, trustworthy sources."
    )


