"""
Publish posts from DeeperPointBlogging to deeperpoint.github.io/blog/posts/
- Strips copyright comment
- Collapses multi-line YAML values
- Ensures summary is double-quoted
- Injects slug field
"""
import re
import os

SRC_DIR = r'c:\Users\MustafaUzumeri\GitHub\DeeperPointBlogging'
DST_DIR = r'c:\Users\MustafaUzumeri\GitHub\deeperpoint.github.io\blog\posts'

FILES = [
    ('2026-03-21-OntarioRoadmapPart1_Fractional.md',               'ontario-roadmap-part1-fractional'),
    ('2026-03-21-OntarioRoadmapPart2_Ecosystem.md',                'ontario-roadmap-part2-ecosystem'),
    ('2026-03-21-OntarioRoadmapPart3_Pocket.md',                   'ontario-roadmap-part3-pocket'),
    ('2026-03-21-OntarioRoadmapPart4_Orchestrating.md',            'ontario-roadmap-part4-orchestrating'),
    ('2026-03-22-OntarioRoadmapPart5_CooperativeSpecialization.md','ontario-roadmap-part5-cooperative-specialization'),
    ('2026-03-22-CoopSpecPart1_InsidetheFirm.md',                  'coopspec-part1-inside-the-firm'),
    ('2026-03-22-CoopSpecPart7_CooperativeWorkshop.md',            'coopspec-part7-cooperative-workshop'),
    ('2026-03-22-fsss-software-ecosystem.md',                      'csss-software-ecosystem'),
]


def process(src_name, slug):
    src_path = os.path.join(SRC_DIR, src_name)
    dst_path = os.path.join(DST_DIR, slug + '.md')

    with open(src_path, encoding='utf-8') as f:
        content = f.read()

    # Strip copyright comment at top
    content = re.sub(r'^<!--.*?-->\s*\n', '', content, flags=re.DOTALL)

    # Split on --- YAML delimiters
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        print(f'ERROR: YAML split failed for {src_name} (got {len(parts)} parts)')
        return

    yaml_block = parts[1].strip()
    body = parts[2]

    # Collapse multi-line YAML continuation lines into single lines
    yaml_lines = yaml_block.split('\n')
    collapsed = []
    for line in yaml_lines:
        if re.match(r'^[a-zA-Z]', line):
            collapsed.append(line)
        elif line.strip() and collapsed:
            collapsed[-1] = collapsed[-1] + ' ' + line.strip()

    # Rebuild YAML lines: quote summary, inject slug
    new_yaml_lines = []
    for line in collapsed:
        if line.startswith('summary:'):
            val = line[len('summary:'):].strip()
            # Strip existing outer quotes
            if (val.startswith('"') and val.endswith('"')) or \
               (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            # Escape inner double quotes
            val = val.replace('"', "'")
            line = 'summary: "' + val + '"'
        if line.startswith('series-position:'):
            new_yaml_lines.append('slug: ' + slug)
        new_yaml_lines.append(line)

    new_yaml = '\n'.join(new_yaml_lines)
    new_content = '---\n' + new_yaml + '\n---\n' + body

    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Written: {slug}.md')


if __name__ == '__main__':
    for src_name, slug in FILES:
        process(src_name, slug)
    print('Done.')
