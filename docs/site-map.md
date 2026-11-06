# deeperpoint.github.io: site map and table of contents

Snapshot of the site as it stands in the repository on 2026-11-06 (commit e7f7518; first built at c7784d6 the same morning and refreshed after the day's changes), read from the HTML, YAML and Markdown on disk rather than from the live site. It exists to make overlaps, duplications and breaks in the logic flow visible in one place. Section 8 lists the candidates noticed while building the map; the judgement on each is the owner's.

**Changes between the two snapshots (all 2026-11-06, owner's decisions):**

- The fifteen cards moved under What We're Building. cards/index.html is now a viewer (one card on stage, arrows, keys, swipe, a menu of all fifteen, full screen, `#<slug>` deep links) that carries the site nav; the doorway block moved from Market Physics to platform.html; the Library's cards and slides tiles are gone; Home's three thumbnails open the viewer on their card. One-line cross-references remain on Market Physics and the Library.
- ClientSynth is presented as a peer of Cosolvent and CommonContext: one tile on platform.html (the separate block at the foot of the page is gone; its two-jobs paragraph moved to mf-clientsynth.html) and the same grid on cosolvent.html (the "Proprietary Testing Harness" section and its BUSL-1.1 label are gone).
- ClientSynth's licence reads "Apache 2.0 with one condition" everywhere, with the condition stated beside it. The site no longer calls ClientSynth open source, because `ClientSynth/LICENSE` says it is not open source under the Open Source Definition; nor does it say source-available, except on the hackathon page.

Sections 7 and 8 end with what those changes resolved and what they did not.

How to read it:

- **Path** is the file under the site root; the live URL is `https://deeperpoint.com/<path>`.
- **Revised** is the last commit that changed the page's content before the November 2026 reorganisation of the navigation. Pages marked *Nov 2026* were rewritten or materially changed in that reorganisation (2026-11-03 to 2026-11-06).
- **In** lists the pages whose body text links to this page (navigation and footer links are excluded, so this shows editorial reachability). **Out** lists what the page's body links to.
- Section headings are given as they appear on the page, each with a one-line gist.

---

## 1. The site at a glance

| Part of the site | Pages | Notes |
|---|---|---|
| Top-level pages in the navigation tree | 27 | Listed in sections 2 and 3 |
| Hidden pages (noindex, out of nav) | 6 | Who It's For and its five guides |
| Redirect stubs | 5 | examples, project, thin-markets, mf-curation, blog/knowledgeslot-schema-scoped-rag |
| Unlinked side pages | 3 | hackathon/, tools/blackwidow-simulator, assets/business-card |
| Cards | 16 | Viewer (one card at a time, arrows and menu) plus 15 standalone cards, synced from DeeperPointComms |
| Catalog | 1 + 313 | 254 entries built from YAML, plus 59 orphan pages from retired sectors |
| Blog | 1 + 78 + 7 | 56 posts with Markdown sources, 22 orphan posts, 7 series pages (1 current) |
| PDFs | 16 | 8 under assets/mysitedocs (2 unlinked), 8 MarketMap reports |

Navigation, as set in `update_nav.py` and mirrored in the blog and catalog builders:

| Nav item | Target | Also shown as current on |
|---|---|---|
| Home | index.html | |
| Why Markets Don't Form | market-physics.html | intervention-matrix, whitepaper |
| What We're Building | platform.html | how-it-works, demo, cosolvent, marketforge, mf-cosolvent, mf-commoncontext, mf-clientsynth, architecture, cards/ |
| Catalog | catalog/index.html | catalog/ |
| Library | library.html | ebook, precis, pitch-deck, search, testbeds, marketmaps, market-diagnostic, examples |
| Blog | blog/index.html | blog/ |
| About | about.html | mission |
| Contribute (button) | contribute.html | |

---

## 2. The navigation tree

Indentation shows how a visitor reaches a page from the nav. A page shown under two parents is linked from both. Pages in *italics* are reachable only through the parent shown, not from any other page's body text.

```
Home                                   index.html
├─ Why Markets Don't Form              market-physics.html
│  ├─ The Intervention Matrix          intervention-matrix.html
│  ├─ Whitepaper                       whitepaper.html   (+ MarketTheoryWP.pdf)
│  └─ How It Works                     how-it-works.html
├─ What We're Building                 platform.html
│  ├─ How It Works                     how-it-works.html
│  ├─ The fifteen cards                cards/index.html  →  cards/<slug>.html ×15 (+ resistance-cards.pptx)
│  ├─ *How an Implementation Is Built* architecture.html
│  ├─ Live demo (ForgeTwin)            demo.html  →  external Vercel app
│  ├─ Cosolvent Suite hub              cosolvent.html
│  │  ├─ Cosolvent                     mf-cosolvent.html   (+ Coswebroadmap.pdf, GitHub cosolvent-beta)
│  │  └─ ClientSynth                   mf-clientsynth.html (+ ClientSwebroadmap.pdf)
│  ├─ CommonContext                    mf-commoncontext.html (+ KSwebroadmap.pdf)
│  ├─ ClientSynth                      mf-clientsynth.html
│  └─ MarketForge roadmap              marketforge.html (+ MarketForgeCreationGuide.pdf)
├─ Catalog                             catalog/index.html  →  catalog/<slug>.html ×254
├─ Library                             library.html
│  ├─ Whitepaper                       whitepaper.html
│  ├─ The Intervention Matrix          intervention-matrix.html
│  ├─ The Middle Power Pivot           ebook.html (+ TheMiddlePowerPivot.pdf)
│  │  ├─ Executive précis              precis.html
│  │  └─ Pitch deck                    pitch-deck.html   (no nav bar)
│  ├─ The Mission                      mission.html
│  ├─ Search                           search.html
│  ├─ Opportunity Catalog              catalog/index.html
│  ├─ *Thin-Market Test Beds*          testbeds.html
│  ├─ MarketMaps                       marketmaps.html  (+ 8 Convoy PDFs)
│  ├─ Market Scenarios                 blog/index.html (Market Scenario stream)
│  ├─ *Market Engineer's Diagnostic*   market-diagnostic.html
│  └─ Live demo                        demo.html
├─ Blog                                blog/index.html  →  51 public posts, 1 series page
├─ About                               about.html
│  └─ The Mission                      mission.html
└─ Contribute                          contribute.html  →  GitHub repos, cards, whitepaper, catalog, marketmaps, mf-commoncontext

Hidden (noindex, no nav link, no body link from any live page except as noted)
   who-should-care.html   ← linked from 20 blog posts ("Who should build this?")
   ├─ guide-founders.html
   ├─ guide-investors.html
   ├─ guide-accelerators.html
   ├─ guide-associations.html
   └─ guide-government.html

Not linked from anywhere
   hackathon/index.html            DeeperPoint Suite architecture (noindex, nofollow)
   tools/blackwidow-simulator.html Black Widow payment-terms simulator
   assets/business-card/business-card.html
   blog/series/*.html ×6           retired series landing pages
   blog/*.html ×22                 orphan posts (see 4.3)
   catalog/*.html ×59              orphan entries (see 4.2)

Redirects
   examples.html → library.html#examples      project.html → platform.html
   thin-markets.html → market-physics.html    mf-curation.html → mf-commoncontext.html
   blog/knowledgeslot-schema-scoped-rag.html → blog/commoncontext-schema-scoped-rag.html
```

---

## 3. Page by page

### 3.1 Home

**index.html** · *DeeperPoint — Activating Thin Markets with AI* · Revised: Nov 2026 (rewritten) · In: pitch-deck, catalog/index, one blog post · Out: market-physics, platform, cards (the viewer, opened on trust, opacity and cold-start), catalog, library, contribute, about

- **Markets don't make themselves.** (h1) Hero: thousands of markets never form; "we call them thin markets"; eighty years of economics explains why; the frictions can now be engineered away. Buttons to Why markets don't form and What we're building; pill "Open source · MIT · contributors welcome".
- Three card thumbnails (Trust, Opacity, Cold Start), each opening the viewer on that card, and "See all fifteen cards".
- Six question tiles: Why don't some markets form? · What are you building? · Show me the markets ("Hundreds of prospective thin markets across 29 sectors") · What should I read, and where does it apply? · Can I help? · Who is behind this?
- **Built in the Open.** The friction-fighting layer is built once and reused; free, MIT-licensed; links to How to contribute and to the MIT rationale on the platform page.

### 3.2 Why Markets Don't Form

**market-physics.html** · *The Market Physics of Thin Markets* · Revised: 2026-07-10, seventh intervention added Nov 2026; the card strip added 2026-11-05 moved to platform 2026-11-06 · In: index, intervention-matrix, mission, testbeds, whitepaper, 54 blog posts · Out: cards (one cross-reference), intervention-matrix, whitepaper (page and PDF), catalog, how-it-works, platform

- **Thick Markets, Thin Markets.** Defines thick (easy discovery, fair prices, quick, confident) and thin as its opposite.
- **Eighty Years of Evidence.** Nobel-recognised research mapped the forces.
- **How Markets Get Built Today.** Pick a product, build a web platform, then the real work begins.
- **The Seven AI Interventions.** 1 AI Matching · 2 AI Trusted Intermediary · 3 AI Input Translation · 4 AI Memory & Active Sourcing · 5 AI-Enabled Aggregation · 6 AI Risk Insulation · 7 AI Synthetic Bootstrapping, each with "Covers:" challenges.
- **Where the Interventions Become Visible: the Content Match Story.** Participants see a document, not a capability; the story becomes the Deal Brief.
- Four closing tiles: Open the full Intervention Matrix (with the one-line pointer to the cards) · Read the full whitepaper · Browse the catalog ("Hundreds of searchable scenarios") · Download the whitepaper PDF. "Continue →" goes to platform.

**cards/index.html** · *Thin-Market Resistances* · Synced 2026-11-06 from DeeperPointComms/library/resistance-cards (viewer rebuilt that day) · In: index, platform, intervention-matrix, contribute, plus one-line cross-references on market-physics and library · Out: platform, intervention-matrix, the scenario post behind each card, the deck and the PNGs

- Carries the site navigation with What We're Building active; crumb to What we're building and the Intervention matrix. "15 reasons a market stays thin, one per card"; the matrix is the exhaustive crossing.
- One card on stage at a time: arrows either side, ← → keys, swipe, a menu of the fifteen grouped as existential gates and resistances, Full screen, and `#<slug>` deep links (cards/index.html#trust). Under the stage: Open card alone, PNG, Deck (.pptx).
- Each card has What it looks like (an illustrative scenario linked to a blog post), How an AI intervention works, How traditional markets cope, and on six cards "What's new here". The card list is in section 4.1.
- In the static HTML only the first card's Open card alone and PNG links exist; the script rewrites them for the card on stage. The other fourteen standalone pages are therefore reached only through the viewer's script, or from each other's previous and next links (section 7).

**intervention-matrix.html** · *The Intervention Matrix* · Revised: 2026-07-09, regenerated 14×7 from canon Nov 2026 · In: library, market-physics, marketmaps, mission, platform, whitepaper, 9 blog posts, cards viewer · Out: cards, market-physics, platform

- Banner: this is the reference view; the cards are the one-reason-at-a-time view.
- **Traditional Responses.** Standardization, human broker, market maker, storage and futures, co-location, clearinghouse, against fourteen challenges.
- **AI-Powered Interventions.** Seven interventions against the same fourteen challenges; click a cell for the mechanism; legend Strongest / Lowers / Partially / Supporting / Neutral.
- "Back to the Platform" button.

**whitepaper.html** · *Whitepaper: Thin Markets* · Revised: 2026-07-09 · In: contribute, library, market-diagnostic, market-physics, mission, platform, testbeds, who-should-care, 7 blog posts · Out: intervention-matrix, market-physics, catalog

- **Executive Summary.**
- **The Thin Market Problem.** Thinness defined by friction, not transaction volume.
- **Part I: Market Structures.** Counterparty Arrangement · Decision Units: Individuals versus Organizations · Theoretical Maximum Market Size · DeeperPoint's Market Focus (many-to-many in scope).
- **Part II: Market Physics and Challenges.** Desire to Exchange · Existential Threats: Risk, Trust, Laws and Regulations · Resistance Challenges: Offering Complexity, Geographic Distance, Temporal Distance, Opacity, Cognitive Bandwidth, Fulfillment and Settlement · Friction Multipliers.
- **Part III: The Cold Start Problem.**
- **Part IV: Traditional Market Engineering.** Human Brokers · Market Makers · Storage and Futures · Standardization and Certification · The Role of Memory.
- **Part V: The AI Revolution in Market Engineering.** Eight headings: Input Friction Reduction · User Aggregation · AI-Driven Matching · AI as Institutional Memory · Dynamic Pricing and Valuation · Asynchronous Brokerage · Trusted Intermediation · Synthetic Market Bootstrapping.
- **Part VI: The Intervention Matrix.** Pattern statement and a link to the interactive matrix.
- **Part VII: Trust in Thin Markets — A Deeper Treatment.** Progressive trust building.
- **Part VIII: Implementation Strategy.** The Tactical AI Stack: Foundation (LLM + RAG), Integration, Interface layers.
- **What Comes Next.** Four initiatives (Cosolvent, CommonContext, ClientSynth, MarketForge).
- **Part X: Strategic Implications.** AI as the Engineering Solution to Middle Powers Trade. (There is no Part IX.)

### 3.3 What We're Building

**platform.html** · *The Platform* · Revised: 2026-07-10; licence wording, component grid and the cards block revised 2026-11-05 and 2026-11-06 · In: index, architecture, intervention-matrix, market-physics, cards viewer, project (redirect) · Out: cards (viewer, four cards, deck), intervention-matrix, how-it-works, demo, architecture, marketforge, cosolvent, mf-commoncontext, mf-clientsynth, catalog, whitepaper

- **A Market Engine Built Once, For Any Thin Market.** (h1) "MIT License · $0 license cost"; the seven interventions in a generic engine; a sponsor adds the vertical.
- Doorway pills: How it works · Live demo · Cosolvent · CommonContext · MarketForge · ClientSynth · How an implementation is built · Fifteen cards.
- **Free, Open Source, Headless.** Three peer components as free, headless server functionality: Cosolvent and CommonContext under MIT, ClientSynth under Apache 2.0 with one condition (the condition is stated in the boundaries paragraph). *Why MIT? Because adoption is a thin market too.* Tiles labelled by licence: Cosolvent (Open Source · MIT) · CommonContext (Open Source · MIT) · ClientSynth (Apache 2.0 with one condition) · MarketForge (Deployment Framework). The heading still says Open Source over all four.
- **Fifteen Resistances, and What the Engine Does About Each.** (added 2026-11-06, moved from Market Physics) Four card thumbnails (Trust, Decision-Process Opacity, Temporal Distance, Cold Start); buttons to the viewer, the deck and the matrix.
- **How a Deal Forms.** Ingest → … → a deal ready to hand off, as one continuous flow.
- **The Deal Brief — Not a Contract, a Handoff.** The platform's primary output.
- **What Adopters Build On Top.** Branding, UX, legal templates, payment rails.
- Buttons: Walk through a working twin · The architecture in four diagrams · The sponsor's playbook · Live demo · Browse the catalog · Read the whitepaper.

**how-it-works.html** · *How It Works* · Revised: 2026-07-10 · In: architecture, market-physics, platform · Out: demo, catalog, mf-cosolvent, mf-commoncontext

- **From Strangers to Deal Brief.** (h1) Anonymous discovery → refined match story → a document professionals can act on.
- **Profiles — Both Sides Describe Themselves.** Vertical-specific schema (barley grower and craft brewer example).
- **Content Match Story — The Case for the Match.** AI-authored narrative of why the pairing is worth pursuing. *One Story, Refined Until It's a Deal Brief.*
- **Structured Negotiation — Exploring the Fit.** Guided workspace after double opt-in.
- **The Deal Brief — Handoff to Your Professionals.** Structured, non-binding.
- **How This Compares to Other Platforms.** Table: supplier directories, marketplaces, etc., versus what this produces and where its job ends.

**architecture.html** · *How an Implementation Is Built* · Revised: 2026-07-05 · In: platform only · Out: demo, how-it-works, platform

- **The anatomy of an implementation.** Three roles: feeder systems, matching engine, the sponsor's front end.
- **How the three roles operate together.** Swimlanes for one vertical.
- **Inside the matching engine.** Two-stage match funnel; deal assembly; cache.
- **Why it scales: the same engine, replicated per vertical.** Three markets side by side.
- **Two ways to build a market.** Rediscover the frictions alone, or start from the engine. *Where to go next.*

**demo.html** · *Interactive Digital Twin Simulation* · Revised: 2026-07-05 · In: architecture, how-it-works, library, marketforge, platform · Out: external Vercel app only

- **ForgeTwin Simulation Sandbox.** (h1) Three personas (machine shop, aerospace buyer, lab inspector). *Sandbox Simulation Notice*: pre-compiled client-side simulation, no live LLM calls.

**cosolvent.html** · *Cosolvent Suite* · Revised: 2026-07-07; ClientSynth made a peer and relabelled 2026-11-06 · In: guide-founders, guide-investors, market-diagnostic, marketforge, mf-clientsynth, mf-commoncontext, mf-cosolvent, mission, platform, 12 blog posts · Out: mf-cosolvent, mf-clientsynth, catalog

- **Where the Theory Becomes Working Software.** (h1) "We are building the open-source tools to do exactly that, alongside ClientSynth, the synthetic-population harness that tests them."
- **The Three Components.** (until 2026-11-06 "The Open-Source Infrastructure" plus a separate "Proprietary Testing Harness" section) One grid: Cosolvent (Open Source · MIT Licensed) · CommonContext (Open Source · MIT Licensed) · ClientSynth (Apache 2.0 with one condition). *The Customization Boundary* (front end, payments and trust workflows deferred to the sponsor).
- **Browse the catalog of examples.** "Over 250 searchable thin market scenarios."

**mf-cosolvent.html** · *Cosolvent — Headless Marketplace Engine* · Revised: 2026-07-10 · In: cosolvent, how-it-works, one blog post · Out: cosolvent, Coswebroadmap.pdf, GitHub cosolvent-beta

- **Build Without Boundaries.** Open-source layer of "the MarketForge ensemble". *Core Features* (matching engine, deal assembly, …) · *The Content Match Story — Knowing Before Committing* · *The Deal Brief — Platform's Primary Deliverable* · *Scope Boundaries: What We Build vs. What You Build.*
- **Cosolvent Feature Overview.** Implemented / planned feature table. *Structured Contingency Schema (a Deal Brief section)*: currency collar, tariff threshold, regulatory escape trigger.

**mf-commoncontext.html** · *AI CommonContext Curation — MarketForge Ecosystem* · Revised: 2026-07-05 · In: contribute, how-it-works, platform, mf-curation (redirect) · Out: cosolvent, KSwebroadmap.pdf

- Badge "MarketForge • Proprietary".
- **Make The Unmatchable, Matchable.** Semantic "Knowledge Slots"; "the proprietary data-refinement wing of the MarketForge ensemble". *How It Integrates*: extraction, normalization, feeding Cosolvent.
- **CommonContext Feature Overview.** Document ingestion, semantic chunking, and so on.

**mf-clientsynth.html** · *ClientSynthAI — MarketForge Ecosystem* · Revised: 2026-07-07; licence box rewritten 2026-11-05 and 2026-11-06, two-jobs paragraph added 2026-11-06 · In: cosolvent, marketmaps, mission, platform · Out: cosolvent, ClientSwebroadmap.pdf

- Badge "MarketForge • Apache 2.0 with one condition".
- **Safely Test Your Theories.** Two jobs (prove the market physics work; seed the cold start with a visibly synthetic population). Licensing paragraph: Apache License 2.0 with one condition, set out in the ClientSynth Additional Terms (never mixed with real participants, never presented as real, provenance marks kept). *Ethical Usage Policy* box. *Core Advantages*.
- **ClientSynth Feature Overview.** Feature table.

**marketforge.html** · *MarketForge Platform* · Revised: 2026-07-05 · In: mission, platform, 30 blog posts · Out: cosolvent, demo, MarketForgeCreationGuide.pdf

- **The Procedural Marketplace Creation Roadmap.** (h1) Step-by-step path from diagnostic scoping to launch.
- **Core Platform vs. Market Vertical: Dividing the Work.** *Generic Participant Roles* (Supply, Demand, …).
- **The 5-Phase Creation Timeline.** Twelve steps: server environment · market rules · industry documents · aligning terms · legal workarounds · compliance settings · simulated users · sandbox matching tests · user screens · match stories · welcoming users · updating the library.
- **The Digital Twin Architecture.** Local simulation with three groups of simulated users.
- **CommonContext Continuous Curation Loops.** Loop 1 Preparing the Ground · Loop 2 Automatic Profile Helping · Loop 3 Closing the Curation Gaps.
- **Ready to review the software?** "Download the MIT licensed transaction database blocks."

### 3.4 Catalog

**catalog/index.html** · *Startup-Ready Markets in Waiting — Scenarios for the MarketForge Opportunity Catalog* · Generated by scripts/build_catalog.py from catalog/scenarios/*.yaml (254 files, last changed 2026-05-17) · In: index, contribute, cosolvent, how-it-works, library, market-physics, mission, platform, testbeds, whitepaper, who-should-care, 4 blog posts, every entry

- Meta description says "One hundred speculative thin market scenarios"; the page shows "254".
- Intro: each entry is a market that could exist if the matching infrastructure were built; the point is the number of plausible opportunities, not any one.
- Twelve collection cards (counts are typed into the builder, not computed; see 4.2), sector filter (29 sectors), tag and build-complexity filters, then the entry grid.
- Each entry page: market analysis, sponsor revenue models, forces, a narrative match story; some link to the blog scenario that dramatises them.

### 3.5 Library

**library.html** · *Library* · Nov 2026 (new; absorbed examples.html; cards and slides tiles removed 2026-11-06) · In: index, examples (redirect) · Out: whitepaper, cards (one cross-reference), intervention-matrix, ebook, precis, pitch-deck, mission, search, catalog, testbeds, marketmaps, blog, market-diagnostic, demo

- **The documents.** Whitepaper · The Intervention Matrix · The Middle Power Pivot (with Executive précis and Pitch deck links beneath it) · The Mission · Search the Site.
- **Worked examples.** Opportunity Catalog ("29 sectors") · Thin-Market Test Beds ("Twenty markets") · MarketMaps · Market Scenarios (blog stream) · Market Engineer's Diagnostic · Live Demo. Closing note on how to read an example.

**ebook.html** · *The Middle Power Pivot — Free Ebook* · Revised: 2026-07-05 · In: library, pitch-deck, precis, one blog post · Out: TheMiddlePowerPivot.pdf, precis, pitch-deck

- **The Middle Power Pivot.** (h1) Working manuscript, March 2026, ~40,000 words.
- **Full Ebook** (PDF) · **Executive Précis** · **Pitch Deck** (three tiles).
- **What's Inside.** Part I Ontario Manufacturing and the Trade War · Part II How Can Ontario Manufacturers Organize to Capture Value? · Part III AI Coordinated Firm-Level Flexible Specialization · Part IV AI Coordinated Operational-Level Cooperative Specialization · Part V From Theory to Practice.
- **Who Should Read This.** Manufacturing executives, association leaders, economic development officials.

**precis.html** · *The Middle Power Pivot — Executive Précis* · Revised: 2026-07-05 · In: ebook, library · Out: ebook, pitch-deck, PDF

- **The Crisis.** Ontario manufacturing employment and the broken OEM arrangement.
- **The Thin Market Problem.** "Twelve distinct friction categories."
- **The Historical Precedent — and Why It Failed.** Italian textile districts and the broker.
- **The AI Alternative.** Overcomes all four failure points.
- **The DeeperPoint Architecture.** Four components: Cosolvent (MIT), CommonContext, MarketForge, ClientSynth.
- **How It Works in Practice.** *Firm-Level Coordination* · *Below the Firm Boundary* (Cooperative Specialization Support System).
- **Governance: Who Owns the Network?** Options A, B, C.
- **The Pilot — and What Comes After.** Fifty SMEs in the Hamilton–Cambridge–Mississauga corridor.

**pitch-deck.html** · *The Middle Power Pivot — Pitch Deck* · Revised: 2026-05-30 · No nav bar; no footer · In: ebook, library, precis · Out: ebook, index, GitHub org

- Fourteen slides: The Crisis (Ontario's Manufacturing Lifeline Is Severed) · The Root Cause (Twelve Frictions That Kill Thin Markets: Trust & Risk, Opacity & Discovery, Offering Complexity, Regulatory Barriers, Geographic & Temporal, Cold Start, "plus cognitive bandwidth · fulfillment · input friction · institutional memory") · Historical Precedent (The Broker Model Always Fails) · The Solution (AI Dissolves All Four Failure Points) · Architecture (Two Altitudes of Coordination) · The Platform (Four Integrated Components) · In Practice (The Virtual Tier-One) · Governance (Who Owns the Network?) · From Theory to Practice (The Pilot: First Fifty Firms) · Measurable Outcomes · The Strategic Trajectory (Ontario → Canada → Federation) · The Thesis · Next Steps ("Cosolvent, MarketForge, CommonContext, and ClientSynth are open-source on GitHub under the MIT licence").

**mission.html** · *The Mission* · Revised: 2026-11-03 (split out of About; essay dated March 2026) · In: about, library, hackathon · Out: about, blog index, two blog posts (thin-market-size, thin-markets-middle-powers), catalog, cosolvent, intervention-matrix, market-physics, marketforge, mf-clientsynth, whitepaper, GitHub Cosolvent

- **Part 1 The Veterinarian's X-Ray.** The zoo analogy · Two kinds of failure (latent and degraded) · Why this matters to me personally.
- **Part 2 Trillions in the Shadows.** The invisible economy (four-factor NAICS model) · Where the pain concentrates · The policy dimension (Middle Powers, $37.7 trillion).
- **Part 3 The Skeleton Key.** The DeeperPoint stack ("four layers: Cosolvent is the open-source core…") · The open/proprietary boundary ("the upper layers are proprietary") · The sponsor model.
- **Part 4 An Open Invitation.** My position · What success looks like (three to five sponsored marketplaces) · Who I'm looking for · What I bring · The invitation.

**testbeds.html** · *Twenty Thin-Market Test Beds* · Revised: 2026-07-05 · In: library only · Out: catalog, whitepaper, market-physics

- **Why These Examples Matter.**
- **The Twenty Test Beds.** Table (list in 4.4).
- **What These Examples Share.** Structural Willingness · Unique Force Profiles · Global Scope · Actionable Today.
- **The Economic Prize.**
- Closing tiles: Explore each test bed in detail ("In-Depth View" goes to the catalog) · Read the full whitepaper · Browse the full catalog ("Over 100 searchable scenarios") · What are thin markets?

**marketmaps.html** · *MarketMap Forensic Engine* · Revised: 2026-07-17 · In: contribute, library · Out: intervention-matrix, mf-clientsynth, 8 Convoy PDFs

- **The MarketMap Synthesis Engine.** (h1) "A strict 11-challenge framework and multi-model AI synthesis."
- **What is a MarketMap?** *Our Methodology* (three models, independent generation, synthesis).
- **Assessing Strategy Viability.** 1 Market Gravity · 2 Business Model Physics · 3 Evidence Quality & Signal · 4 Pre-Launch Market Engineering.
- **The Research Library.** Case Study: Convoy — Two Eras, One Engine · Convoy — Before the Fall (blinded to June 2023) · Convoy Reborn — The DAT Platform (2026) · Methodological Notes.

**market-diagnostic.html** · *Market Diagnostic* · Revised: 2026-07-09 · In: library only · Out: whitepaper, cosolvent

- **Before You Begin.**
- **1. Market Structure.** Counterparty Arrangement · Participant Types · Theoretical Maximum Market Size.
- **2. Desire to Exchange.** Structural · Transient.
- **3. Existential Threats — Risk.** Exogenous Risk Exposure.
- **4. Existential Threats — Trust & Regulation.** Trust · Regulatory Friction (Exogenous - EMU).
- **5. Resistance — Complexity & Distance.** Offering Complexity · Geographic Distance · Temporal Distance · Technological Obsolescence.
- **6. Resistance — Opacity, Cognition, Fulfillment & Fragmentation.** Opacity · Cognitive Bandwidth · Fulfillment & Settlement · Participant Fragmentation.
- **7. The Cold Start Problem.**
- Buttons: Read Full Whitepaper · Explore Building Tools (cosolvent.html).

**search.html** · *Search* · Pagefind full-text search over everything deployed, orphans included · In: library.

### 3.6 Blog

**blog/index.html** · *Blog — Dispatches from the Thin Market Frontier* · Generated by scripts/build_blog.py from blog/posts/*.md · In: library, mission

- Stream tabs: Market Scenario · Workshop Notes · Engineer's Log (posts without a stream fall into "other").
- Pinned: the Shadow Capacity series card and The Virtual Tier-One.
- Post list in 4.3.

### 3.7 About and Contribute

**about.html** · *About* · Revised: 2026-11-03 · In: contribute, index, mission, hackathon · Out: mission, mailto, Substack, LinkedIn

- **The Founder & the Journey.** (h1) Button "Why I'm building this →" to the mission.
- **The Professional Journey Behind the Insight.** Timeline 1974–2026 in four phases: Origins, Academic (1987–2012), iPOV (2000–2014), Recent (2013–2026).

**contribute.html** · *Contribute* · Nov 2026 (new) · In: index (and every nav bar and footer) · Out: about, cards, catalog, marketmaps, mf-commoncontext, whitepaper, GitHub (three repos, issues, CONTRIBUTING)

- **Open to Anyone Who Wants In.** (h1) Self-funded, no investors, no board; MIT engine.
- **The code.** Cosolvent (MIT) · CommonContext (MIT) · ClientSynth (Apache 2.0 with one condition).
- **Help that is not code.** Knowledge of a market · a market to test on · judgment on the catalog and MarketMaps · words on the cards.
- **How to start.** Read the cards or the whitepaper; open an issue; contributor guide; write via About. Closing box: "work and judgment, not money".

### 3.8 Hidden pages (noindex since 2026-11-05)

**who-should-care.html** · *Who Should Care* · In: 20 blog posts ("Who should build this?" and similar calls to action) · Out: five guides, catalog ("over 100 scenarios"), whitepaper. Stakeholder tiles and five Deep-Dive Guides.

Each guide is about 600–800 words, links to `../contact/index.html` (a page that does not exist) and, in two cases, to cosolvent.html:

- **guide-founders.html** Founders: Survive and Thrive in Niche Markets. Mode A The Market Maker (How it Works, The Business Model) · Mode B The Precision Vendor · Ready to Start? ("250+ pre-validated thin markets").
- **guide-investors.html** Early Investors: Find Profitable Monopolies in Mundane Markets. 1 Forensic Due Diligence: The MarketMap · 2 Capital Efficiency: The Cosolvent Engine · 3 The Exit Strategy: Horizontal Aggregation · Directing Your Deal Flow.
- **guide-accelerators.html** Incubator Managers: Build Successes in the Real Economy. 1 The Intake Filter · 2 The Venture Studio Playbook · 3 The Infrastructure Advantage · 4 The "Thin Market Track" · Partner With Us.
- **guide-associations.html** Industry Associations: Build the Digital Market Your Members Need. 1 Weaponize Your Trust · 2 Immunize Against Big Tech · 3 The Great Equalizer: Input Translation · Redefining Member Value.
- **guide-government.html** Trade Policy Makers: Give Small Businesses Global Bidding Power. 1 The AI Trade Commissioner · 2 The Regulatory Rosetta Stone · 3 Sovereign Digital Infrastructure · Building the Mechanisms of Trade.

### 3.9 Unlinked side pages

- **hackathon/index.html** *DeeperPoint Suite — Architecture* (2026-10-03; noindex, nofollow). One engine suite, two populations, a vertical alignment layer: Domain wiki → everything · CommonContext · ClientSynth (source-available) · Cosolvent — the shared backend · The vertical alignment layer · Two populations, one firewall. Links to about, mission, two blog posts, two catalog entries. The most current description of how the suite fits together, and the only page that mentions the domain wiki.
- **tools/blackwidow-simulator.html** *Black Widow Payment Simulator* (2026-07-05). Interactive cash-trap simulator; no inbound links.
- **assets/business-card/business-card.html** Print-ready business card (2026-05-06).

---

## 4. The collections

### 4.1 The fifteen cards (cards/)

| # | Card | AI intervention(s) on the face | "What's new here" | In the 14-row matrix |
|---|---|---|---|---|
| 1 | Trust | Trusted Intermediary · Memory | yes | yes |
| 2 | Risk | Risk Insulation · Memory | | yes |
| 3 | Regulatory Friction | Risk Insulation · Input Translation | | yes |
| 4 | Geopolitical & Trade Volatility | Risk Insulation | | yes |
| 5 | Macro & FX Exposure | Risk Insulation | | yes |
| 6 | Opacity | Matching · Trusted Intermediary | yes | yes |
| 7 | Decision-Process Opacity | Trusted Intermediary · Content Match Story | yes | **no** (the one card outside the canon's fourteen) |
| 8 | Geographic Distance | Matching · Input Translation | | yes |
| 9 | Temporal Distance | Memory · Matching | yes | yes |
| 10 | Offering Complexity | Matching | | yes |
| 11 | Cold Start | Synthetic Bootstrapping | | yes |
| 12 | Cognitive Bandwidth | Matching · Input Translation | | yes |
| 13 | Fulfillment | Aggregation · Matching | yes | yes |
| 14 | Participant Fragmentation | Aggregation | yes | yes |
| 15 | Technological Obsolescence | Risk Insulation · Memory | | yes |

Source of truth: `DeeperPointComms/library/resistance-cards/content/*.yaml`; the site copy is never edited by hand. Since 2026-11-06 the cards live under What We're Building: the viewer carries the site nav with that item active, the doorway is on platform.html, and the Library no longer lists them or the deck.

### 4.2 The catalog (catalog/)

254 current entries in 29 sectors (counts from the YAML):

| Sector | n | Sector | n |
|---|---|---|---|
| canadian-financial-services | 20 | global-knowledge-equity | 10 |
| canadian-justice-system | 15 | canadian-energy | 9 |
| arts-cultural-markets | 13 | canadian-education | 9 |
| municipal-government | 13 | canadian-agriculture | 8 |
| remote-town-renewal | 13 | global-health-pharma | 8 |
| professional-services | 12 | canadian-healthcare-support | 6 |
| canadian-natural-resources | 11 | environmental-circular-economy | 6 |
| canadian-food-last-stage | 10 | social-enterprise | 6 |
| canada-mexico-trade | 10 | canadian-defence-sector | 5 |
| canadian-research-institutions | 10 | manufacturing | 5 |
| canadian-sport | 10 | pets-and-animals | 5 |
| developing-economy | 10 | senior-expert-marketplace | 5 |
| canadian-export | 10 | talent-deep-match | 5 |
| | | canadian-forestry | 4 |
| | | construction | 3 |
| | | logistics | 3 |

Twelve collection cards on the index. The count on each card is typed into the builder; three no longer match the YAML:

| Collection | Sectors | Shown | Actual |
|---|---|---|---|
| Resources & Energy | natural-resources, energy, forestry | 24 | 24 |
| Manufacturing & Build | manufacturing, construction, logistics | 11 | 11 |
| Finance & Risk | financial-services | 20 | 20 |
| Justice & Social | justice-system, social-enterprise | 21 | 21 |
| Agriculture & Food | agriculture, food-last-stage | 18 | 18 |
| Northern & Municipal | remote-town-renewal, municipal-government | 23 | **26** |
| Talent & Professional | senior-expert, talent-deep-match, professional-services | 22 | 22 |
| Healthcare & Pharma | healthcare-support, global-health-pharma | 14 | 14 |
| Arts, Sport & Education | arts, sport, education | 32 | 32 |
| Defence, Gov & Export | defence, *gov-expert-networks (retired)*, export | 25 | **15** |
| Global & Diaspora | developing-economy, knowledge-equity, canada-mexico, *diaspora-connections (retired)* | 30 | 30 |
| Research & Environment | research-institutions, circular-economy, pets-and-animals | 20 | **21** |

Orphans: 59 entry pages whose YAML no longer exists are still committed and served, and the search index covers them. They come from six retired sectors: canadian-gov-expert-networks (cgov-, 10), canadian-startup-ecosystem (cstartup-, 10), real-estate-assembly (rea-, 10), sme-service-consortium (sme-, 10), diaspora-connections (dia-, 9), ring-of-fire-hub (rof-, 9), plus one misspelled slug (dev-postharevst-cold-chain-access, superseded by dev-postharvest-cold-chain-access). `catalog_summary.json` at the root is older still (202 entries, 25 sectors) and is not read by the builder.

### 4.3 The blog (blog/)

57 Markdown posts: 51 public, 6 unlisted. Streams among the public posts: Market Scenario 22 · Workshop Notes 16 · Engineer's Log 1 · no stream 12.

**Market Scenario (22)**

| Date | Title | Slug |
|---|---|---|
| 2026-05-17 | The Machine Between Shifts (Shadow Capacity 6) | additive-manufacturing-shadow-capacity |
| 2026-05-16 | The Tensile Test That Almost Didn't Happen (SC 4) | manufacturing-scenarios-testing |
| 2026-05-12 | The Certification Bridge (SC 3) | certification-bridge-thin-market |
| 2026-04-27 | The Empty Lodge (no local HTML yet; built on deploy) | the-empty-lodge |
| 2026-04-10 | Two Lines Looking for Each Other | two-lines-looking-for-each-other |
| 2026-04-09 | The Contaminated Lot | the-contaminated-lot |
| 2026-04-08 | The Ninety-Day Map | the-ninety-day-map |
| 2026-04-08 | The Invisible Specialist | the-invisible-specialist |
| 2026-04-08 | The First Wall | the-first-wall |
| 2026-03-18 | The Machine Under the Tarp (SC 8) | used-machinery-thin-market |
| 2026-03-18 | The Welder Who Wrote Firewalls (SC 7) | manufacturing-scenarios-skills |
| 2026-03-18 | The Idle Shift (SC 5) | manufacturing-scenarios-capacity |
| 2026-03-17 | Happy St. Paddy's Day | irish-trad-thin-market |
| 2026-03-13 | Defense Innovation at the Speed of War | ukraine-defense-procurement-thin-market |
| 2026-03-12 | The Virtual Guest Lecture Dating Service | virtual-guest-lectures |
| 2026-03-12 | Drill Core and Deal Flow | junior-mining-thin-market |
| 2026-03-10 | Six Hundred Kilometres from a Family Lawyer | rural-legal-thin-market |
| 2026-03-10 | One Container of Barley | malting-barley-thin-market |
| 2026-03-10 | Tomatoes in the Sun | ethiopia-produce-thin-market |
| 2026-03-09 | The House You Can't Visit | diaspora-property-thin-market |
| 2026-03-09 | The Vase and the Rebozo | artisanal-craft-collaboration |
| 2026-03-07 | The Last Timber Framers | heritage-craft-thin-market |

**Workshop Notes (16)**

| Date | Title | Slug |
|---|---|---|
| 2026-06-06 | WooCommerce for Thin Markets | woocommerce-for-thin-markets |
| 2026-05-26 | The Regulatory Escape Hatch (SC 9) | the-regulatory-escape-hatch |
| 2026-05-20 | When Your Market Barely Exists | when-your-market-barely-exists |
| 2026-05-14 | Shadow Capacity (SC 1, pinned) | shadow-capacity |
| 2026-05-13 | The Portfolio Effect (SC 2) | portfolio-effect |
| 2026-05-11 | Why We Didn't Build a Frontend | why-we-didnt-build-a-frontend |
| 2026-04-30 | Everything Is Getting Harder to Buy | everything-is-getting-harder-to-buy |
| 2026-04-14 | The Match Argument | content-match-story |
| 2026-04-13 | Two Hundred Thin Markets | catalog-200-thin-markets |
| 2026-04-11 | The Hub Before the Road | greenstone-hub-before-the-road |
| 2026-04-06 | Why a Semantic Match Is Not Enough | why-industry-context-closes-deals |
| 2026-04-06 | How CommonContext Keeps Its Answers Relevant | commoncontext-schema-scoped-rag |
| 2026-04-05 | The Knowledge Problem at the Heart of Every Thin Market | tribal-knowledge-thin-markets |
| 2026-03-30 | The Middle Power Pivot (ebook announcement) | middle-power-pivot-ebook |
| 2026-03-23 | The Virtual Tier-One (pinned) | ontario-roadmap-part3-pocket |
| 2026-03-23 | A Cosolvent-Powered Marketplace | ontario-roadmap-part1-fractional |

**Engineer's Log (1)**: 2026-05-19 AI vs. 80 Years of Nobel Economics (ai-interventions-critique-opus).

**No stream (12, shown as "other")**: How Big Is the Thin Market Problem? (thin-market-size, 2026-03-10) · Boardy.ai and the Proof of Concept (2026-03-10) · The Thin Market Toolkit — What Cosolvent Does (cosolvent-toolkit, 2026-03-07) · Why Thin Markets Fail (2026-02-25) · Why AI Won't Take Over Work (2025-10-23) · The Market That Feeds 22 Million People a Day (2025-09-29, titled "Workshop Notes" but no stream set) · Repetition, Lean Thinking, and Thin Digital Markets (2025-08-29) · The Thick/Thin Structure of Grain Trade (2025-07-24) · Markets for Premium Grain from Western Canada (2025-07-23) · Creating Trust in Thin Markets (2025-07-20) · Pre-Technology Solutions to Thin Markets (2025-07-18) · Bulk vs Containerized Shipment (2025-07-16).

**Unlisted (6, served but not in the index)**: The Berry Syndicate (2026-06-12) · The CFIN Export Consortium · The Zero-Waste Consortium · Safely Searching the Dark (Scopri) · The Vendor Review That Almost Didn't Happen (CCN) · The Community That Could Be a Marketplace (AI4M).

**Orphan posts (22 HTML files with no Markdown source; committed, served, searchable, linked only from each other)**: the Ontario Roadmap parts 2, 4 and 5 · Inside the Firm Boundary and The Cooperative Workshop (coopspec) · The Software Stack That Surrounds a CSSS · seven flexspec posts (Italian impannatore, Magna, Not Italian It's Universal, Failure Points, Cooperation Marketplace, Ontario Manufacturing, The Pocket) · three earlier "fractional" scenarios (capacity, skills, testing: older versions of the three manufacturing scenarios above) · four middle-power posts (Dilemma, Gravity of the Center, Strategic Pivot, Thickness Without Centralization) · Thin Markets Are Why Canada Can't Diversify Its Trade (linked from mission.html) · knowledgeslot-schema-scoped-rag (redirect).

**Series pages (blog/series/)**: Shadow Capacity (current, 9 entries) and six retired landing pages with no inbound links: Fractional Manufacturing, The Ontario Roadmap, AI Powered Flexible Specialization for Ontario?, The Siren Song of Flexible Specialization, New Frontier: AI Powered Cooperative Manufacturing, B2B in a Middle Power World.

### 4.4 The twenty test beds (testbeds.html)

Cross-Border Grain Trade · Freelance Localization · Surplus Industrial Equipment · Cross-Border Telehealth · Indie Film Distribution · Specialty Timber · Biotech–CRO Matching · Artisan Food → Retail · Pro Bono Legal Matching · Community Ecotourism · Commercial Real Estate Reuse · Heritage Craft Matching · University Tech Transfer · Disaster Relief Supply · Immigrant Credentials · Short Sea Shipping · Music Sync Licensing · Community Renewable Energy · Rare Disease Patient-to-Trial · Military Tech Transfer.

The "In-Depth View" button promises each test bed in detail but opens the catalog index, which does not group them.

### 4.5 PDFs

| File | Linked from |
|---|---|
| assets/mysitedocs/MarketTheoryWP.pdf | market-physics |
| assets/mysitedocs/TheMiddlePowerPivot.pdf | ebook, precis |
| assets/mysitedocs/MarketForgeCreationGuide.pdf | marketforge |
| assets/mysitedocs/Coswebroadmap.pdf | mf-cosolvent |
| assets/mysitedocs/KSwebroadmap.pdf | mf-commoncontext |
| assets/mysitedocs/ClientSwebroadmap.pdf | mf-clientsynth |
| assets/mysitedocs/DeeperPointPlan.pdf | nothing |
| assets/mysitedocs/webforgeroadmap.pdf | nothing |
| assets/marketmaps/convoy-2023/*.pdf (4), convoy-dat/*.pdf (4) | marketmaps |
| cards/resistance-cards.pptx | platform, cards viewer |

---

## 5. Where each topic is explained

● = a section or more on the topic (four or more mentions). ○ = mentioned in passing. Counted in body text only.

| Page | Seven interventions | Match Story | Deal Brief | Cosolvent | CommonContext | ClientSynth | MarketForge | MarketMap | Sponsor model | Cold start | Middle Power / Ontario | Licence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| index | ○ | | ○ | | | | | | | ○ | | MIT |
| market-physics | ● | ● | ○ | | | | | | ○ | ● | | MIT |
| cards/ | ● | ○ | ○ | ○ | | | | | ○ | ○ | ○ | |
| intervention-matrix | ● | | | | | | | | | ○ | | |
| whitepaper | ● (eight, older names) | | | ○ | ○ | ○ | ○ | | ○ | ● | ● | |
| platform | ○ | ○ | ● | ● | ● | ● | ○ | | ● | ○ | | MIT; Apache 2.0 + one condition |
| how-it-works | | ● | ● | ○ | ○ | | | | ○ | | | |
| architecture | | ● | ● | | | | | | ● | | | |
| demo | | | | ○ | | | ○ | | | | | |
| cosolvent | ○ | | | ● | ○ | ○ | | | ○ | | | MIT; Apache 2.0 + one condition |
| mf-cosolvent | ○ | ● | ● | ● | ○ | ○ | ○ | | ● | | | MIT |
| mf-commoncontext | | ○ | | ● | ● | | ○ | | ○ | | | "Proprietary" |
| mf-clientsynth | | | | ● | | ● | ○ | | ○ | | | Apache 2.0 + one condition |
| marketforge | | | | ○ | ○ | | ○ | | ○ | | | MIT |
| catalog/ | ○ | ○ | | ● | ● | | ● | | ● | | ● | |
| library | | | | | | | | ○ | | | ○ | |
| ebook | | | | | | | | | | | ● | |
| precis | ○ | | ○ | ○ | ○ | ○ | ○ | | ○ | ○ | ● | MIT |
| pitch-deck | ○ | | ○ | ○ | ○ | ○ | ○ | | ○ | ○ | ● | MIT (all four) |
| mission | ○ | | | ○ | ○ | ○ | ○ | | ● | ○ | ○ | MIT + "proprietary layers" |
| testbeds | ○ | | | ○ | ○ | | | | ○ | | | |
| marketmaps | ○ | | | | | ● | | ● | ○ | ○ | | |
| market-diagnostic | ○ | | | | | ○ | | | | ● | | |
| about | ○ | | | ○ | | | | | | | ○ | MIT |
| contribute | ○ | ○ | ○ | ○ | ○ | ○ | | | | | | MIT; Apache 2.0 + one condition |
| guides (5) | ○ | | | ● | | ○ | | ○ | ○ | ○ | ○ | MIT |
| hackathon | | | | ● | ● | ● | ○ | | | | ○ | MIT; source-available |

Three pages define a thin market in their own words: Home ("willing buyers and sellers who cannot find each other, trust each other, or close a deal"), Market Physics ("the opposite" of a thick market), Mission ("willing buyers and willing sellers exist and a transaction would genuinely benefit both but the transaction doesn't happen"); the hackathon page has a fourth ("defined by the frictions between willing counterparties, not by how few of them there are"). The whitepaper's definition is friction, not volume.

---

## 6. Numbers and claims the site states, and where they differ

| Claim | Values on the site | Pages |
|---|---|---|
| AI interventions | seven | index, market-physics, intervention-matrix, platform |
| | eight, under different names (Input Friction Reduction, User Aggregation, AI-Driven Matching, AI as Institutional Memory, Dynamic Pricing and Valuation, Asynchronous Brokerage, Trusted Intermediation, Synthetic Market Bootstrapping) | whitepaper Part V |
| Challenges / frictions | fourteen | intervention-matrix, mission |
| | fifteen cards (fourteen plus Decision-Process Opacity) | cards, index, platform, contribute |
| | twelve | pitch-deck ("Twelve Frictions"), precis |
| | eleven | marketmaps ("11-challenge framework") |
| | nine named plus Friction Multipliers (3 existential, 6 resistance) | whitepaper Part II |
| | thirteen, with Technological Obsolescence and "Regulatory Friction (Exogenous - EMU)" | market-diagnostic |
| Catalog size | "254" | catalog index body |
| | "One hundred" | catalog index meta description |
| | "over 250" / "250+" | cosolvent, how-it-works, guide-founders, guide-investors, guide-accelerators |
| | "over 100" | testbeds, who-should-care |
| | "200" / "Two Hundred" | blog post catalog-200-thin-markets, hackathon |
| | "Hundreds … across 29 sectors" | index, library, market-physics |
| | 254 entries in 29 sectors; 313 pages on disk | actual |
| Test beds | twenty | testbeds, library |
| Evidence | eighty years, Nobel-recognised | index, market-physics, whitepaper, architecture, blog |
| Components | four: Cosolvent, CommonContext, ClientSynth, MarketForge | platform, pitch-deck, precis, whitepaper "What Comes Next" |
| | three (no MarketForge) | cosolvent |
| | four: domain wiki, CommonContext, ClientSynth, Cosolvent | hackathon |
| | "four layers", Cosolvent the open core, "upper layers proprietary" | mission |
| Cosolvent licence | MIT | everywhere it is named |
| ClientSynth licence | "Apache 2.0 with one condition" (never mixed with real participants, never presented as real, provenance marks kept); not called open source | platform, cosolvent, mf-clientsynth, contribute (since 2026-11-06; cosolvent said BUSL-1.1 and "proprietary" until then) |
| | "source-available" | hackathon; also what the LICENSE file calls itself |
| | "open-source on GitHub under the MIT licence" (all four components) | pitch-deck |
| CommonContext licence | MIT | contribute, cosolvent, platform |
| | "Proprietary" badge; "the proprietary data-refinement wing" | mf-commoncontext |
| MarketForge | a roadmap / "the sponsor's playbook" | platform, marketforge |
| | "Orchestration layer" component | pitch-deck, precis |
| | ecosystem brand ("MarketForge Ecosystem", "MarketForge ensemble") | mf-* page titles, mf-cosolvent |
| Repository | github.com/DeeperPoint/Cosolvent | contribute, mission |
| | github.com/DeeperPoint/cosolvent-beta | mf-cosolvent |
| CommonContext naming | CommonContext | all pages |
| | "Knowledge Slots" | mf-commoncontext body; KSwebroadmap.pdf filename |

---

## 7. Link integrity and reachability

**Broken links on live pages**

- The four guides (accelerators, associations, government, investors) link to `../contact/index.html`; there is no contact page.
- Blog post *Why Thin Markets Fail* links to `spoke-matching.html` and `spoke-science.html`, which do not exist.
- Blog post *The Certification Bridge* links to `commoncontext.html` at the root; the page is `mf-commoncontext.html`.
- Blog post *Shadow Capacity* links to `../portfolio-effect.html` (one level too high); *The Portfolio Effect* links to `certification-shadow.html`, which does not exist.
- The committed `blog/index.html` has six links rewritten from `-thin-markets.html` to `-market-physics.html` (woocommerce, catalog-200, creating-trust, pre-technology-solutions, repetition-lean-thinking, tribal-knowledge). The Markdown sources are correct, so the deploy rebuild overwrites the file; the error came from a blanket rename of `thin-markets.html` applied to the generated index.

**Links that work only because the site sits at the domain root**

- Every catalog entry page uses `../../` for the root (styles.css, index, market-physics, marketforge, blog links); from `catalog/<slug>.html` that is one level too high. Browsers clamp at the root, so the live site is unaffected; a local preview from a subfolder breaks.
- guide-founders.html links to `../catalog/index.html` from the root.

**Reachability**

- Only one body link reaches architecture.html (from platform), testbeds.html (from library) and market-diagnostic.html (from library).
- The fifteen standalone card pages (cards/<slug>.html) are reached only through the viewer, whose Open card alone and PNG links are rewritten by script for the card on stage; in the static HTML only Trust's are present. Nothing else on the site links them since Home and Market Physics switched to viewer deep links (2026-11-06).
- who-should-care.html is hidden from nav and search, but 20 blog posts still call it ("Who should build this? →").
- mission.html links to the orphan post *Thin Markets Are Why Canada Can't Diversify Its Trade*, which has no Markdown source and survives only because the HTML is committed.
- The search index (Pagefind) is built over every HTML file deployed, so the 59 orphan catalog pages, the 22 orphan posts and the 6 retired series pages all appear in search results. Pages carrying a noindex meta (the hackathon page, Who It's For, the guides and the redirect stubs) are the only ones it skips.

**Footer variants** (five different footers are in use)

| Footer links | Pages |
|---|---|
| Home · Search · Contribute · GitHub | 20 pages, including the blog index, the hidden pages and, since 2026-11-06, the cards viewer |
| Home · Search · About · Contribute · GitHub | index, how-it-works, ebook, precis, marketmaps, search |
| Home · Search · Platform · Contribute · GitHub | architecture |
| Home · Search · Cosolvent Suite | mf-cosolvent, mf-commoncontext, mf-clientsynth |
| none | catalog index and entries, demo, pitch-deck, hackathon, redirects, the 15 standalone cards (their only footer is the card face's matrix link) |

---

## 8. Candidate overlaps, duplications and breaks

Noticed while building the map. Each is a candidate, not a verdict.

**Overlaps (the same thing told in more than one place)**

1. **The Content Match Story → Deal Brief progression** is told at length four times: market-physics ("Where the Interventions Become Visible"), how-it-works (the whole page), mf-cosolvent (two sections), platform ("How a Deal Forms", "The Deal Brief"). The blog post *The Match Argument* is a fifth.
2. **The component roster** is listed on nine pages with three different rosters (section 6). platform.html and cosolvent.html do the same job: roster, licence, customization boundary. cosolvent.html is the hub the three mf-* pages return to ("Back to Ecosystem", footer), while the nav sends visitors to platform.html. Two hubs for one question. ClientSynth is now treated the same on both (2026-11-06), which removes one difference between them, not the duplication.
3. **How a vertical is built** is described three ways: architecture.html (four diagrams), marketforge.html (five phases, twelve steps, digital twin, curation loops) and mf-commoncontext.html (How It Integrates). The hackathon page is a fourth and the most current, but unlinked.
4. **The Middle Power Pivot material** exists as the ebook, précis and pitch deck; as whitepaper Part X; as guide-government; and as 22 orphan posts and 6 retired series pages on flexible specialization, the Ontario roadmap and Middle Power strategy that are still served and searchable.
5. **Test beds, catalog and scenario stories** are three samplings of the same idea at three dates (20 → 254 → 22 stories). testbeds.html predates the catalog, counts it as "over 100", and its "In-Depth View" button leads to the catalog index.
6. **Catalog size** is stated six ways (section 6).
7. **Guides and catalog**: the five guides pitch the catalog as "250+ pre-validated thin markets" and Cosolvent as the engine; the owner already judged Who It's For duplicative of the catalog and hid it. Twenty blog posts still send readers there.

**Contradictions**

8. **Licensing** was inconsistent across the site. Since 2026-11-06 platform, cosolvent, contribute and mf-clientsynth agree: Cosolvent and CommonContext MIT, ClientSynth "Apache 2.0 with one condition". Still differing: mf-commoncontext.html ("Proprietary" badge, "the proprietary data-refinement wing"), pitch-deck.html (all four components MIT), mission.html ("the upper layers are proprietary"), and the hackathon page ("source-available", which is what the LICENSE file calls itself but not what the site now says).
9. **Challenge taxonomy** differs between the whitepaper (nine plus multipliers), the diagnostic (thirteen), the matrix (fourteen), the cards (fifteen), the précis and deck (twelve) and MarketMaps (eleven). The whitepaper is offered as "the full version" of the argument but uses the oldest taxonomy and eight interventions under names the rest of the site no longer uses.
10. **MarketForge** is a roadmap on platform.html and marketforge.html, an "orchestration layer" component in the deck and précis, and an ecosystem brand in the mf-* page titles.
11. **Repository** names differ: DeeperPoint/Cosolvent (contribute, mission) and DeeperPoint/cosolvent-beta (mf-cosolvent).

**Breaks in flow**

12. **Why Markets Don't Form → What We're Building** has two bridges: market-physics ends with "Continue →" to platform, and its closing tiles send readers to the matrix, whitepaper and catalog first. The whitepaper's own exit is "Back to Summary" (market-physics) and the catalog, not the platform.
13. **The mf-* pages** are a self-contained loop (cosolvent.html ↔ mf-*) with their own footer and "MarketForge Ecosystem" branding; nothing on them leads to How It Works, the demo or Contribute.
14. **market-diagnostic** and **testbeds** are reachable from the Library only; the diagnostic's exit is "Explore Building Tools" to cosolvent.html rather than platform.
15. **mission.html** (March 2026) is the fullest statement of the sponsor model and of why the engine is open, but it describes a four-layer stack with proprietary upper layers that platform.html no longer claims. It is linked from About and the Library.
16. **The blog** shows 12 of 51 public posts as "other" because they carry no stream, including one titled "Workshop Notes".
17. **The hackathon page** is the only place the domain wiki is named and the clearest statement of the real/synthetic firewall; it is unlinked and noindexed.
18. **Two unlinked PDFs** (DeeperPointPlan.pdf, webforgeroadmap.pdf) and the Black Widow simulator are deployed with no page pointing at them.

**Resolved between the two snapshots (2026-11-06)**

- The cards were listed in three places (Home strip, Market Physics block, two Library tiles) with no single home. They now have one, under What We're Building; Home's strip and two one-line cross-references point at it.
- ClientSynth was told three times on platform.html (an exception clause in the licence paragraph, a tile labelled differently from its peers, a full block at the foot of the page) and sat in a separate "proprietary" section on cosolvent.html. It is now one tile among peers on both pages.
- cosolvent.html's BUSL-1.1 label and "proprietary simulation engine" wording, and a stale "(Formerly CommonContext)" note on its CommonContext card.
- Direct links to the standalone card pages on Home and Market Physics became viewer deep links, so the standalone pages are now viewer-only (section 7).
