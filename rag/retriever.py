from typing import List, Dict


def retrieve(query: str, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    A minimal lexical retriever: returns documents that contain any
    query term. If nothing matches, return an empty list.
    """
    if not documents:
        return []

    terms = {t for t in query.lower().split() if t}
    results: List[Dict[str, str]] = []

    for doc in documents:
        content_lower = doc["content"].lower()
        if any(term in content_lower for term in terms):
            results.append(doc)

    return results


