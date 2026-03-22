"""
Fix series ordering on blog index by adjusting post dates.
Target display order (newest first on index):
  1st: S1 B2B Middle Power           -> max date 2026-03-25
  2nd: S3 AI Flex Spec Ontario        -> max date 2026-03-24
  3rd: S2 Siren Song Flex Spec        -> max date 2026-03-23
  4th: S4 New Frontier Cooperative    -> max date 2026-03-22 (already correct - no change)
"""
import re, os

DST_DIR = r'c:\Users\MustafaUzumeri\GitHub\deeperpoint.github.io\blog\posts'

# series slug -> new date to apply to ALL posts in that series
SERIES_DATES = {
    'middle-power-strategy':         '2026-03-25',
    'ai-flex-spec-manufacturing':    '2026-03-24',
    'flexible-specialization':       '2026-03-23',
    # ai-cooperative-manufacturing stays at 2026-03-22
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
                print(f'{fname}  ->  date: {new_date}')
            break

print('Done.')
