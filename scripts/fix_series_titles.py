"""Fix series-title fields for Series 1 and Series 2."""
import re, os

DST_DIR = r'c:\Users\MustafaUzumeri\GitHub\deeperpoint.github.io\blog\posts'

FIXES = {
    'middle-power-strategy':    'B2B in a Middle Power World',
    'flexible-specialization':  'The Siren Song of Flexible Specialization',
}

for fname in os.listdir(DST_DIR):
    if not fname.endswith('.md'):
        continue
    path = os.path.join(DST_DIR, fname)
    with open(path, encoding='utf-8') as f:
        content = f.read()
    for series_slug, new_title in FIXES.items():
        if 'series: ' + series_slug in content:
            content = re.sub(
                r'^series-title: .*',
                'series-title: "' + new_title + '"',
                content, flags=re.MULTILINE
            )
            print(f'{fname}  ->  "{new_title}"')
            break
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Done.')
