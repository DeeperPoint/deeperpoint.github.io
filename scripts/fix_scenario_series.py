"""
Move the 4 manufacturing scenario posts into Series 4 (ai-cooperative-manufacturing),
assigning them positions 2-5.
"""
import re, os

DST_DIR = r'c:\Users\MustafaUzumeri\GitHub\deeperpoint.github.io\blog\posts'

FILES = [
    ('used-machinery-thin-market',       2),
    ('manufacturing-scenarios-testing',  3),
    ('manufacturing-scenarios-skills',   4),
    ('manufacturing-scenarios-capacity', 5),
]

NEW_SERIES       = 'ai-cooperative-manufacturing'
NEW_SERIES_TITLE = 'New Frontier: AI Powered Cooperative Manufacturing'

for slug, pos in FILES:
    path = os.path.join(DST_DIR, slug + '.md')
    with open(path, encoding='utf-8') as f:
        content = f.read()

    content = re.sub(r'^series: \S+',
                     'series: ' + NEW_SERIES,
                     content, flags=re.MULTILINE)
    content = re.sub(r'^series-title: .*',
                     'series-title: "' + NEW_SERIES_TITLE + '"',
                     content, flags=re.MULTILINE)
    content = re.sub(r'^series-position: \d+',
                     'series-position: ' + str(pos),
                     content, flags=re.MULTILINE)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {slug}.md  ->  series-position: {pos}')

print('Done.')
