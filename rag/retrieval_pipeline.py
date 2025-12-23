from rag.retriever import retrieve
from rag.apis.wikipedia import fetch_wikipedia_summary
from rag.apis.news import fetch_news


def get_rag_context(query: str, query_type: str, static_documents: list):
    # 1️⃣ Static RAG
    static_chunks = retrieve(query, static_documents)
    if static_chunks:
        return static_chunks

    # 2️⃣ Wikipedia for stable facts
    if query_type == "stable_fact":
        wiki = fetch_wikipedia_summary(query)
        if wiki:
            return [wiki]

    # 3️⃣ News API for volatile facts
    if query_type == "volatile_fact":
        news = fetch_news(query)
        if news:
            return news

    return []
