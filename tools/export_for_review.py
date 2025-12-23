import json
import csv
from pathlib import Path

RAW_PROMPTS = Path("data/raw/phase1_prompts.jsonl")
OUT_CSV = Path("data/raw/phase1_review_sheet.csv")

fields = [
    "id",
    "user_input",
    "final_assistant_response",
    "notes"
]

rows = []

with open(RAW_PROMPTS, "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        rows.append({
            "id": item.get("id"),
            "user_input": item.get("user_input"),
            "final_assistant_response": "",
            "notes": ""
        })

with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"Export complete → {OUT_CSV}")
print("Share this CSV with the psychologist for Phase 1 authoring.")
