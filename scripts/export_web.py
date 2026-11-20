"""Export the Excel word list to docs/data/words.json for the web app (GitHub Pages).

Run:  python scripts/export_web.py
The GitHub Action .github/workflows/web-data.yml runs this automatically when the
Excel file changes, so the web app always shows the same words as the Streamlit app.
"""
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
FILE = ROOT / "Nederlands_naar_perfectie_B2_C1_woordenschat.xlsx"
OUT = ROOT / "docs" / "data" / "words.json"


def clean(v) -> str:
    return "" if pd.isna(v) else str(v).strip()


df = pd.read_excel(FILE)
df.columns = [c.strip() for c in df.columns]
rows = []
for r in df.to_dict("records"):
    rows.append({
        "h": int(r["Hoofdstuk"]),
        "t": int(r["Tekst"]),
        "nl": clean(r["Dutch Word/Phrase"]),
        "en": clean(r["English Translation"]),
        # the sentences start with "- " in the Excel file
        "ex": re.sub(r"^-\s*", "", clean(r["ranscribed Dutch Sentence"])),
        "ex_en": re.sub(r"^-\s*", "", clean(r["Literary English Translation (for back translation)"])),
    })
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(rows, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"wrote {OUT}: {len(rows)} entries")
