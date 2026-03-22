"""
Swap dates on Series 2 and Series 3 so index order is correct:
  1. S1 B2B Middle Power                       2026-03-25
  2. S2 Siren Song Flexible Specialization     2026-03-24
  3. S3 AI Flex Spec Ontario                   2026-03-23
  4. S4 New Frontier Cooperative               2026-03-22
"""
import re, os

DST_DIR = r'c:\Users\MustafaUzumeri\GitHub\deeperpoint.github.io\blog\posts'

SERIES_DATES = {
    'flexible-specialization':    '2026-03-24',
    'ai-flex-spec-manufacturing': '2026-03-23',
}

for fname in os.listdir(DST_DIR):
    if not fname.endswith('.md'):
        continue
    path = os.path.join(DST_DIR, fname)
    with open(path, encoding='utf-8') as f:
        content = f.read()
    for series_slug, new_date in SERIES_DATES.items():
        if 'series: ' + series_slug in content:
            updated = re.sub(r'^date: \d{4}-\d{2}-\d{2}', 'date: ' + new_date,
                             content, flags=re.MULTILINE)
            if updated != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(updated)
                print(f'{fname}  ->  {new_date}')
            break

print('Done.')
