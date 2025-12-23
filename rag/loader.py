from pathlib import Path


def load_documents() -> list:
    """
    Load all markdown source files from rag/sources into a list of
    {'source': str, 'content': str, 'rag_type': 'static'}.
    """
    sources_dir = Path(__file__).parent / "sources"
    docs = []

    for path in sources_dir.glob("*.md"):
        try:
            content = path.read_text(encoding="utf-8").strip()
        except OSError:
            continue

        if content:
            docs.append({
                "source": path.name,
                "content": content,
                "rag_type": "static",
            })

    return docs

