import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.router import detect_mode
from core.llm import generate_reply
from memory.store import save_turn
from memory.memory_manager import SessionMemory, PatternMemory
from memory.pattern_detector import detect_patterns

from rag.router import classify_query, should_use_api
from rag.loader import load_documents
from rag.retrieval_pipeline import get_rag_context

# Initialize memory objects
session_memory = SessionMemory(max_turns=12)
pattern_memory = PatternMemory()

# Load RAG documents once
documents = load_documents()

def run():
    print("MACHA is here. Type 'exit' to stop.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        clean_input = user_input.strip()

        # ---- Classify query ----
        query_type = classify_query(clean_input)

        # ---- Fact / news queries: build RAG context or refuse ----
        rag_chunks = []
        if query_type in ["stable_fact", "volatile_fact"]:
            rag_chunks = get_rag_context(clean_input, query_type, documents)

            if rag_chunks:
                rag_types = {c.get("rag_type", "unknown") for c in rag_chunks}
                sources = [c.get("source", "Unknown") for c in rag_chunks]
                print(f"[DEBUG] query_type={query_type}")
                print(f"[DEBUG] RAG types used: {sorted(rag_types)}")
                print(f"[DEBUG] RAG sources: {sources}")
            else:
                print(f"[DEBUG] query_type={query_type}")
                print("[DEBUG] No RAG used")
                print(
                    "\nMACHA: I don’t have reliable or up-to-date information on that right now. "
                    "For important updates, please check established news or official sources.\n"
                )
                continue

        # ---- Layer 2: Observe patterns ----
        detected_patterns = detect_patterns(clean_input)
        for tag in detected_patterns:
            pattern_memory.observe(tag)

        # ---- Generate reply ----
        mode = detect_mode(clean_input)
        reply = generate_reply(
            clean_input,
            mode,
            rag_chunks=rag_chunks
        )

        # ---- Layer 1: Store session turn ----
        session_memory.add_turn(user_input, reply)
        save_turn(user_input, reply)

        print(f"\nMACHA: {reply}\n")

if __name__ == "__main__":
    run()
