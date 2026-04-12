"""
Add commerce-extension, logistics-extension, financial-product, insurance-product,
and equipment-finance sponsor/investor opportunities to all catalog entries
that currently have none. Covers all remaining sectors systematically.
"""
# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.
import re, yaml
from pathlib import Path

def add_opp(slug, opp):
    f = Path(f"catalog/scenarios/{slug}.yaml")
    if not f.exists():
        print(f"  SKIP (not found): {slug}")
        return
    text = f.read_text(encoding="utf-8")
    block = (
        f'  - title: "{opp["title"]}"\n'
        f'    type: {opp["type"]}\n'
        f'    revenue_model: "{opp["revenue_model"]}"\n'
        f'    strategic_logic: "{opp["strategic_logic"]}"\n'
        f'    recurring: {str(opp["recurring"]).lower()}\n'
        "\n"
    )
    story_match = re.search(r"^story:", text, re.MULTILINE)
    if not story_match:
        print(f"  ERROR: no story: in {slug}")
        return
    new_text = text[:story_match.start()] + block + text[story_match.start():]
    f.write_text(new_text, encoding="utf-8")
    print(f"  OK: {slug}")

data = yaml.safe_load(Path("scripts/_all_extension_data.yaml").read_text(encoding="utf-8"))
additions = data["additions"]

for item in additions:
    add_opp(item["slug"], item["opp"])

print(f"\nDone. {len(additions)} opportunities applied.")
