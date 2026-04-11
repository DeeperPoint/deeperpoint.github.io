# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.
"""
Inject card_title into all published scenario YAML files.
Run from repo root: python scripts/_add_card_titles.py
"""
import yaml
from pathlib import Path

# slug -> card_title  (max ~60 chars, ideally one punchy line)
CARD_TITLES = {
    # --- Allergen / Food ---
    "allergen-free-comanufacturing":        "Allergen-Free Co-Manufacturing Access",
    "food-product-development":             "Food Product Development Services",
    "food-service-distribution":            "Food Service Distribution Matching",
    "institutional-procurement":            "Institutional Food Procurement",
    "kosher-halal-certification":           "Kosher & Halal Certification Matching",
    "private-label":                        "Private Label Product Development",
    "retail-listing":                       "Retail Shelf Discovery for Small Producers",
    "shared-kitchen":                       "Shared Licensed Kitchen Access",
    "co-manufacturing":                     "Co-Manufacturing Capacity Matching",
    "cold-chain-delivery":                  "Cold Chain Delivery for Small Shippers",

    # --- Canadian Government Expert Networks (cgov) ---
    "cgov-critical-infrastructure-cyber":   "Cybersecurity Expertise for Critical Infrastructure",
    "cgov-environmental-assessment":        "Environmental Assessment Expert Procurement",
    "cgov-forensic-accounting":             "Forensic Accounting for Government Investigations",
    "cgov-heritage-conservation":           "Heritage Conservation Specialists for Public Buildings",
    "cgov-immigration-tribunal":            "Immigration Tribunal Interpretation & Legal Support",
    "cgov-indigenous-consultation":         "Indigenous Consultation Expertise for Government Projects",
    "cgov-municipal-climate-adaptation":    "Climate Adaptation Consultants for Municipalities",
    "cgov-northern-infrastructure":         "Northern Infrastructure Specialists",
    "cgov-public-health-surge":             "Public Health Surge Capacity — Specialist Matching",
    "cgov-regulatory-science":              "Regulatory Science Expertise on Demand",

    # --- Canada-Mexico Trade (cm) ---
    "cm-greenhouse-tech":                   "Greenhouse Technology Transfer: Canada to Mexico",
    "cm-medical-equipment":                 "Medical Equipment Trade: Canada-Mexico",
    "cm-mining-services":                   "Mining Services Trade: Canada to Mexico",
    "cm-nearshore-software":                "Nearshore Software Development: Mexico for Canada",
    "cm-probono-legal":                     "Cross-Border Pro Bono Legal Matching",
    "cm-pulse-crops":                       "Pulse Crop Trade: Canadian Growers, Mexican Buyers",
    "cm-skilled-trades":                    "Skilled Trades Exchange: Canada-Mexico",
    "cm-specialty-lumber":                  "Specialty Lumber Trade: Canada to Mexico",
    "cm-sustainable-packaging":             "Sustainable Packaging Sourcing: Canada-Mexico",
    "cm-tech-transfer":                     "Technology Transfer: Canada-Mexico Innovation",

    # --- Canadian Healthcare Support (chc) ---
    "chc-adaptive-equipment-exchange":      "Used Wheelchairs & Home Care Equipment Exchange",
    "chc-caregiver-respite-matching":       "Respite Care for Exhausted Family Caregivers",
    "chc-home-dialysis-peer-support":       "Home Dialysis: Practical Peer Support",
    "chc-lymphedema-garment-access":        "Lymphedema Compression Garment Fitting Network",
    "chc-ostomy-peer-navigator":            "Finding the Right Ostomy Peer Mentor",
    "chc-rare-disease-patient-navigator":   "Rare Disease: Finding a Specialist and a Peer",

    # --- Canadian Sport (csport) ---
    "csport-broadcasting-rights":           "Minor Sport Broadcasting Rights Matching",
    "csport-coach-placement":               "Specialized Coach Placement in Canadian Sport",
    "csport-disability-adaptive":           "Adaptive Sport Program Matching",
    "csport-equipment-resale":              "Used Sport Equipment Resale & Exchange",
    "csport-event-sponsorship":             "Independent Sport Event Sponsorship Matching",
    "csport-facility-sharing":              "Sport Facility Sharing Across Organizations",
    "csport-indigenous-sponsorship":        "Indigenous Sport Sponsorship: Reconciliation Partnerships",
    "csport-psychology-services":           "Sport Psychology Services for Athletes",
    "csport-science-consulting":            "Sport Science Consulting for High Performance",
    "csport-tourism-hosting":               "Sport Tourism: Matching Events to Host Communities",
    "csport-youth-recruitment":             "Elite Youth Athlete Recruitment Across Canada",

    # --- Canadian Startup Ecosystem (cstartup) ---
    "cstartup-accelerator-matching":        "Remote Founder — Accelerator Matching",
    "cstartup-angel-discovery":             "Remote Founder — Angel Investor Discovery",
    "cstartup-cofounder-matching":          "Co-Founder Discovery Across Canada",
    "cstartup-immigrant-talent":            "Immigrant Technical Talent for Startups Outside Hubs",
    "cstartup-indigenous-entrepreneur":     "Indigenous Entrepreneur Access to Startup Networks",
    "cstartup-pilot-customer":              "Remote B2B Startup — First Pilot Customer",
    "cstartup-professional-services":       "Startup-Savvy Professional Services Outside Hubs",
    "cstartup-remote-mentorship":           "Remote Founder — Mentor Matching",
    "cstartup-research-commercialization":  "University Research Commercialization at Small Campuses",
    "cstartup-small-batch-manufacturing":   "Remote Startup — Small-Batch Canadian Manufacturer",

    # --- Global Knowledge Exchange (gke) ---
    "gke-biomedical-equipment-support":     "Remote Biomedical Equipment Support for Hospitals",
    "gke-climate-data-collaboration":       "Climate Science Data Exchange: Africa and Global Analysts",
    "gke-land-rights-legal-tech":           "Land Rights Legal Technology for African Organizations",
    "gke-open-source-software-mentorship":  "Open Source Architecture Mentorship for African Teams",
    "gke-pharmaceutical-formulation":       "Pharmaceutical Formulation Collaboration: African Manufacturers",
    "gke-plant-pathology-response":         "Crop Disease Emergency: Remote Plant Pathology Consulting",
    "gke-research-equipment-surplus":       "Research Equipment Surplus: Lab-to-Lab Transfer",
    "gke-solar-microgrid-peer-review":      "Solar Microgrid Design: Peer Engineering Review",
    "gke-surgical-case-consultation":       "Complex Surgery: Remote Second Opinion Network",
    "gke-traditional-knowledge-validation": "Traditional Agricultural Knowledge: Scientific Validation",

    # --- Municipal (muni) ---
    "muni-adaptive-recreation":             "Accessible Recreation & Adaptive Equipment",
    "muni-brownfield":                      "Brownfield Remediation & Adaptive Development",
    "muni-climate-contractors":             "Climate Action Contractors for Municipal Green Infrastructure",
    "muni-disability-employment":           "Disability Employment & Workplace Accommodation",
    "muni-energy-retrofit":                 "Community Energy Retrofit — Contractor Matching",
    "muni-heritage-trades":                 "Heritage Trades for Municipal Buildings",
    "muni-social-procurement":              "Local & Social Enterprise Supplier Development",
    "muni-surplus-assets":                  "Municipal Surplus Asset Disposal & Transfer",
    "muni-transitional-housing":            "Transitional Housing & Supportive Services Placement",
    "muni-volunteer-matching":              "Municipal Volunteer & Community Skills Matching",

    # --- Real Estate Assembly (rea) ---
    "rea-commercial-tenant-improvement":    "Trade Assembly for Commercial Tenant Buildouts",
    "rea-density-bonus-application":        "Developer Team Assembly for Density Bonus Applications",
    "rea-development-site-diligence":       "Fast-Track Due Diligence Team for Site Acquisition",
    "rea-distressed-property-turnaround":   "Distressed Property Turnaround Team Assembly",
    "rea-industrial-tenant-buildout":       "Specialized Trades for Industrial Lease Buildouts",
    "rea-multifamily-capital-renewal":      "Specialist Contractors for Multifamily Capital Renewal",
    "rea-pre-sales-launch-package":         "Condo Pre-Sales: Developer Marketing Package Assembly",
    "rea-retail-plaza-leasing":             "Retail Plaza Leasing: Hard-to-Fill Centres",
    "rea-rural-land-subdivision":           "Rural Land Subdivision: Servicing Consultant Assembly",
    "rea-str-portfolio-launch":             "Short-Term Rental Portfolio: Service Assembly",

    # --- Ring of Fire Hub (rof) ---
    "rof-environmental-compliance-pool":    "Shared Environmental Monitoring — Ring of Fire Operations",
    "rof-greenstone-hub-marketplace":       "Greenstone as a Full-Service Hub Town",
    "rof-ground-control-engineering":       "Shared Rock Mechanics Engineer — Multiple Remote Mines",
    "rof-indigenous-contractor-registry":   "Indigenous Contractor Registry — Ring of Fire IBA Procurement",
    "rof-medevac-helicopter-cooperative":   "Shared Medevac Helicopter — Remote Mining Cluster",
    "rof-medical-officer-network":          "Fractional Medical Officer — Remote Mine Operations",
    "rof-underground-equipment-maintenance":"Underground Mining Equipment Maintenance Hub",

    # --- Remote Town Renewal (rtr) ---
    "rtr-local-resource-value-chain":       "Building a Local Food & Product Economy in Post-Industrial Towns",
    "rtr-remote-professional-attraction":   "Attracting Professionals to Remote Communities",
    "rtr-skilled-trades-return-migration":  "Skilled Trades Return Migration to Infrastructure-Rich Towns",

    # --- SME Consortium (sme) ---
    "sme-after-school-consortium":          "SME Consortium for School Board After-School Contracts",
    "sme-corporate-event-consortium":       "SME Consortium for Corporate Event Production",
    "sme-corporate-incentive-travel":       "Boutique Operator Consortium for Corporate Incentive Travel",
    "sme-corporate-wellness-consortium":    "SME Provider Consortium for Corporate Wellness Contracts",
    "sme-destination-wedding-package":      "Boutique Provider Consortium for Destination Weddings",
    "sme-digital-marketing-consortium":     "SME Agency Consortium for Enterprise Digital Marketing",
    "sme-film-production-consortium":       "SME Crew Consortium for Independent Film Production",
    "sme-home-deep-retrofit":               "Trade Consortium for Integrated Home Deep Retrofits",
    "sme-property-services-bundle":         "Trade Bundle for Strata & Property Management Contracts",
    "sme-senior-transition-consortium":     "Multi-Provider Consortium for Senior Life Transitions",

    # --- Social Value Zone (svz) ---
    "svz-disability-employment":            "Accessible Employment Matching for People with Disabilities",
    "svz-immigrant-credentials":            "Immigrant Professional Credential Recognition",
    "svz-probono-legal":                    "Pro Bono Legal Matching for Social Enterprises",
    "svz-restorative-justice":              "Restorative Justice & Reintegration Services",
    "svz-sustainable-materials":            "Sustainable Materials Commercialization",
    "svz-telepharmacy":                     "Minor Ailment Telepharmacy Matching",
}

SCENARIOS_DIR = Path("catalog/scenarios")

updated = 0
skipped = 0
for f in sorted(SCENARIOS_DIR.glob("*.yaml")):
    slug = f.stem
    if slug not in CARD_TITLES:
        print(f"  No card_title defined for: {slug}")
        skipped += 1
        continue
    text = f.read_text(encoding="utf-8")
    # Remove existing card_title line if present
    lines = text.splitlines(keepends=True)
    lines = [l for l in lines if not l.startswith("card_title:")]
    # Insert card_title after the title line
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if line.startswith("title:"):
            new_lines.append(f'card_title: "{CARD_TITLES[slug]}"\n')
    f.write_text("".join(new_lines), encoding="utf-8")
    updated += 1

print(f"\nDone: {updated} updated, {skipped} skipped (no card_title defined).")
