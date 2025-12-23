import csv
import json
from pathlib import Path

IN_CSV = Path("data/raw/phase1_review_sheet.csv")
OUT_JSONL = Path("data/reviewed/phase1_authoritative.jsonl")

with open(IN_CSV, "r", encoding="utf-8") as f, open(OUT_JSONL, "w", encoding="utf-8") as out:
    reader = csv.DictReader(f)
    for row in reader:
        if not row["final_assistant_response"].strip():
            continue  # skip unfilled rows
        record = {
            "messages": [
                {"role": "user", "content": row["user_input"]},
                {"role": "assistant", "content": row["final_assistant_response"]}
            ],
            "notes": row.get("notes", "")
        }
        out.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"Ingest complete → {OUT_JSONL}")
