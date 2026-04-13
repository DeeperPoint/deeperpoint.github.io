import json
from collections import defaultdict
from difflib import SequenceMatcher

with open('catalog_summary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('analysis_report.txt', 'w', encoding='utf-8') as out:
    out.write('=== CATEGORY 2: POTENTIAL DUPLICATES ===\n')
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            t1, t2 = data[i]['title'], data[j]['title']
            ratio = SequenceMatcher(None, t1, t2).ratio()
            if ratio > 0.80:
                out.write(f"Match {ratio:.2f}:\n - {data[i]['id']}: {t1}\n - {data[j]['id']}: {t2}\n")

    out.write('\n=== CATEGORY 3: SECTOR GROUPINGS (Amalgamations) ===\n')
    sectors = defaultdict(list)
    for d in data:
        sectors[d['sector']].append((d['id'], d['title']))

    for sec, items in sorted(sectors.items(), key=lambda x: len(x[1]), reverse=True):
        out.write(f"\nSector: {sec} ({len(items)} items)\n")
        for idx, title in items:
            out.write(f"  - {idx}: {title}\n")

    out.write('\n=== CATEGORY 1: SMALL UPSIDE MARKETS ===\n')
    for d in data:
        upside = d.get('upside', '')
        # Check for smaller market indicators (e.g. hundreds of thousands or fewer than $5M)
        if '100,000' in upside or '500,000' in upside or 'small' in upside.lower():
            out.write(f"- {d['id']}: {d['title']}\n  Upside snippet: {upside[:150]}...\n")

print("Analysis complete.")
