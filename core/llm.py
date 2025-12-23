from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

from openai import OpenAI
from prompts.system import WISE_FRIEND_SYSTEM_PROMPT

client = OpenAI()


def generate_reply(
    user_input: str,
    mode: str,
    rag_chunks: list | None = None
) -> str:
    """
    Generate a reply using OpenAI with optional RAG grounding.
    This function is model-agnostic and safe for later swap to Mistral.
    """

    mode_instruction = {
        "support": (
            "Be emotionally present and grounded. "
            "Do not analyze deeply or diagnose. "
            "Focus on listening and gentle validation."
        ),
        "reflect": (
            "Offer gentle reflection without interpretation. "
            "Avoid conclusions. Ask at most one open-ended question."
        ),
        "fact": (
            "Be neutral and precise. "
            "Prefer accuracy over completeness. "
            "If information may be outdated, evolving, or uncertain, say so clearly. "
            "Encourage verification with reliable external sources."
        )
    }[mode]

    messages = [
        {"role": "system", "content": WISE_FRIEND_SYSTEM_PROMPT},
        {"role": "system", "content": mode_instruction},
    ]

    # ---------- RAG INJECTION ----------
    if rag_chunks:
        rag_context = "\n\n".join(
            f"[Source: {chunk.get('source', 'Unknown')}]\n{chunk.get('content', '')}"
            for chunk in rag_chunks
        )

        messages.append({
            "role": "system",
            "content": (
                "The following information is provided for factual grounding only.\n"
                "- Do NOT diagnose, personalize, or provide medical, legal, or financial advice.\n"
                "- Information from news or external sources may change over time.\n"
                "- If the information is incomplete, conflicting, or uncertain, say so explicitly.\n"
                "- Encourage users to verify important facts with reliable sources.\n\n"
                f"{rag_context}"
            )
        })
    # -----------------------------------

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.6
    )

    return response.choices[0].message.content
