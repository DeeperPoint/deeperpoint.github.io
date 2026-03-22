<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->

---
series: manufacturing-scenarios
series-title: "Manufacturing Scenarios"
series-position: 3
slug: manufacturing-scenarios-skills
title: "Market Scenario: The Welder Who Wrote Firewalls"
date: 2026-03-18
stream: market-scenario
tags: [thin-markets, ai, market-design, case-study, scenario, cosolvent, knowledgeslot, marketforge, manufacturing]
summary: A small manufacturer in Trois-Rivières needs someone who understands industrial cybersecurity — not full-time, just enough to pass an audit. Three hundred kilometres away, a machining shop in Sherbrooke has a production supervisor whose previous career was in IT security. The skill exists. The need exists. But no marketplace connects fractional industrial talent between SMBs.
estimated-read: 12 min read
---

<figure class="blog-hero">
  <img class="blog-hero__img" src="../images/blog/fractional-skills-thin-market-hero.png" alt="A CNC machining shop where the network switch on the wall matters as much as the machines on the floor" loading="lazy">
  <figcaption>A CNC machining shop where the network switch on the wall matters as much as the machines on the floor.</figcaption>
</figure>

## The Expanding Perimeter

The perimeter of what constitutes "manufacturing" has expanded into two dozen adjacent specialties that didn't exist a generation ago. Every new regulation, every software platform, every cybersecurity framework adds another line item to the roster of skills a manufacturer must access. A large company absorbs this by hiring specialists into dedicated departments. A twelve-person shop absorbs it by asking whoever seems least busy.

The choices are all unsatisfying: train the machinist who is least terrified of computers, hire a consulting firm at $25,000+ per engagement, or post on Upwork and sort through fifty applicants who have never set foot in a manufacturing facility. But there is a fourth option that doesn't yet exist: find another SMB that happens to have *surplus capacity* in exactly that skill — a production supervisor who did cybersecurity in a previous career, a quality manager who spent five years doing ISO documentation for an aerospace contractor.

These people exist. Their employers have already benefited from their skills and now have what amounts to surplus capacity in a specialized domain. But there is no mechanism for one SMB to discover that another SMB has a person with forty hours of uncommitted expertise in the exact discipline they need. *The characters below are fictional, but the skill gaps and market forces are real.*

---

## 1. Nadine's Audit

Nadine Bergeron runs a twenty-two-person manufacturer of custom hydraulic cylinders and manifold blocks in Trois-Rivières, Québec. The company — Hydraulique Bergeron — makes components for forestry equipment, snow groomers, and marine deck machinery. It's a family business, founded by her father in 1986. Revenue is steady, margins are tight, and the customer base is loyal.

Last month, a procurement officer at one of her largest customers — a Scandinavian forestry equipment OEM that buys custom hydraulic manifolds — sent a new supplier questionnaire. The questionnaire is twenty-three pages long and includes a section Nadine has never seen before: **Industrial Cybersecurity Compliance Self-Assessment**.

The section asks whether Hydraulique Bergeron has: a documented cybersecurity policy; a network segmentation plan separating IT systems from operational technology (OT) systems; multifactor authentication on all administrative accounts; an incident response plan; regular vulnerability scanning; an employee cybersecurity training program; and compliance with either IEC 62443 (industrial automation security) or NIST SP 800-82 (guide to industrial control system security).

Nadine's operation has none of this. The shop runs three CNC lathes and two CNC mills, all with Fanuc controllers networked to a single CAM workstation running Mastercam. The network also connects to the office — the ERP system, email, accounting. The entire IT infrastructure is managed by her nephew Étienne, who is officially the production scheduler but is the unofficial "computer person" because he built gaming PCs in high school.

Nadine calls the Scandinavian procurement officer. The conversation is friendly but firm: the OEM's parent company has adopted a supply chain cybersecurity standard. All Tier 2 and Tier 3 suppliers must demonstrate at least "basic hygiene" compliance within six months or face supplier status review. The procurement officer is sympathetic — she knows Nadine's manifold blocks are excellent — but the policy is corporate, not personal.

Nadine now has a problem that is both urgent and completely outside her domain. She calls two cybersecurity consulting firms in Montréal. Both are happy to help. Both quote engagements starting at $25,000 — a gap assessment, a remediation plan, employee training, and documentation. One can start in eight weeks; the other in twelve. Neither has specific experience with manufacturing OT environments — they do offices, clinics, and law firms. The Fanuc controllers, the Mastercam workstation, the air-gapped CNC versus networked CNC question — that's not their world.

Nadine needs someone who understands both cybersecurity *and* manufacturing shop floors. She needs perhaps forty to sixty hours of that person's time, spread over four to six weeks. She does not need a full-time cybersecurity analyst, and she cannot afford one. She needs a fractional expert — and not a generic one, but one who knows what a Fanuc controller is, who has seen a CAM workstation connected to a production network, who understands that "segment the OT network" in a twenty-two-person shop means something different than it does at Bombardier.

---

## 2. Maxime's Surplus

Three hundred kilometres east, in Sherbrooke, Québec, Maxime Ouellet is the production supervisor at Usinage Précision Estrie — a fourteen-person precision machining shop that makes aerospace components and medical device parts. Maxime has an unusual résumé.

Before joining Usinage Précision four years ago, Maxime spent eight years as a network security analyst at a defence contractor in Mirabel. He holds a CompTIA Security+ certification (maintained) and completed a SANS Institute course in industrial control system security — GICSP (Global Industrial Cyber Security Professional). He left the defence industry because he wanted to work closer to the machines, not the screens. He became a machinist, then a CNC programmer, then a production supervisor.

When Maxime arrived at Usinage Précision, he took one look at the shop's network — five Haas CNC machining centres daisy-chained to an unsegmented Ethernet network shared with the office computers — and quietly spent three weekends fixing it. He segmented the OT network. He configured the router's firewall rules. He set up a separate VLAN for the CNC controllers with restricted gateway access. He enabled multifactor authentication on the Jobboss ERP system. He wrote a ten-page cybersecurity policy document, a four-page incident response plan, and a one-page employee training handout. He presented it to his boss, Marc-André, who said: "This is good. Can you also look at the coolant pump on the Haas VF-4? It's making a noise."

Maxime now carries both roles — production supervisor and de facto cybersecurity administrator — but the cybersecurity work is done. The systems are hardened. The documentation is written. The annual review takes him about four hours. He has forty-plus hours of specialized, manufacturing-specific cybersecurity expertise with nothing to apply it to — surplus capacity in a skill that other manufacturers desperately need.

He doesn't know Nadine exists. She doesn't know he exists. And no marketplace, directory, industry association listing, or freelance platform connects SMB-to-SMB fractional skill sharing.

---

## 3. What the Platform Changes

Now imagine that **CME — Canadian Manufacturers & Exporters** — has deployed a fractional skills marketplace on [MarketForge infrastructure](https://deeperpoint.com/marketforge.html), designed for SMB manufacturers who need to buy, sell, or swap specialized expertise in fractional quantities. Manufacturers register their *available* expertise (surplus capacity in skills their employees already have) and their *needed* expertise (gaps they need to fill). The platform's AI matches supply to demand — not by job title, but by demonstrated competence against specific requirements.

---

### Nadine's Listing

Nadine opens the platform and describes her need — in French, conversationally:

> *"Mon client scandinave me demande une auto-évaluation en cybersécurité industrielle. Je n'ai aucune politique de cybersécurité, aucun plan de segmentation réseau, rien. J'ai besoin de quelqu'un qui comprend la sécurité informatique ET les ateliers de fabrication — quelqu'un qui sait ce qu'est un contrôleur Fanuc et pourquoi il ne devrait pas être sur le même réseau que mon courriel. Il me faut probablement 40 à 60 heures de travail, étalées sur un mois."*

The platform's AI extracts structured requirements:

- **Skill domain**: Industrial cybersecurity (IEC 62443 / NIST SP 800-82)
- **Manufacturing context**: CNC machining, Fanuc controllers, CAM workstation (Mastercam), small shop (22 employees)
- **Specific deliverables**: Cybersecurity policy, network segmentation plan, MFA implementation, incident response plan, employee training, compliance self-assessment documentation
- **Scope**: 40–60 hours, on-site or hybrid
- **Timeline**: Results needed within 6 weeks
- **Language**: French preferred
- **Budget ceiling** (private): $8,000 maximum

---

### Maxime's Profile

Maxime registered on the platform two months ago when CME's regional representative visited the shop for a technology adoption assessment. The platform built his expertise profile through a structured interview and document uploads:

- **Primary role**: Production supervisor, Usinage Précision Estrie
- **Available expertise**: Industrial cybersecurity — ICS/OT network security, policy development, employee training
- **Certifications**: CompTIA Security+, SANS GICSP
- **Manufacturing experience**: CNC machining environments, Haas and Fanuc controllers, Jobboss ERP, Mastercam, shop networks
- **Demonstrated work**: Segmented OT/IT networks at own facility, wrote cybersecurity policy and incident response plan, passed customer cybersecurity audit
- **Availability**: Evenings and selected weekdays (with employer's agreement), approximately 8–12 hours per week
- **Language**: French native, English fluent
- **Rate** (private): $85/hour — substantially below consulting firm rates, reflecting that this is side capacity from a salaried employee, not a consulting business

Maxime's employer, Marc-André, has also registered — as the "releasing" company. The platform requires employer acknowledgment for any skills-sharing engagement: the releasing company confirms the employee's availability, approves the scope of external work, and agrees that it does not conflict with the employee's primary duties or the releasing company's competitive interests. Marc-André agreed readily — Usinage Précision doesn't compete with Hydraulique Bergeron (different industries, different geographies), and he sees fractional revenue as a way to retain Maxime by making his full skill set economically productive.

---

### 4. The Match

The platform's semantic matching engine doesn't match by job title. "Cybersecurity analyst" would return hundreds of candidates, almost none of whom have manufacturing OT experience. Instead, it matches Nadine's *specific requirement profile* against Maxime's *demonstrated competence profile*.

The match is structural:

- **IEC 62443 / NIST 800-82 competence**: GICSP certification directly covers industrial control system security standards. ✓
- **CNC controller experience**: Maxime has worked with both Haas and Fanuc controllers in networked environments. Nadine's shop uses Fanuc. ✓
- **CAM workstation security**: Maxime secured a Mastercam workstation at his own facility. Nadine uses Mastercam. ✓
- **Small-shop context**: Maxime's own shop is 14 people. He understands that "network segmentation" in a small shop means a managed switch and VLAN configuration, not an enterprise-grade firewall appliance. ✓
- **Deliverables**: Maxime has already written the exact documents Nadine needs — policy, segmentation plan, incident response, training materials — for his own facility. He can adapt them, not invent them from scratch. ✓
- **Language**: French. ✓
- **Budget alignment**: 50 hours × $85/hour = $4,250 — well within Nadine's $8,000 ceiling. ✓

The match confidence is high. Both parties receive notifications.

Nadine sees:

> *"Nous avons identifié un superviseur de production dans un atelier d'usinage de précision au Québec qui détient une certification GICSP en cybersécurité industrielle. Il a segmenté le réseau OT/IT dans son propre atelier (contrôleurs Haas et Fanuc, poste Mastercam), rédigé une politique de cybersécurité et un plan de réponse aux incidents, et a passé un audit cybersécurité client. La portée de travail correspond à vos besoins documentés. Tarif estimé : 4 000 à 5 500 $ pour 50 à 60 heures. Souhaitez-vous voir son profil de compétences détaillé?"*

Maxime sees:

> *"Un fabricant de cylindres hydrauliques à Trois-Rivières a besoin d'aide en cybersécurité industrielle — segmentation réseau OT, rédaction de politiques, formation des employés, documentation d'auto-évaluation. L'atelier utilise des contrôleurs Fanuc et Mastercam dans un environnement similaire à ce que vous avez sécurisé chez Usinage Précision. Portée estimée : 40 à 60 heures sur 4 à 6 semaines. Votre disponibilité et votre profil de compétences correspondent aux exigences. Souhaitez-vous examiner les détails?"*

---

### 5. What the Platform Knows

When CME configured the platform, they populated the **Knowledge Slot** with domain-specific reference material curated by cybersecurity and manufacturing experts:

- **IEC 62443 requirements mapped to shop sizes**: a simplified matrix showing which security levels (SL-1 through SL-4) are expected for different manufacturing contexts — a 20-person job shop has different requirements than a 500-person Tier 1 automotive supplier
- **Common CNC controller network architectures**: reference diagrams for Fanuc, Haas, Siemens, and Mazak controller networking, including which models support VLANs natively and which require external managed switches
- **NIST SP 800-82 templates**: editable versions of cybersecurity policy documents, incident response plans, and self-assessment checklists adapted for small and medium manufacturers — in both English and French
- **Canadian Centre for Cyber Security (CCCS) guidelines**: the government's recommended cybersecurity baseline for small organizations, cross-referenced to IEC 62443 requirements
- **Skills engagement contract templates**: standard terms for fractional engagements between SMBs, covering IP protection, non-competition scope, liability allocation, and payment terms — vetted by CME's legal team

The Knowledge Slot carries domain metadata tags — `cybersecurity`, `IEC_62443`, `CNC_controllers`, `OT_network`, `SMB_manufacturing` — that scope retrieval so that when Nadine asks "What does network segmentation actually mean for my shop?", the platform surfaces CNC-specific guidance, not enterprise IT architecture documents.

---

### 6. The Engagement

Maxime drives to Trois-Rivières on a Saturday morning — a three-hour drive. He walks through Nadine's shop floor with her, looking at the network architecture. He identifies the problems in twenty minutes: the Fanuc controllers, the Mastercam workstation, the ERP terminal, and Étienne's gaming-turned-office computer are all on the same flat network. The shop's Wi-Fi router serves both the production floor and the office, with a default admin password that has never been changed.

Maxime has seen this before. It's the same configuration his own shop had four years ago. He knows the fix because he's already done it.

Over the next five weeks, Maxime works approximately twelve hours per week — some on-site in Trois-Rivières, some remotely from Sherbrooke. He:

- Segments the OT network: configures a managed switch to create separate VLANs for CNC controllers, the CAM workstation, and office IT
- Enables MFA on the ERP system and all administrative accounts
- Writes a cybersecurity policy document — adapted from the one he wrote for Usinage Précision, modified for Nadine's specific environment and Fanuc controllers
- Drafts an incident response plan and a business continuity procedure
- Conducts a two-hour training session for all twenty-two employees, in French, covering phishing recognition, password hygiene, and the specific risks of USB drives on CNC machines
- Completes the Scandinavian OEM's cybersecurity self-assessment questionnaire with Nadine, documenting every control they've implemented

Total billable hours: fifty-three. Total cost: $4,505. Time to completion: five weeks.

For comparison: the Montréal consulting firms quoted $25,000+ and eight to twelve weeks — and neither had CNC shop floor experience.

---

## 7. What Makes This a Thin Market Story

Step back from the narrative and look at the structural forces:

**Opacity** — This is the dominant barrier. Maxime's cybersecurity competence is invisible to anyone outside Usinage Précision Estrie. It doesn't appear on LinkedIn (his profile says "production supervisor"). It doesn't appear in any industry directory. It doesn't appear on any freelance platform. The skill exists, it's proven, and it's available — but it is completely opaque to the market. Multiply this by every SMB employee in Canada who carries a specialist skill from a previous career, a side qualification, or a self-taught competence that their current employer has already consumed. The aggregate surplus is enormous and entirely invisible.

**Discovery** — Nadine in Trois-Rivières and Maxime in Sherbrooke had no mechanism to find each other. The consulting firms she called don't know Maxime exists. Upwork doesn't know he exists. CME's member directory doesn't list individual employees' secondary competences. The traditional mechanisms for skills discovery — job boards, consulting directories, professional associations — are designed around full-time roles and dedicated practices, not fractional surplus capacity inside SMBs.

**Information asymmetry** — Even if Nadine could somehow discover Maxime, how would she evaluate whether his cybersecurity skills are genuine and relevant? A GICSP certification tells her something, but what she really needs to know is: *has this person actually secured a CNC shop floor?* The platform's match report answers that question structurally — matching demonstrated competence (what Maxime has actually done at his own facility) against specific requirements (what Nadine's shop needs), rather than relying on credential proxies alone.

**Trust** — Fractional skills sharing between SMBs introduces a trust architecture that doesn't exist in traditional consulting. Nadine is giving Maxime access to her network infrastructure. Marc-André is lending out his production supervisor. Both need institutional protections: IP agreements, non-compete boundaries, liability allocation. The platform's engagement framework — drawn from the Knowledge Slot's vetted contract templates — provides these protections without requiring either party to hire a lawyer.

**The taxonomy problem** — Manufacturing's expanding skill perimeter means that the skills SMBs need are increasingly exotic combinations: not "cybersecurity" (generic) but "cybersecurity for CNC-networked manufacturing environments" (specific). Not "quality management" (generic) but "ISO 13485 documentation for contract medical device machining" (specific). Keyword matching fails because the intersections are too narrow. Only semantic matching — understanding that GICSP certification plus Fanuc controller experience plus VLAN configuration experience equals "manufacturing OT cybersecurity" — can navigate these compound requirements.

---

*The story of Nadine and Maxime is fictional, but the skill gaps, consulting costs, and market dynamics are real. CME or a similar industry association could build this kind of fractional skills marketplace using the [DeeperPoint toolkit](https://deeperpoint.com/thin-markets.html).*

*[The MarketForge platform →](https://deeperpoint.com/marketforge.html) · [Who should build this? →](https://deeperpoint.com/who-should-care.html)*
