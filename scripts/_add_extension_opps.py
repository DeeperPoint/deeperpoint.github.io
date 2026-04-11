"""Add commerce-extension and logistics-extension sponsor/investor opportunities to selected catalog entries."""
# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.
import re
from pathlib import Path

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

    # ── Tier 1 ──────────────────────────────────────────────────────────────

    ('shared-kitchen', {
        'title': 'Ingredient Procurement + Last-Mile Distribution Commerce Extension',
        'type': 'commerce-extension',
        'revenue_model': 'Distributor margin on group ingredient orders (8-15% on wholesale volumes); per-delivery logistics fee per producer per weekly run; cold storage booking fee; platform earns commerce margin vs. booking fee from the same customer base at 20-30x uplift per participant',
        'strategic_logic': 'The kitchen booking platform knows what every producer is making and when — because booking reveals the production schedule. This data asset, which specialty food distributors spend millions trying to approximate and never fully obtain, is a by-product of the matching operation. Extending into group ingredient procurement and last-mile retail distribution converts the platform from a $30 booking fee business into a $1,000+/month commerce relationship with each producer — from the same customer, at zero incremental acquisition cost. The matching platform is the customer acquisition infrastructure for the commerce business, not the end product.',
        'recurring': True,
    }),

    ('dia-cultural-import-sourcing', {
        'title': 'Platform-Managed Import and Ethnic Food Distribution',
        'type': 'commerce-extension',
        'revenue_model': 'Distributor margin on imported goods (15-25% vs. 2% matching fee on same volume); DTC ethnic food subscription box revenue; private label product margin; import logistics fee per consolidated container shipment',
        'strategic_logic': 'Once the platform has verified supplier relationships in origin countries and verified buyer relationships in Canadian diaspora grocery and restaurant channels, it already is the distribution chain — the matching fee is the lowest-value component of the infrastructure it has built. Moving from matching sourcing agents to buyers to operating as the importer of record — consolidating orders, clearing customs under the platform\'s own import licenses, delivering to buyers — multiplies revenue per transaction by 8-12x with no new customer acquisition. The supplier vetting and import corridor infrastructure built for the matching business is the defensible asset that makes platform-managed distribution possible.',
        'recurring': True,
    }),

    ('rof-greenstone-hub-marketplace', {
        'title': 'Northern Supply Procurement and Camp Logistics Extension',
        'type': 'logistics-extension',
        'revenue_model': 'Group purchasing margin on aggregated camp supply orders (8-12%); northbound freight coordination fee per tonne; southbound return-logistics revenue (currently deadhead value captured); camp services management fee per operation; platform earns a logistics and commerce margin on every dollar of subcontract value it matches',
        'strategic_logic': 'Every verified subcontract match on the platform generates 15-30 cents of camp supply and logistics spend from the same matched contractors — spend that currently flows through fragmented and expensive southern procurement channels. The platform already knows who is working where, on what timeline, and what they need transported. Extending into consolidated supply procurement (group volume pricing from southern suppliers) and coordinated northbound logistics (shared charter and ground routes) does not require a new customer relationship — it monetizes the supply chain the matched participants already operate. A northern supply business built on verified contractor relationships has defensible monopoly characteristics that a logistics-only competitor cannot replicate.',
        'recurring': True,
    }),

    ('chc-adaptive-equipment-exchange', {
        'title': 'Chronic Condition Consumables Subscription Commerce Extension',
        'type': 'commerce-extension',
        'revenue_model': 'Monthly consumables subscription per enrolled patient ($150-300/month; ostomy, dialysis, lymphedema, CPAP categories); group purchasing margin on aggregated consumable orders (10-20%); premium reimbursement navigator subscription; platform earns recurring revenue for the life of the condition from customers acquired through the equipment exchange',
        'strategic_logic': 'Chronic condition patients who find equipment through the exchange need consumables on a predictable monthly schedule — and the platform already knows the device type, condition category, and supply requirements that determine what they need. The equipment sale is a one-time transaction; the consumable subscription is 12-24 months of recurring revenue from the same patient. Operating the exchange at near-cost as the customer acquisition channel and monetizing through consumable subscriptions is the razor/blade model applied to chronic care supply — with the platform\'s community intelligence providing a sourcing advantage that pharmacy and mail-order channels cannot match.',
        'recurring': True,
    }),

    ('cdef-sme-prime-capability-match', {
        'title': 'Defence SME Certification and Compliance Services Extension',
        'type': 'commerce-extension',
        'revenue_model': 'Certification advisory retainer (ISO 9001/AS9100/CMMC preparation; $15,000-40,000 per SME per certification cycle); compliance monitoring subscription (annual); security clearance facilitation advisory (FSC application support); platform earns professional services revenue from every SME it matches — converting a one-time match into a multi-year advisory relationship',
        'strategic_logic': 'Defence SMEs that win subcontract matches through the platform immediately face a follow-on need: certifications (ISO 9001, AS9100, CMMC Level 2) required to compete for the next program. The platform knows exactly which certifications each matched SME lacks, which are required for which program tiers, and on what timeline certification must be achieved before the next RFP cycle. A certification advisory service marketed to platform participants converts the one-time matching relationship into a 2-3 year engagement — the platform becomes the SME\'s ongoing defence market infrastructure provider, not just a one-time directory. The advisory revenue per SME (2-3 certifications over 5 years at $20K average) substantially exceeds the matching fee that initiated the relationship.',
        'recurring': True,
    }),

    # ── Tier 2 ──────────────────────────────────────────────────────────────

    ('cold-chain-delivery', {
        'title': 'Shared Cold Chain Network Operating Extension',
        'type': 'logistics-extension',
        'revenue_model': 'Per-tonne-kilometre freight rate on managed cold chain routes; temperature zone booking fee per pallet-slot; network access subscription for regular cold-chain shippers; platform earns freight margin vs. matching fee by operating the routes the matching platform designed',
        'strategic_logic': 'The cold chain matching platform accumulates data on delivery schedules, temperature requirements, route patterns, and truck capacity utilization across its participant base. At scale, this data is sufficient to design and operate a shared cold chain network — aggregating small loads onto optimized temperature-controlled routes and charging freight rates. The platform moves from earning a matching fee on cold chain transactions to earning the freight margin on the cold chain itself. Network participants who were previously independent buyers of cold chain logistics become anchor customers of a platform-operated logistics business.',
        'recurring': True,
    }),

    ('dia-property-remote-oversight', {
        'title': 'Ongoing Diaspora Property Management Subscription',
        'type': 'commerce-extension',
        'revenue_model': 'Monthly property management subscription (8-12% of rental income or flat fee for vacant properties); tenant sourcing fee; maintenance coordination markup; annual property condition report; platform converts a one-time renovation oversight engagement into a multi-year property management relationship using the verified contractor network and property profile already established',
        'strategic_logic': 'After the renovation oversight project closes, the diaspora property owner still has an ongoing need: tenant management, rent collection, maintenance coordination, and condition monitoring from overseas. The platform already has the verified local contractor network, the property profile, the owner\'s trust, and the AI-verification infrastructure. Offering a property management subscription as the natural next step converts a transaction (renovation project) into a recurring revenue relationship (annual property management) — using assets that have already been built and paid for by the matching operation.',
        'recurring': True,
    }),

    ('rof-indigenous-contractor-registry', {
        'title': 'Ring of Fire Consolidated Supply Procurement Extension',
        'type': 'logistics-extension',
        'revenue_model': 'Group purchasing margin on aggregated contractor supply orders (tools, PPE, small equipment, consumables; 8-16%); supply delivery coordination fee per remote site; preferred supplier partnership fees; the supply procurement extension monetizes a portion of every dollar the matched contractors spend on inputs and consumables',
        'strategic_logic': 'Every contractor matched through the registry needs supplies — tools, safety equipment, consumables, and small materials sourced from southern Ontario suppliers at prices that remote northern buyers cannot negotiate individually. The platform already knows what each contractor is doing, where, and on what timeline — exactly the demand intelligence a consolidated supply procurement operation needs. Aggregating contractor supply orders into group purchasing volumes unlocks pricing that no individual contractor could achieve and creates a logistics coordination advantage built entirely on matching relationship data.',
        'recurring': True,
    }),
]

for slug, opp in additions:
    add_opp(slug, opp)

print('Done. All extension opportunities added.')
