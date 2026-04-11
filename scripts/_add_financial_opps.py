"""Add financial product and insurance sponsor/investor opportunities to selected catalog YAML files."""
# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.
import re
from pathlib import Path
import glob

def add_opp(slug, opp):
    f = Path(f'catalog/scenarios/{slug}.yaml')
    if not f.exists():
        print(f'  SKIP (not found): {slug}')
        return
    text = f.read_text(encoding='utf-8')
    block = (
        f'  - title: "{opp["title"]}"\n'
        f'    type: {opp["type"]}\n'
        f'    revenue_model: "{opp["revenue_model"]}"\n'
        f'    strategic_logic: "{opp["strategic_logic"]}"\n'
        f'    recurring: {str(opp["recurring"]).lower()}\n'
        '\n'
    )
    story_match = re.search(r'^story:', text, re.MULTILINE)
    if not story_match:
        print(f'  ERROR: no story: section in {slug}')
        return
    insert_pos = story_match.start()
    new_text = text[:insert_pos] + block + text[insert_pos:]
    f.write_text(new_text, encoding='utf-8')
    print(f'  Added to {slug}')

additions = [
    ('dia-property-remote-oversight', {
        'title': 'Diaspora Property Renovation Insurance Product',
        'type': 'insurance-product',
        'revenue_model': 'Per-policy annual premium; parametric completion bond premium per renovation project; reinsurance co-arrangement with diaspora association sponsor; platform data licensing fee paid by underwriter for access to verified renovation compliance stream',
        'strategic_logic': 'The platform generates exactly the documentation a parametric property insurer needs: geotagged milestone photos, AI-verified code compliance, and escrow-backed payment record. Overseas diaspora properties are chronically uninsurable because no verification infrastructure existed; the platform creates the underwriting basis for the first time. A fintech insurer co-investing with the association sponsor accesses a market of hundreds of thousands of uninsured diaspora-owned properties — a new asset class created by the marketplace data.',
        'recurring': True,
    }),
    ('dia-bilateral-trade-sourcing', {
        'title': 'Diaspora Trade Finance Facility',
        'type': 'financial-product',
        'revenue_model': 'Per-transaction advance fee (2-3% of purchase order value); 90-day revolving facility interest; development finance institution annual license; platform origination fee (0.5% of each advance)',
        'strategic_logic': 'Bank trade finance minimums ($100K+) exclude the $5K-$50K order sizes typical of diaspora-facilitated trade. The platform generates the verified facilitator track record, buyer/seller due diligence, and escrow transaction history that a fintech trade lender needs to underwrite at this order size. A development finance institution (EDC, Caribbean Development Bank) co-investing as the facility anchor activates a segment of bilateral trade that currently flows informally without credit infrastructure.',
        'recurring': True,
    }),
    ('cdef-sme-prime-capability-match', {
        'title': 'Defence Subcontract Invoice Factoring Facility',
        'type': 'financial-product',
        'revenue_model': 'Per-invoice advance fee (1.5-2% per 30-day period); facility line fee (0.5% annual); platform origination fee (0.25% per invoice factored); optional credit insurance co-product with Export Development Canada',
        'strategic_logic': 'DND milestone payment cycles run 45-90+ days, creating a working capital gap that is crippling for small defence SMEs. The platform-verified subcontract record, milestone completion documentation, and prime contractor counterparty profile are exactly the credit basis an invoice factoring fund needs. Almost no factoring market currently serves defence subcontract invoices under $500K. A factoring fund co-investing with the platform accesses DND-backed receivables — a credit-quality asset class with minimal default risk and no current market infrastructure.',
        'recurring': True,
    }),
    ('chc-adaptive-equipment-exchange', {
        'title': 'Adaptive Medical Equipment Acquisition Financing',
        'type': 'financial-product',
        'revenue_model': 'Per-loan origination fee (2-3% of equipment value); monthly interest income (8-12% APR); platform referral fee per financed transaction; optional equipment protection insurance co-product',
        'strategic_logic': 'The secondary adaptive equipment marketplace generates verified device condition and market pricing data — making the secondary market financeable for the first time. A medical equipment fintech or credit union co-investing as the lender uses platform pricing as the valuation basis and platform seller verification as the underwriting anchor. Patients who cannot afford upfront secondary-market prices gain access; the lender gains a verified collateral valuation it could not produce independently.',
        'recurring': True,
    }),
    ('rof-indigenous-contractor-registry', {
        'title': 'Northern Contractor Equipment Lease-to-Own Facility',
        'type': 'equipment-finance',
        'revenue_model': 'Monthly lease payment income; end-of-term purchase option fee; BDC or indigenous development corporation co-investment as lessor; mining company client first-loss guarantee in exchange for preferred contractor access; platform facilitation fee per lease originated',
        'strategic_logic': 'Indigenous and northern contractors winning Ring of Fire subcontracts through the platform have verified subcontract records — a bankable credit asset they could not demonstrate before the platform existed. The match record is the credit basis; the subcontract cash flow is the repayment source; the equipment is the collateral. A BDC or First Nations development corporation co-investing as the lessor activates a contractor development mandate that these institutions have but cannot operationalize without verified deal flow.',
        'recurring': True,
    }),
    ('shared-kitchen', {
        'title': 'Food Entrepreneur Revenue-Based Financing',
        'type': 'financial-product',
        'revenue_model': 'Advance origination fee (3-5%); revenue share repayment (8-12% of monthly platform-verified kitchen revenue until 1.5x repaid); platform data licensing fee paid by lender for ongoing access to verified production and booking history',
        'strategic_logic': 'Food entrepreneurs with 6+ months of verified kitchen booking and production history have a credit record that no traditional lender can see but that a marketplace lender can underwrite directly from the platform data feed. Revenue-based repayment aligns with the entrepreneur revenue cycle — no fixed monthly payment to default on during a slow month. A food business fintech or credit union co-investing as the lender accesses a segment of small business borrowers with verifiable cash flow but no conventional credit footprint.',
        'recurring': True,
    }),
    ('cdef-caf-transition-employment', {
        'title': 'CAF Releasing Member Income Protection Insurance',
        'type': 'insurance-product',
        'revenue_model': 'Monthly premium during active platform job search; employer partner premium co-subsidy (hiring employer contributes to premium, reducing member urgency and employer time-to-fill); Veterans Affairs Canada program grant support; platform facilitation fee per policy originated',
        'strategic_logic': 'The platform generates match quality data — placement likelihood by MOC code, time-to-placement distributions, employer demand by military trade — that creates an actuarial basis for income protection insurance that does not currently exist for releasing CAF members. A specialty insurer pricing the product against verified platform data rather than general unemployment statistics creates a more accurate product at a lower premium. VAC co-funding the subsidy activates a transition support mandate it has but cannot operationalize through clinical services alone.',
        'recurring': True,
    }),
]

for slug, opp in additions:
    add_opp(slug, opp)

print('All additions complete.')
