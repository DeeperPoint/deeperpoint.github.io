"""Sanitize _add_all_extension_opps.py: replace smart quotes,
em-dashes, and unescaped apostrophes-in-single-quoted-strings."""
import re
from pathlib import Path

src = Path('scripts/_add_all_extension_opps.py')
text = src.read_text(encoding='utf-8')

# Replace smart quotes and em-dashes with ASCII equivalents
text = text.replace('\u2014', '-')   # em dash
text = text.replace('\u2013', '-')   # en dash
text = text.replace('\u2018', "'")   # left single quote
text = text.replace('\u2019', "'")   # right single quote / apostrophe
text = text.replace('\u201c', '"')   # left double quote
text = text.replace('\u201d', '"')   # right double quote

# The remaining problem: unescaped ' inside single-quoted string literals
# e.g.  'the platform's data'  -> the inner apostrophe terminates the string
# Strategy: find every string value after 'strategic_logic': or 'revenue_model':
#    and escape any bare apostrophes that appear inside them.
# We process line by line since the values are all on single lines.

lines = text.split('\n')
fixed = []
for line in lines:
    # Match lines that are string-value assignments in the dict literals
    m = re.match(r"^(\s+'(?:strategic_logic|revenue_model|title)': ')(.+?)('(?:,?))\s*$", line)
    if m:
        prefix, content, suffix = m.group(1), m.group(2), m.group(3)
        # Escape any remaining apostrophes in content
        content = content.replace("'", "\\'")
        fixed.append(prefix + content + suffix)
    else:
        fixed.append(line)

src.write_text('\n'.join(fixed), encoding='utf-8')
print('Done sanitizing.')
