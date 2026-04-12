"""Audit extension coverage across all catalog entries."""
import yaml, glob
from pathlib import Path

EXT_TYPES = {'commerce-extension', 'logistics-extension', 'financial-product',
             'insurance-product', 'equipment-finance'}

results = {}
for f in sorted(glob.glob('catalog/scenarios/*.yaml')):
    d = yaml.safe_load(Path(f).read_text(encoding='utf-8'))
    opps = d.get('sponsor_opportunities', [])
    types = [o.get('type', '?') for o in opps]
    has_ext = any(t in EXT_TYPES for t in types)
    sector = d.get('sector', '?')
    slug = Path(f).stem
    results.setdefault(sector, {'entries': 0, 'with_ext': 0, 'no_ext': []})
    results[sector]['entries'] += 1
    if has_ext:
        results[sector]['with_ext'] += 1
    else:
        results[sector]['no_ext'].append(slug)

for sec, r in sorted(results.items()):
    no_ext = r['no_ext']
    print(f"\n{sec}: {r['with_ext']}/{r['entries']} have extensions")
    for s in no_ext:
        print(f"  - {s}")
