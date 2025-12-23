import requests

WIKI_API_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"

def fetch_wikipedia_summary(query: str):
    """
    Fetch a neutral summary from Wikipedia.
    Returns None if the page does not exist or is ambiguous.
    """

    title = query.strip().replace(" ", "_")

    try:
        response = requests.get(
            WIKI_API_URL + title,
            headers={"User-Agent": "MACHA/1.0"}
        )

        if response.status_code != 200:
            return None

        data = response.json()

        # Reject disambiguation or empty pages
        if data.get("type") == "disambiguation":
            return None

        extract = data.get("extract")
        if not extract or len(extract) < 50:
            return None

        return {
            "content": extract,
            "source": "Wikipedia",
            "confidence": "medium",
            "rag_type": "wikipedia",
        }

    except Exception:
        return None
