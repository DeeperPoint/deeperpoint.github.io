import os
import re

new_nav_items = [
    ("Home", "index.html"),
    ("Theory", "thin-markets.html"),
    ("Project", "project.html"),
    ("Demo", "demo-guide.html"),
    ("Matrix", "intervention-matrix.html"),
    ("Catalog", "catalog/index.html"),
    ("MarketMaps", "marketmaps.html"),
    ("Blog", "blog/index.html"),
    ("Ebook", "ebook.html"),
    ("About", "about.html")
]

def get_relative_prefix(filepath):
    parts = filepath.split('/')
    if parts[0] == '.':
        parts = parts[1:]
    depth = len(parts) - 1
    if depth == 0:
        return ""
    return "../" * depth

def build_nav_html(prefix, current_filepath):
    parts = current_filepath.split('/')
    if parts[0] == '.':
        parts = parts[1:]
    normalized_current = "/".join(parts)
    
    lines = ['      <ul class="nav__links">']
    for label, target in new_nav_items:
        href = target
        if prefix:
            href = prefix + target
            
        is_active = False
        # If the target is an exact match for the current file
        if normalized_current == target:
            is_active = True
        # For directories like blog/ or catalog/, if we are inside them, maybe mark as active
        elif target.endswith('index.html') and target != 'index.html' and normalized_current.startswith(target.replace('index.html', '')):
            is_active = True
            
        active_class = ' nav__link--active' if is_active else ''
        lines.append(f'        <li><a href="{href}" class="nav__link{active_class}">{label}</a></li>')
    lines.append('      </ul>')
    return '\n'.join(lines)

nav_regex = re.compile(r'^[ \t]*<ul class="nav__links">.*?</ul>', re.MULTILINE | re.DOTALL)

updated_count = 0
for root, dirs, files in os.walk('.'):
    # skip .git or node_modules or something if they exist
    if '.git' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            prefix = get_relative_prefix(filepath)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            new_nav = build_nav_html(prefix, filepath)
            new_content = nav_regex.sub(new_nav, content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1

print(f"Updated {updated_count} files.")
