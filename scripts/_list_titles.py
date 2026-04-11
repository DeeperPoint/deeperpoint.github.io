import yaml
from pathlib import Path
files = sorted(Path('catalog/scenarios').glob('*.yaml'))
for f in files:
    d = yaml.safe_load(f.read_text(encoding='utf-8'))
    if d.get('hidden'):
        continue
    if d.get('status') != 'published':
        continue
    print(f.stem + '|||' + d.get('title', ''))
