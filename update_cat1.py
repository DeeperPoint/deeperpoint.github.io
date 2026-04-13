import os, re

cat1_files = [
    'catalog/scenarios/muni-volunteer-matching.yaml',
    'catalog/scenarios/muni-adaptive-recreation.yaml',
    'catalog/scenarios/sme-after-school-consortium.yaml',
    'catalog/scenarios/sme-corporate-wellness-consortium.yaml',
    'catalog/scenarios/gke-land-rights-legal-tech.yaml',
    'catalog/scenarios/dev-coyote-price-transparency.yaml',
    'catalog/scenarios/dia-refugee-peer-support.yaml',
    'catalog/scenarios/art-heritage-craft-transmission.yaml'
]

flag_text = ' [Note: Due to the marginal commercial value of transactions in this market, MarketForge deployment in this scenario is entirely dependent on philanthropic, public-sector, or non-profit sponsorship.]'

for f in cat1_files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if '[Note: Due to the marginal' not in content:
            # We look for summary: "..." and insert the text before the final quote
            # Because yaml multi-line strings might span multiple lines, we use DOTALL
            new_content = re.sub(r'(market_example:\s*summary:\s*".*?)(")', r'\1' + flag_text + r'\2', content, flags=re.DOTALL)
            with open(f, 'w', encoding='utf-8') as out:
                out.write(new_content)
            print('Updated: ' + f)
        else:
            print('Already flagged: ' + f)
    else:
        print('Missing: ' + f)
