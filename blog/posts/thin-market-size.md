<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->

---
title: "How Big Is the Thin Market Problem? Trillions in Missing Commerce, Sector by Sector"
slug: thin-market-size
date: 2026-03-10
tags: [thin-markets, market-design, ai, explainer, marketforge, investors]
summary: "We scanned the full economy — every NAICS sector, plus cross-border trade and labour markets — to estimate the value of commerce that doesn't happen because of thin market friction. The answer: $5.7–10.4 trillion globally. This isn't speculation; it's anchored in the academic transaction cost literature and validated sector by sector."
estimated-read: 12 min read
---

<figure class="blog-hero">
  <img class="blog-hero__img" src="../images/blog/market-size-hero.jpg" alt="The visible market is the surface. The missing transactions underneath are worth trillions." loading="lazy">
  <figcaption>The visible market is the surface. The missing transactions underneath are worth trillions.</figcaption>
</figure>

## The Question Nobody Has Answered

Every new market platform launches with a TAM slide. "The global $X market is worth $Y billion." These numbers are typically wrong — not because the market isn't large, but because the slide measures the *existing* market, not the *missing* one.

Thin markets are different. The whole point of a thin market is that willing buyers and sellers exist but cannot find each other, cannot evaluate each other, or cannot structure a deal even when they do. The transactions that *should happen* but *don't* — those are the opportunity. And nobody measures them, because by definition they leave no trace in the data.

We tried anyway. Starting from the full economy — every NAICS sector — we asked: *what fraction of potential transactions in each sector fail to occur because of thin market forces?*

| | **Economy-Wide Estimate** |
|---|---|
| **Method** | Top-down from full NAICS sectoral GDP taxonomy |
| **Canada** | **$76–141B** (2.7–5.0% of GDP) |
| **Global** | **$5.7–10.4 trillion** (5.2–9.5% of GDP) |

Before you dismiss the larger number, understand what it includes — and what it doesn't. These are not market sizes. They are *missing transactions*: commerce that would create value for both parties if the matching infrastructure existed.

---

## The Method: A Four-Factor Model

The analysis applies a four-factor model to each sector of the economy:

```
Sector GDP
  × Transaction intensity (share of GDP involving discrete matching-dependent transactions)
  × Thin market fraction (share of those transactions suffering from thin market forces)
  × Addressability (share of that friction reducible by AI-driven matching)
  = Recoverable thin market transaction value
```

**Transaction intensity** asks: how much of this sector's output depends on discrete, matching-dependent transactions — as opposed to commodity flows, regulated tariffs, or internally provisioned work? A construction company that matches subcontractors to projects has high transaction intensity. A utility distributing electricity over a regulated grid has low intensity.

**Thin market fraction** asks: of those matching-dependent transactions, what share suffers from thin market forces — information asymmetry, discovery failure, trust deficit, offering complexity, or participant scarcity? Most grocery transactions are thick. Most heritage masonry subcontractor searches are thin.

**Addressability** asks: what share of that friction can be reduced by AI-driven matching, as distinct from friction that requires physical infrastructure (cold storage), institutional reform (credential treaties), or regulatory change (telehealth licensing)? The platform provides the matching layer; some friction is structural and not software-solvable.

---

## Anchoring to the Academic Literature

This isn't speculation. It's bounded by decades of empirical work on transaction costs.

Wallis and North (1988) measured total transaction costs in the U.S. economy at approximately **55% of GDP** — all costs of using the price mechanism: search, negotiation, monitoring, enforcement. Similar studies found 60% in Australia (1991) and 35% in Argentina (1990). North (1990) showed that institutional quality is the primary determinant of where in that range a country falls.

Thin market costs are a *subset* of those transaction costs: specifically, the costs of transactions that **fail to occur at all**. Not "expensive transactions" — "missing transactions." The grocery store works. Amazon works. Most labour markets clear. The thin market problem arises in the long tail — where offerings are heterogeneous, participants are scarce or dispersed, and the information required to evaluate fit is complex.

Our estimate of 2.7–5.0% of GDP (for Canada) represents **5–9% of total transaction costs**. That is a plausible fraction for the subset where participants exist and want to transact but can't find or evaluate each other — bounded well below the 55% total and well above zero.

---

## Canada, Sector by Sector

**Canada GDP (2024):** ~CAD $2,800B | **Source:** Statistics Canada Table 36-10-0434-01

| NAICS | Sector | GDP ($B) | Trans. Int. | Thin Frac. | Address. | Recoverable ($B) |
|---|---|---|---|---|---|---|
| 11 | Agriculture, Forestry, Fishing | $44 | 70% | 12–18% | 50–65% | $1.8–3.6 |
| 21 | Mining, Oil & Gas | $118 | 40% | 5–8% | 30–40% | $0.7–1.5 |
| 22 | Utilities | $50 | 20% | 8–12% | 40–50% | $0.3–0.6 |
| 23 | Construction | $165 | 65% | 10–15% | 45–55% | $4.8–8.8 |
| 31–33 | Manufacturing | $207 | 55% | 12–18% | 50–60% | $6.8–12.3 |
| 41 | Wholesale Trade | $120 | 65% | 8–12% | 50–60% | $3.1–5.6 |
| 44–45 | Retail Trade | $130 | 75% | 3–5% | 30–40% | $0.9–2.0 |
| 48–49 | Transportation & Warehousing | $105 | 60% | 10–15% | 50–60% | $3.2–5.7 |
| 51 | Information & Culture | $75 | 50% | 12–18% | 55–65% | $2.5–4.4 |
| 52 | Finance & Insurance | $175 | 35% | 5–8% | 35–45% | $1.1–2.0 |
| 53 | Real Estate, Rental, Leasing | $350 | 30% | 8–15% | 40–50% | $3.4–7.9 |
| **54** | **Professional, Scientific, Technical** | **$160** | **80%** | **15–22%** | **55–70%** | **$10.6–19.7** |
| 55 | Management of Companies | $25 | 20% | 3–5% | 25–35% | $0.04–0.1 |
| 56 | Admin, Support, Waste Mgmt | $65 | 70% | 12–18% | 50–60% | $2.7–4.9 |
| 61 | Educational Services | $120 | 40% | 8–12% | 40–50% | $1.5–2.9 |
| 62 | Health Care & Social Assistance | $195 | 45% | 10–15% | 40–55% | $3.5–7.2 |
| 71 | Arts, Entertainment, Recreation | $25 | 65% | 18–25% | 55–65% | $1.6–2.6 |
| 72 | Accommodation & Food Services | $55 | 70% | 10–15% | 45–55% | $1.7–3.2 |
| 81 | Other Services | $55 | 75% | 15–22% | 50–60% | $3.1–5.4 |
| 91 | Public Administration | $195 | 25% | 8–12% | 30–40% | $1.2–2.3 |
| — | **Cross-border trade** | $800 | 45% | 10–15% | 45–55% | $16.2–29.7 |
| — | **Labour market mismatch** | $1,400 | 15% | 8–12% | 35–50% | $5.9–12.6 |
| | | | | | **TOTAL** | **$76–141B** |

---

## Where the Big Numbers Come From

The sector table is not a uniform smear — the thin market problem concentrates sharply. Five sources account for over 60% of the Canadian total.

### Professional, Scientific & Technical Services — $10.6–19.7B

The single largest domestic source of thin market friction. This sector earns the highest scores on all three multipliers: 80% transaction intensity (nearly all output involves bespoke matching), 15–22% thin fraction, and 55–70% addressability.

The mechanism is straightforward: every time an SME in Kitchener pays a generalist accountant because they can't find the industry-specialist CPA they need, that's a thin market loss. Every time a biotech startup in Montréal settles for a CRO that's adequate but not ideal because the ideal partner in Bangalore is invisible to them, that's recoverable value. The transaction isn't priced wrong — it never happens at all, replaced by a second-best match that leaves value on the table.

This sector also has the highest addressability because the matching problem is fundamentally informational. The specialists exist. The clients exist. What's missing is curated discovery — exactly what AI-driven matching excels at.

### Cross-Border Trade — $16.2–29.7B

The largest overall category. Canada's trade exceeds $800B annually, but the conventional picture — pipelines, auto parts, softwood lumber — is all thick-market trade flowing through established channels. The thin fraction sits in the differentiated, small-lot, specialist-service tail: specialty grain varieties that a craft brewer in the Philippines actually wants, niche industrial components that a machine shop in Uruguay actually needs, consulting expertise that a government ministry in Kenya would actually pay for.

The thin market fraction (10–15%) is moderate for any single corridor. But the bilateral corridor count for Canada alone — roughly 60 meaningful trade partners — means thin friction compounds geometrically. A 10% thin fraction across 60 corridors represents vastly more missing commerce than a 10% fraction in a single domestic market.

### Manufacturing — $6.8–12.3B

Beyond the visible surplus equipment market, manufacturing harbours deep thin markets in three areas:

- **Component sourcing for SMEs.** Large OEMs have procurement departments. A 50-person manufacturer in rural Ontario searching for a specialized powder-coating supplier operates in a thin market.
- **Contract manufacturing matching.** Idle capacity and unmet demand coexist because neither side can discover the other.
- **Industrial waste-to-input matching.** One plant's waste stream is another's raw material — but cross-sector discovery is nearly nonexistent.

### Construction — $4.8–8.8B

General contractors in secondary cities struggle to find certified subcontractors for heritage masonry, geothermal drilling, passive house envelope work, or industrial heritage restoration. The Heritage Craft [story post](../blog/heritage-craft-thin-market.html) documents one instance — a $140–220K barn restoration — but the pattern extends across every construction specialization that is low-frequency and high-skill.

The 65% transaction intensity reflects that construction is fundamentally a matching business: every project assembles a unique team. The 10–15% thin fraction reflects that most subcontractor matching (drywall, electrical, plumbing) is thick, but the specialty tail is long.

### Labour Market Mismatch — $5.9–12.6B

Immigrant credential recognition is the most visible form, but the broader category includes:

- **Skilled trades matching across provinces** — a journeyman welder in New Brunswick and a welding shop in Alberta can't find each other
- **Academic-to-industry transition** — PhDs with directly applicable expertise are invisible to the companies that need them
- **Micro-credential matching** — workers who have completed industry certifications are not discoverable by employers seeking those specific skills
- **Volunteer and pro bono matching** — lawyers, doctors, and engineers willing to donate time cannot be matched to organizations that need them

The $1,400B base (total employment income) has low transaction intensity (15%) because most employment is recurring. But the thin fraction (8–12%) of the matching-dependent slice captures the chronic mismatch between skills available and skills sought.

---

## Global: The Developing Economy Multiplier

The Canadian model provides the framework, but two critical adjustments drive the global estimate.

### Developing Economies Have Thicker Thin Markets

In developing economies — roughly 40% of global GDP — thin market friction is structurally 1.5–2.5× higher than in advanced economies. The reasons compound:

- **Weaker information infrastructure.** No MLS, no SEDAR, no standardised industry databases. Discovery depends on personal networks, which are geographically bounded.
- **More severe regulatory fragmentation.** In the Ethiopia produce [story](../blog/ethiopia-produce-thin-market.html), a 16-farmer corridor demonstrates the pattern: smallholders face 30% post-harvest loss and 50%+ information asymmetry margin capture by middlemen — not because middlemen are predatory, but because there is no alternative discovery mechanism.
- **Greater geographic dispersion.** Rural producers and urban consumers are separated by poor transport infrastructure, making the matching problem physical as well as informational.
- **Less developed trust institutions.** No credit bureaus, no contract enforcement courts, limited insurance markets. Trust deficit — one of the five thin market forces — is structurally higher.

North (1990) demonstrated empirically that institutional quality is the primary determinant of transaction cost levels. In countries with weak institutions, a larger share of potential transactions never occur.

### Cross-Border Thin Markets Scale Geometrically

With approximately 195 countries, the number of potential bilateral trade corridors (~19,000) vastly exceeds any single country's internal market. Most of these corridors carry zero or negligible trade *specifically because* of thin market conditions — neither side has the information infrastructure to discover or evaluate counterparties.

This is not hypothetical. The malting barley [story](../blog/malting-barley-thin-market.html) — Saskatchewan to Cebu — involves a corridor that carries real trade ($0) in the specific variety. The demand exists. The supply exists. The transaction doesn't, because the corridor is invisible.

### The Global Table

| Economy Group | GDP ($T) | Thin Market % | Recoverable ($T) |
|---|---|---|---|
| Advanced economies (G7 + EU + AUS/NZ/KR/SG) | $65 | 2.5–4.5% | $1.6–2.9 |
| Middle-income (China, India, Brazil, ASEAN, etc.) | $35 | 4.0–7.0% | $1.4–2.5 |
| Low-income and fragile states | $5 | 6.0–10.0% | $0.3–0.5 |
| Cross-border thin markets (incremental) | $30T trade vol. | 8–15% | $2.4–4.5 |
| | | **TOTAL** | **$5.7–10.4T** |

The gradient is the finding: the poorer the economy, the higher the thin market fraction; the more borders involved, the more friction compounds. The economic and social returns to solving thin markets are highest precisely where they are thickest.

---

## What "Recoverable" Means — and Doesn't

These figures represent **incremental transaction value**: commerce that would create value for both parties but currently does not occur. This is distinct from:

- **Total market size** — most of each market works through existing channels
- **Revenue to a platform operator** — platform fees would be a small fraction of transaction value
- **GDP contribution** — which would include multiplier effects, typically 2–3× direct transaction value

The GDP contribution from unlocking this value — accounting for employment, tax revenue, input purchases, and reduced waste — would be substantially larger than the direct transaction figures. If even a fraction of the $5.7–10.4 trillion were recovered, the second-order effects on economic growth, particularly in developing economies, would be transformative.

---

## Assumptions and Caveats

Five assumptions deserve explicit scrutiny:

1. **Thin fraction is the hardest number.** It is calibrated against: the transaction cost literature (bounding total friction at ~55% of GDP), DeeperPoint's per-transaction story post evidence (showing 50–300% value capture improvements), and the internal consistency check (our estimate should be 5–10% of total transaction costs). Small changes in this assumption produce large swings.

2. **Addressability is conservative.** Some thin market friction requires physical infrastructure (cold storage), institutional reform (credential recognition treaties), or regulatory change (telehealth licensing). The platform provides the matching layer; structural friction is excluded.

3. **The informal sector is not counted.** In developing economies, 30–60% of economic activity is informal. Much of this is thin-market-driven — the Ethiopian produce chain is largely informal. Including the informal sector would increase the global estimate substantially.

4. **These are steady-state estimates**, not year-one targets. Reaching the full estimate would require thousands of platforms across hundreds of verticals over a 10–20 year horizon. The number describes the size of the *problem*, not the size of any single company's addressable market.

5. **Transaction intensity, thin fraction, and addressability** all vary enormously *within* sectors. Real estate includes both standardised apartment rentals (not thin) and adaptive-reuse commercial matching (very thin). The per-sector figures are weighted averages across a wide internal distribution.

---

## The Actionable Takeaway

**For policymakers**, thin markets are not a niche phenomenon or a curiosity of exotic commodities. They are a structural feature of every economy — representing 2.7–5.0% of Canadian GDP and 5.2–9.5% of global GDP in missing commerce. They intensify in developing countries and across borders, which is precisely where the economic and social returns to solving them are highest. Any trade strategy, workforce development program, or economic development initiative that ignores thin market friction is leaving trillions unrealised.

**For sponsors and investors**, the sector table identifies *where* to look. Professional services, cross-border trade, manufacturing, construction, and labour markets are the five highest-value concentration points. A sponsor building a MarketForge deployment in one of these sectors can point to a specific, bounded opportunity within a rigorously estimated total.

**For the discipline of market engineering**, the wide estimate — $5.7–10.4 trillion globally — defines the field. It says that across the entire global economy, transactions worth 5–10% of GDP are not happening because the matching infrastructure doesn't exist. This is not a market to be *captured* by a single platform. It is a *landscape* to be addressed by an ecosystem of sponsor-configured, AI-driven matching platforms, each solving a specific vertical's thin market problem.

---

*The detailed methodology, per-sector tables, and full NAICS analysis underlying this post are documented in the DeeperPoint reference library. Academic anchoring uses Wallis & North (1988), Coase (1937/1960), North (1990), Akerlof (1970), and Stiglitz & Weiss (1981).*

*[What makes a thin market tick? →](../thin-markets.html) · [The Opportunity Catalog →](../catalog/index.html) · [The MarketForge platform →](../marketforge.html)*
