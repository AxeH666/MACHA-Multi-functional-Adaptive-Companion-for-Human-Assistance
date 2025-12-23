from collections import deque, defaultdict
from typing import List, Dict

# -------------------------------
# Layer 1: Session Memory
# -------------------------------

class SessionMemory:
    def __init__(self, max_turns: int = 12):
        self.max_turns = max_turns
        self.turns = deque(maxlen=max_turns)

    def add_turn(self, user_input: str, assistant_response: str):
        self.turns.append({
            "user": user_input,
            "assistant": assistant_response
        })

    def get_recent_context(self) -> List[Dict[str, str]]:
        """
        Returns raw recent turns.
        Used ONLY for coherence.
        """
        return list(self.turns)

    def clear(self):
        self.turns.clear()
# -------------------------------
# Layer 2: Pattern Memory
# -------------------------------

class PatternMemory:
    def __init__(self):
        # pattern_name -> count
        self.pattern_counts = defaultdict(int)

    def observe(self, pattern_tag: str):
        """
        pattern_tag examples:
        - mentions_numbness
        - self_blame_language
        - seeks_reassurance
        """
        self.pattern_counts[pattern_tag] += 1

    def get_patterns(self, threshold: int = 3) -> Dict[str, int]:
        """
        Return only patterns that repeat enough
        to be meaningful.
        """
        return {
            tag: count
            for tag, count in self.pattern_counts.items()
            if count >= threshold
        }

    def reset(self):
        self.pattern_counts.clear()
