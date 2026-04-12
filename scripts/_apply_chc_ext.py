import re, yaml
from pathlib import Path

def add_opp(slug, opp):
    f = Path(f"catalog/scenarios/{slug}.yaml")
    text = f.read_text(encoding="utf-8")
    block = (
        f"  - title: \"{opp['title']}\"\n"
        f"    type: {opp['type']}\n"
        f"    revenue_model: \"{opp['revenue_model']}\"\n"
        f"    strategic_logic: \"{opp['strategic_logic']}\"\n"
        f"    recurring: {str(opp['recurring']).lower()}\n\n"
    )
    story_match = re.search(r"^story:", text, re.MULTILINE)
    new_text = text[:story_match.start()] + block + text[story_match.start():]
    f.write_text(new_text, encoding="utf-8")
    print(f"  OK: {slug}")

data = yaml.safe_load(Path("scripts/_chc_extension_data.yaml").read_text(encoding="utf-8"))
for item in data["additions"]:
    add_opp(item["slug"], item["opp"])
print("Done.")
