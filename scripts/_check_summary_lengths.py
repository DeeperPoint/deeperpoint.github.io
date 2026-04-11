import yaml
from pathlib import Path

files = sorted(Path('catalog/scenarios').glob('*.yaml'))
rows = []
for f in files:
    d = yaml.safe_load(f.read_text(encoding='utf-8'))
    if d.get('hidden') or d.get('status') != 'published':
        continue
    summary = d.get('market_example', {}).get('summary', '')
    rows.append((len(summary.split()), d.get('sector',''), f.stem, summary[:80]))

rows.sort(key=lambda r: -r[0])
print(f"{'Words':>5}  {'Sector':<35}  {'Slug'}")
print('-' * 90)
for words, sector, slug, preview in rows:
    print(f"{words:>5}  {sector:<35}  {slug}")
