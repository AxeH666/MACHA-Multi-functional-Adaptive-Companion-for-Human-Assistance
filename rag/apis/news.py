import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

def fetch_news(query: str, max_articles: int = 3):
    """
    Fetch recent news articles for a query.
    Returns a list of neutral summaries or None.
    """

    if not NEWS_API_KEY:
        return None

    try:
        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": max_articles,
            "apiKey": NEWS_API_KEY
        }

        response = requests.get(NEWS_API_URL, params=params)

        if response.status_code != 200:
            return None

        data = response.json()
        articles = data.get("articles", [])

        if not articles:
            return None

        chunks = []
        for article in articles:
            if not article.get("description"):
                continue

            chunks.append({
                "content": (
                    f"{article['description']} "
                    f"(Source: {article['source']['name']}, "
                    f"Published: {article['publishedAt']})"
                ),
                "source": article["source"]["name"],
                "confidence": "medium",
                "rag_type": "news",
            })

        return chunks if chunks else None

    except Exception:
        return None
