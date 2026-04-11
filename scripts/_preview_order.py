import yaml
from pathlib import Path
from collections import OrderedDict

files = sorted(Path('catalog/scenarios').glob('*.yaml'))
scenarios = []
for f in files:
    d = yaml.safe_load(f.read_text(encoding='utf-8'))
    if not d.get('hidden') and d.get('status') == 'published':
        scenarios.append(d)

buckets = OrderedDict()
for s in scenarios:
    sec = s.get('sector', 'other')
    if sec not in buckets:
        buckets[sec] = []
    buckets[sec].append(s)

result = []
queues = list(buckets.values())
while any(q for q in queues):
    for q in queues:
        if q:
            result.append(q.pop(0))

for i, s in enumerate(result[:24]):
    sec = s.get('sector', '')[:28]
    ct = s.get('card_title', s.get('title', ''))[:48]
    print(f"{i+1:>3}. [{sec:<28}]  {ct}")
