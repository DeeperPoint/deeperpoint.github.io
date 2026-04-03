<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->
---
title: "Market Scenario: Three Shops and a Platform"
date: 2026-04-03
slug: three-shops-platform
stream: market-scenario
tags: [thin-markets, ai, market-design, case-study, scenario, cosolvent, marketforge, manufacturing, canada]
summary: How three non-competing Canadian integrators could pool their expertise to harden an open-source marketplace platform — then offer it to manufacturer communities as the infrastructure none of them could have built alone.
estimated-read: 16 min read
unlisted: true
---

<figure class="blog-hero">
  <img class="blog-hero__img" src="../images/blog/three-shops-platform-hero.png" alt="Three integrators, three specializations, one platform." loading="lazy">
  <figcaption>Three integrators, three specializations, one platform.</figcaption>
</figure>

## The Problem With Doing Everything Alone

The Canadian manufacturing ecosystem has no shortage of companies trying to help. AI integrators. Automation houses. Digital supply chain platforms. Smart manufacturing consultants. Each one knows its domain deeply, serves its clients well, and struggles with the same limitation: every engagement is custom, every client relationship is bilateral, and the knowledge gained in one project stays locked inside that project.

What if three integrators — each with a different, non-competing specialization — decided not to compete for the same market, but to build the market together?

This isn't a merger fantasy. It's a structural observation about how [thin markets](../thin-markets.html) work. When the supply side is fragmented into specialists who each solve one piece of a manufacturer's puzzle, the manufacturers can't efficiently assemble the right combination. The specialists, meanwhile, can see that their clients need capabilities beyond what any single firm provides — but they have no mechanism to coordinate, refer, or co-deliver without ad hoc phone calls and personal favours.

The platform that connects these specialists to each other — and then connects all of them to the manufacturing communities that need the combined offering — is the missing infrastructure. And the firms best positioned to build it are the ones who already understand the problem from the inside.

*(Note: The following scenario is fictional, designed to illustrate how a consortium of integrators could develop and deploy a community marketplace for the Canadian manufacturing sector. Three real companies — [Evormore](https://evormore.ai), [The Assembly](https://theassemblystudio.com), and [EVM Group](https://evmgrp.com) — serve as inspiration for the specialized capabilities described. The specific characters, events, and platform interactions are invented. None of these companies has committed to or endorsed this scenario.)*

---

## The Story: Three Shops and a Platform

### The Three

They didn't all meet at the same moment. It started with separate conversations at the N3 Summit — Canada's national advanced manufacturing conference — in the spring of 2025. Vic Uzumeri, the researcher behind DeeperPoint's open-source Cosolvent architecture, walked the exhibition floor and stopped at three booths. At each one, he described the same idea: a semantic matching engine for manufacturing communities, open-source, designed to connect participants with complementary needs through AI-mediated introductions and structured trust-building. At each booth, the founder listened, asked sharp questions, and said some version of the same thing: "That's interesting. Tell me more."

**Brock Rowlands** ran a seven-person AI integration firm out of London, Ontario. His company deployed sovereign, open-source AI infrastructure for small manufacturers — private AI assistants built on Open WebUI, workflow automation with n8n, CRM systems that clients owned outright. No vendor lock-in. No per-seat fees. The value proposition was simple: your data stays on Canadian servers, and everything we build belongs to you. Sixty-day experiments to prove the value before scaling. He'd done forty-plus engagements across southwestern Ontario — CNC shops, food processors, greenhouse operations, packaging lines.

**Dustin Sparks** ran a digital supply chain platform from Charlottetown, Prince Edward Island, with a production network that spanned the country. His company converted physical inventory into digital files and routed on-demand manufacturing to vetted Canadian producers. The core innovation was a smart routing engine that matched parts to the optimal producer based on capability, capacity, location, and cost — eliminating the warehouse, the carrying costs, and the twelve-week lead times. He worked with equipment suppliers, marine distributors, HVAC manufacturers, aerospace parts companies. His platform already did a form of semantic matching, though he didn't call it that.

**Adam McCormick** ran a forty-person industrial automation house based in Hamilton, Ontario. His company designed and installed complete automation systems — robotic cells, conveyor lines, SCADA and MES implementations, custom control panels, electrical and mechanical installations. Five hundred projects completed, two hundred systems integrated, a licensed electrical contractor with a 20,000-square-foot facility. When a manufacturer needed physical infrastructure modernized — not just AI configured, not just parts sourced, but actual machines designed, built, wired, and commissioned — Adam's team did the work.

Brock and Dustin found each other at the conference and had a long conversation — two founders solving adjacent problems who recognized, almost immediately, that their capabilities were complementary rather than competitive. When Vic mentioned EVM Group to both of them separately, their ears perked up. They knew of the Hamilton automation house by reputation. The three-way connection hadn't been made yet, but the ingredients were on the table.

What happened next — in this scenario, at least — is that Vic made the introduction, and the three founders discovered what thin market theory would have predicted: their capabilities interlocked almost perfectly, with virtually zero overlap.

### The Collaboration

They didn't form a company. They formed a working group.

Over the next four months, meeting biweekly on video calls and twice in person (once in Hamilton, once in London), the three firms contributed development time to hardening the open-source [Cosolvent](../marketforge.html) codebase for manufacturing use. Each brought a different perspective:

**Brock's team** handled the AI layer. They configured the semantic matching engine to understand manufacturing vocabulary — process types, material categories, equipment specifications, certification standards. They built the conversational profile intake system, where a manufacturer could describe their situation in plain language and the AI would extract structured attributes. They deployed the platform on sovereign Canadian infrastructure using the same open-source stack they configured for clients: self-hosted, no vendor dependencies.

**Dustin's team** contributed the production-matching logic. They'd already built a routing engine that matched parts to producers based on capability, capacity, and location. Adapting that logic for a broader manufacturing services marketplace — where the "part" might be a consulting engagement, a training program, surplus equipment, or a subcontracting opportunity — was an extension, not a reinvention. They also contributed the IP protection architecture: encrypted file handling, controlled access, Canadian data residency.

**Adam's team** grounded the platform in physical reality. They defined the equipment taxonomy — how to describe automation systems, control architectures, installation requirements, and safety certifications in structured terms that the matching engine could understand. They stress-tested the matching engine against real scenarios from their project history: could it match a manufacturer who needed "a robotic palletizing cell for case-packed dairy products" with an integrator who'd built exactly that?

By month five, they had something that worked. Not a product — a prototype. A Cosolvent instance configured for Canadian manufacturing, running on Canadian infrastructure, with a semantic vocabulary that understood the difference between a CNC lathe and a CNC mill, between MES and SCADA, between a 60-day AI experiment and a full system integration.

### The Pitch

The question was: who sponsors the marketplace?

In thin market theory, the sponsor is the entity with the convening authority and the membership trust to get participants through the door. For Canadian manufacturing, the obvious candidates were the industry associations — organizations that already had the members, the governance structures, and the mandate to serve their communities.

The trio approached three: Canadian Manufacturers & Exporters (CME), which represented 2,500+ manufacturers nationally with Peer Councils already facilitating knowledge exchange. Excellence in Manufacturing Consortium (EMC), a not-for-profit focused on Ontario manufacturers. And the Canadian Advanced Manufacturing Alliance, a newer coalition linking regional manufacturing clusters.

The pitch wasn't "buy our software." It was: "Your members already have these problems. We've built a tool that solves them. Let's test it."

They presented three scenarios drawn from their combined client experience:

**Scenario A — Equipment matching.** Adam's team had a client in Brantford with a surplus robotic welding cell — fully commissioned, barely used, sitting idle after a contract cancellation. Brock's team had a client in Guelph who needed exactly that capability but couldn't afford a new system. In a community marketplace, the matching engine would have connected them in hours. In reality, neither knew the other existed.

**Scenario B — Capability sourcing.** Dustin's platform regularly received requests from manufacturers who needed parts produced in specific processes or materials that none of his current network producers offered. In a broader community marketplace, those requests could be matched against the capability profiles of manufacturers who weren't part of Dustin's network but were members of the same industry association.

**Scenario C — Integration referral.** Brock's team regularly identified automation needs during AI deployments that required physical installation work. He knew Adam's team could do it, but his clients in Kitchener and Stratford didn't know Adam existed. Meanwhile, Adam's clients in Hamilton and Niagara frequently needed the AI configuration and data layer that Brock's team provided. The referrals happened informally; the marketplace would make them systematic.

CME's Ontario chapter was the first to say yes. They'd run it as a pilot with 150 volunteer members from their southwestern Ontario Peer Council network.

### The Specializations

As the pilot took shape, something interesting happened. Each of the three firms discovered that the community marketplace wasn't cannibalizing their existing business — it was clarifying it.

**Brock's firm** became the community's **AI and data layer specialist.** When a manufacturer joined the platform and needed help setting up their profile, configuring their semantic search parameters, or deploying a local AI assistant that could interact with the community knowledge base — that was Brock's team. He offered a "Community Onboarding" package: a four-week engagement that got a new manufacturer onto the platform with a properly configured AI environment, a structured profile, and a trained team. Revenue per engagement: $8,000–$15,000.

**Dustin's firm** became the community's **digital supply chain and production routing service.** When the matching engine identified that a manufacturer had surplus inventory, needed on-demand parts, or wanted to digitize their physical stock into a shared catalogue — that was Dustin's domain. He offered a "Digital Inventory Conversion" service: scanning, digitizing, and making a member's parts available for on-demand production through the vetted Canadian network. He also ran the IP protection layer that ensured design files stayed sovereign and encrypted during any transaction. Revenue model: per-conversion fee plus a percentage of successful production transactions.

**Adam's firm** became the community's **physical installation and automation partner.** When the matching engine identified that a manufacturer needed equipment installed, a production line upgraded, a control system modernized, or a safety compliance review — that was Adam's team. The difference was that Adam was no longer cold-calling or waiting for RFPs. The platform was generating qualified, contextualized leads from manufacturers whose needs had already been semantically profiled. Revenue model: standard project-based engineering fees, but with dramatically reduced business development costs.

The three firms' offerings were architecturally non-competitive:

| Layer | Firm | What They Provide | What They Don't Do |
|---|---|---|---|
| **Data & AI** | Brock (London) | AI deployment, profile configuration, semantic search, data sovereignty | Physical installation, parts production |
| **Supply Chain** | Dustin (Charlottetown) | Digital inventory, production routing, IP protection, on-demand manufacturing | AI configuration, equipment installation |
| **Physical Systems** | Adam (Hamilton) | Automation, controls, electrical/mechanical installation, SCADA/MES | AI deployment, supply chain routing |

When a manufacturer needed capabilities from two or all three layers — which happened more often than anyone predicted — the trio could assemble a combined engagement. A food processor in Stratford who needed a robotic packaging cell (Adam), AI-driven quality inspection (Brock), and on-demand spare parts for the new line (Dustin) got a coordinated proposal from all three firms, with the community platform handling the matching, scoping, and introduction.

### Six Months In

The CME pilot grew from 150 to 340 members. Two additional chapters — Northern Ontario and the Prairies — requested access. The matching engine had facilitated 67 peer connections, 23 equipment transactions, 14 service engagements, and 8 combined multi-firm projects.

The three firms hadn't merged. They hadn't created a joint venture. They'd done something more durable: they'd built the connective tissue of a community marketplace, offered their specialized services through it, and demonstrated that the platform's value to manufacturers increased with every new member — including the members who never hired any of the three firms directly.

Adam put it most concisely at a review meeting: "We didn't build a company. We built a neighbourhood. We happen to be the plumber, the electrician, and the architect. But the neighbourhood isn't ours — it's theirs."

Two of the three — Brock and Adam — signed on to provide ongoing community support to the CME platform: member onboarding, technical maintenance, quarterly profile refreshes, and matching engine tuning. The support contract covered their operational costs and gave them persistent visibility within the community they'd helped build. Dustin's production routing operated as a service layer accessible to all members, generating transaction-based revenue without requiring a support contract.

---

*(End of fictional scenario.)*

---

## How This Could Actually Happen — Timing and Phases

The story above compresses what would realistically unfold over twelve to eighteen months into a single narrative arc. In practice, there are four distinct phases — each with a different level of commitment, risk, and cost. Nobody has to bet the company. Nobody has to quit their day job.

**Phase 1 — Chat (Months 1–3).** The trio engages with DeeperPoint to periodically discuss the design and progress of Cosolvent and the other [MarketForge](../marketforge.html) components. Monthly video calls, shared Slack channel, maybe a site visit. Nobody invests more than a few hours per month. Vic Uzumeri continues to fund core development out of personal resources, which means progress is steady but unhurried — the burn rate of a self-funded researcher, not a venture-backed startup. The trio's role in this phase is advisory: they provide domain expertise, test assumptions, and flag requirements that only people who've deployed real systems in real factories would know. Cost to each firm: essentially zero beyond the principals' time.

**Phase 2 — Engagement (Months 3–8).** One, two, or all three of the trio identify specific areas where they can contribute to making Cosolvent production-ready faster, or to expanding its capabilities into areas their clients need. They actively participate in the open-source project — contributing a modest but steady stream of pull requests. Brock's team might build the manufacturing-vocabulary layer for the semantic engine. Dustin's team might adapt their production-routing logic as a Cosolvent plugin. Adam's team might define the equipment taxonomy and stress-test the matching against their project history. The contributions are real but manageable — a developer here, a domain expert there, integrated into existing workloads. The open-source model means every contribution benefits all participants, including DeeperPoint. Cost to each firm: one to two developer-days per week, absorbed into existing capacity.

**Phase 3 — Sell and Integrate (Months 8–14).** One or two of the trio find a legitimate prospect — a manufacturer, an industry association chapter, or a regional consortium — that wants to build a pilot system and is willing to provide seed funding. The funding isn't enough to generate profit, but it covers the direct costs of bringing the system to life: hosting infrastructure, configuration, testing, member onboarding, and a few months of operational support. Some of these funds are spent with DeeperPoint's experienced development team in Addis Ababa, where senior developers cost less than US$20/hour — making the seed funding stretch further than it would with a North American-only team. The pilot has a defined scope (e.g., 50–150 members from one CME chapter), a clear success metric (e.g., 20 matches facilitated in 90 days), and an exit condition if it doesn't work. Cost to each participating firm: partially covered by the seed funding, with some in-kind contribution of integration time.

**Phase 4 — Expand (Month 14+).** After the pilot succeeds — and "success" means members are using it unprompted, not just that the software runs — each of the three firms begins to use the platform to expand their core mission. Brock offers Community Onboarding packages to new members. Dustin lists his Digital Inventory Conversion service. Adam's automation practice starts receiving contextualized leads instead of cold inquiries. The platform begins to generate its own demand, and the trio's first-mover advantage compounds with every new member added.

**Somewhere in this timeline, DeeperPoint itself would need to grow up.** Today it's a one-person, self-funded research project — Vic Uzumeri writing code, funding a small development team, and publishing the open-source codebase because he believes the architecture is sound and the problem is real. That's fine for Phase 1 and adequate for Phase 2. But by the time real clients are running pilot systems and real companies are building services on top of the platform, a vanity project isn't a credible foundation.

The natural transition is from solo project to **non-profit open-source development organization** — a governance structure that gives contributing companies a voice in the roadmap, protects the open-source license from capture, and provides the institutional continuity that clients and sponsors need to trust the platform long-term. Think Apache Software Foundation or Eclipse Foundation, but smaller and purpose-built for thin market infrastructure.

Any or all of the three companies might choose to assume founding roles in that transition — seats on a technical steering committee, influence over the development roadmap, recognition as charter contributors. Or they might prefer to remain service providers who build on top of the platform without taking governance responsibility. Either position is legitimate. The point is that the option exists, and the transition from "Vic's project" to "the community's infrastructure" is a feature of the model, not a bug. The platform's credibility — and the trio's first-mover advantage within it — is stronger when the underlying technology is governed by an organization that no single party controls.

The critical feature of this timeline is that **nobody has to over-commit early.** Phase 1 costs nothing but attention. Phase 2 costs modest developer time. Phase 3 is the first real expenditure, and it's partially funded by the client. Phase 4 is where the return begins — but by then, the risk has been validated by real data from the pilot.

---

## The Structural Logic

This scenario illustrates a pattern that [thin market theory](../thin-markets.html) predicts but that most industry players don't recognize: **the firms closest to the thin market problem are the ones best positioned to solve it — but only if they collaborate rather than compete.**

A single integrator building a community marketplace for their own clients (as explored in [The Integrator Who Built a Network](../evormore-network.html)) creates a valuable but bounded network. Three non-competing specialists doing it together create something qualitatively different: a platform where every capability gap identified by the matching engine has a resident expert ready to fill it.

The key structural features:

- **Non-competitive specialization** means the firms can share a platform without cannibalizing each other. Each new member is a potential client for all three, but in different ways.
- **Community sponsorship** (through the industry association) provides the trust infrastructure and convening authority that no individual firm could achieve alone.
- **First-mover advantage** is collective. A competing trio would need to replicate not just the technology but the combined domain knowledge, client relationships, and community trust that these three firms built together.
- **The platform belongs to the community**, not to the firms — but the firms that built it have structural advantages within it that persist as long as they continue to serve the community well.

The technology foundation — the open-source [Cosolvent](../marketforge.html) matching architecture — is designed for exactly this pattern: multi-stakeholder communities where participants have diverse, complementary capabilities and the matching engine's job is to discover combinations that no single participant could have found alone.

---

*This document was prepared by [DeeperPoint](https://deeperpoint.com) as a discussion starter. The scenario is fictional; the companies mentioned — [Evormore](https://evormore.ai), [The Assembly](https://theassemblystudio.com), and [EVM Group](https://evmgrp.com) — are real, but the specific events, characters, and collaborations described are invented. Cosolvent is open-source software under active development. DeeperPoint is not affiliated with any of the companies mentioned. We welcome questions and collaboration — [deeperpoint.com](https://deeperpoint.com).*
