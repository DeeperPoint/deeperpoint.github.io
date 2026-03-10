<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->

---
title: "Boardy.ai and the Proof of Concept for Thin Market Engineering"
slug: boardy-proof-of-concept
date: 2026-03-10
tags: [thin-markets, market-design, ai, explainer, marketforge, cosolvent, knowledgeslot]
summary: "Boardy.ai is an AI superconnector that matches founders to investors through voice conversations. Whether its team knows it or not, Boardy has built a working implementation of several core thin market engineering principles. If it can thicken the market for startup capital, the framework works everywhere."
estimated-read: 12 min read
---

<figure class="blog-hero">
  <img class="blog-hero__img" src="../images/blog/boardy-deeperpoint-hero.jpg" alt="Two approaches to the same problem — thickening markets that should work but don't." loading="lazy">
  <figcaption>Two approaches to the same problem — thickening markets that should work but don't.</figcaption>
</figure>

## A Box-Headed AI Is Validating the Framework

In early 2025, a Toronto-based startup called Boardy.ai raised $8 million in seed funding. The story made headlines not for the amount but for the claim that Boardy — the AI agent itself, personified with a cardboard-box head — had orchestrated much of the fundraise, engaging directly with potential investors through voice conversations.

That detail is interesting but peripheral. What matters is what Boardy actually *does*: it calls you on the phone, interviews you about your work and what you need, builds a profile from the conversation, and then matches you to other people in its network through double-opt-in email introductions. No app. No forms. No LinkedIn-style profile page. Just a voice conversation, an AI that remembers what you said, and introductions that both parties have to accept before either sees the other.

I have no relationship with Boardy and no inside knowledge of how it works. But from the outside, watching it operate, I see something that the DeeperPoint framework would recognize immediately: **Boardy is a thin market engineering tool that has independently converged on several of the core principles we've been developing.**

This is not a competitor analysis. DeeperPoint is not competing with Boardy — we are not competing with anyone. The thin market opportunity is measured in [trillions of dollars of missing commerce](thin-market-size.html), and fighting over niches would be absurd. What Boardy represents is something more valuable than a rival: **a proof of concept.** If a voice-first AI agent can thicken the notoriously thin market of founders and funders, the underlying principles work. And if they work there, they work everywhere.

---

## Where Boardy and DeeperPoint Converge

The convergence is striking — not because Boardy was built from DeeperPoint's whitepaper (it wasn't), but because the same structural problems produce the same engineering solutions when people think clearly about them.

### 1. Voice-First, Form-Free Onboarding

**Boardy's approach:** You give Boardy your phone number. It calls you. You talk. The AI extracts structured data from the conversation — your goals, your expertise, what kind of connections you're looking for. No forms, no dropdowns, no "select your industry" menus.

**DeeperPoint's principle:** The whitepaper calls this *multimodal input translation* and *natural language onboarding*. The framework explicitly identifies the "digital literacy barrier" as a force that excludes participants from markets — and proposes voice and natural language as the solution:

> *"Instead of forms, users have conversations. A farmer in rural India can call a phone number and speak in their local language... AI extracts quantity, product type, quality indicators, harvest timing, and location — then generates a marketplace listing."*

Boardy does exactly this, in a different vertical. A founder describes their company, stage, traction, and needs. The AI extracts it into a matchable profile. The parallel is precise.

**What Boardy validates:** Voice onboarding is not a theoretical convenience — it is a structural necessity for thin markets where participants either cannot or will not fill out forms. Founders don't want to write LinkedIn profiles that double as investor pitches. Farmers don't want to fill out commodity specification forms. Voice lets the AI do the structuring while the human does the talking.

---

### 2. Semantic Matching, Not Keyword Search

**Boardy's approach:** When Boardy identifies a match, it is not because both parties used the same keywords. It is because the AI evaluated the *semantic overlap* between what one person needs and what another person offers. A founder building a fintech in Nairobi doesn't search for "East African fintech investor" — Boardy understands from the conversation that the founder needs growth-stage capital, has traction in mobile payments, and would benefit from an investor who understands emerging market financial infrastructure.

**DeeperPoint's principle:** The whitepaper's matching architecture is built on *vector embeddings* — mapping every participant to a point in high-dimensional semantic space and measuring proximity. The framework explicitly contrasts this with keyword search:

> *"Traditional search requires buyers to know the right keywords. AI understands what they mean even with imperfect queries."*

Boardy appears to be doing exactly this. Users don't search — they talk, and the AI identifies matches they could never have specified in a search query.

**What Boardy validates:** Semantic matching is not an academic concept. It produces real introductions between real people who would never have found each other through directories, events, or LinkedIn. When a Boardy user gets an introduction to someone they didn't know existed, that is a thin market transaction that was *created* by the matching infrastructure.

---

### 3. Double-Opt-In Progressive Disclosure

**Boardy's approach:** When Boardy identifies a potential match, it contacts both parties separately, describes the match rationale, and asks each whether they want to proceed. Only if *both* say yes does Boardy make the email introduction. Neither party's details are shared until mutual consent.

**DeeperPoint's principle:** The whitepaper calls this the *Trusted Intermediary Protocol* — the AI learns sensitive information from both sides under confidentiality and facilitates introductions "only when appropriate," without requiring mutual disclosure until both parties have opted in. The *Trust Gradient* model explicitly stages disclosure:

> *Browsing → Profile creation → Sharing sensitive data → Initiating contact → Negotiating terms → Committing funds*

Boardy implements the first three stages of this gradient. The user shares sensitive information (goals, vulnerabilities, what they need) with the AI under implicit confidentiality. The AI evaluates fit without exposing either party. Disclosure happens only at mutual opt-in.

**What Boardy validates:** People will share sensitive strategic information with an AI intermediary that they would never broadcast publicly. Founders tell Boardy things about their runway, pivots, and weaknesses that they would never post on Twitter. This validates the entire premise of trusted intermediation — the AI as confidential broker.

---

### 4. The AI as Persistent Memory

**Boardy's approach:** Boardy remembers your previous conversations. If you call back weeks later with updated goals, it adjusts your profile and matching criteria. The AI maintains a persistent model of who you are and what you need, evolving over time.

**DeeperPoint's principle:** The whitepaper identifies *memory* as one of the most fragile and valuable assets in thin markets, and proposes AI-based institutional memory as the solution:

> *"Traditional marketplaces suffer from 'amnesia.' Every interaction requires users to re-explain preferences, re-verify credentials, and re-establish intent. AI transforms memory from a fragile, person-dependent asset into a persistent, scalable matching advantage."*

The whitepaper explicitly describes *anticipatory matching* — where the AI recognizes evolving patterns in a user's needs and proactively surfaces matches before the user searches.

**What Boardy validates:** Memory-driven matching works in practice. A founder who talked to Boardy three months ago about needing a CTO now gets proactively matched to a technical co-founder who just entered the network. The system gets smarter over time, which is exactly what thin markets need — markets that *learn*.

---

### 5. Proactive Outreach, Not Passive Discovery

**Boardy's approach:** Boardy doesn't wait for users to search. When a new person enters the network and matches an existing user's needs, Boardy initiates the introduction proactively. The AI is an active matchmaker, not a search engine.

**DeeperPoint's principle:** The whitepaper describes *asynchronous brokerage agents* — AI that "actively engages with buyers who just arrived" and can "hold real conversations, answer questions, negotiate within parameters." The Cosolvent roadmap includes *proactive matching notifications* and *outreach generation* as core features.

**What Boardy validates:** Passive marketplaces — where users search through listings — are the wrong model for thin markets. In a thin market, neither party knows what to search for, and the listing they need may not exist yet. Proactive, AI-initiated matching is the viable architecture.

---

## Where They Diverge

The convergences are remarkable. The divergences are equally instructive — and they map precisely to the complexity of the markets each system is designed to serve.

### Boardy Is Single-Vertical; DeeperPoint Is a Framework

Boardy operates in one vertical: professional networking, with a heavy emphasis on founders and investors. Its Knowledge Slot equivalent is the AI's accumulated understanding of the startup ecosystem — who are credible investors, what stage-appropriate introductions look like, what founders need at seed versus Series A.

DeeperPoint's architecture is designed to be *vertical-agnostic*. The Cosolvent framework, the Knowledge Slot, and the YAML-driven marketplace configuration are designed so that a sponsor — a trade association, a government agency, a regulatory body — can deploy a matching platform for *any* thin market: [specialty grain](malting-barley-thin-market.html), [rural legal services](rural-legal-thin-market.html), [heritage crafts](heritage-craft-thin-market.html), or [developing-world produce distribution](ethiopia-produce-thin-market.html).

This is not a criticism of Boardy — single-vertical focus is a perfectly legitimate strategy, especially at seed stage. But it does mean Boardy's proof of concept applies to the *principles* of thin market engineering, not to the *framework generalization* problem that DeeperPoint is solving.

### Boardy Has No Visible Sponsor Model

Boardy is a commercial product. It is its own sponsor, curator, and platform operator. It collects information, curates matches, and monetizes the network directly.

DeeperPoint's architecture explicitly separates the *platform* (matching infrastructure), the *sponsor* (the institution that configures, curates, and governs), and the *Knowledge Slot* (the domain-specific reference library). This three-layer separation is what allows the same framework to serve a Law Society matching rural clients to urban lawyers, an African agricultural cooperative connecting smallholders to cold chain logistics, or a trade ministry linking manufacturers to export markets.

Boardy's commercial model works for the startup ecosystem because the ecosystem is self-selecting and relatively homogeneous. Founders and investors share vocabulary, incentives, and cultural norms. In more complex verticals — where participants speak different languages, operate under different regulatory regimes, and have fundamentally different levels of digital literacy — the sponsor model is essential.

### Boardy Stops at the Introduction; DeeperPoint Builds to the Deal

Boardy's output is an email introduction. What happens next — the pitch, the due diligence, the term sheet — is up to the humans. Boardy is a top-of-funnel tool.

DeeperPoint's architecture extends much further: from initial matching through *deal structuring* (assembling the multilateral participants — logistics providers, quality inspectors, trade finance — needed for complex transactions), *dynamic pricing* (fair-value estimation from comparable transactions), and the *Handoff Artifact* (a structured output that captures the full deal context and hands it off to human execution). This difference reflects the complexity of the markets DeeperPoint targets. An introduction is enough when a founder and an investor share a coffee. It is not enough when a grain farmer in Saskatchewan, a craft brewery in the Philippines, a shipping company in Vancouver, and a customs broker in Manila need to coordinate a specialty barley shipment.

### Boardy Has No Knowledge Slot

When a founder talks to Boardy, the AI draws on its general training and its accumulated network intelligence. There is no visible curated reference library — no equivalent of a sponsor loading the system with "here are the regulations for cross-border grain trade" or "here are the Law Society's cost guidelines for family law."

For professional networking, this works. The domain knowledge is general enough that a well-trained LLM can handle it. But for vertical-specific thin markets — where a participant might ask "can a lawyer from Ottawa represent me in Cochrane?" or "what moisture level is acceptable for Grade 1 Canada Western Red Spring?" — general AI knowledge is insufficient. The Knowledge Slot exists because thin markets have *domain-specific* information that must be curated by someone embedded in that domain.

---

## What Boardy's Existence Proves

Here is the argument, distilled:

**The founder-investor market is a thin market.** There are vastly more founders than there are suitable investors for any given company. Discovery is terrible — founders cold-email hundreds of investors; investors wade through thousands of decks. Information asymmetry is severe — founders exaggerate traction; investors hide their investment thesis. Trust is hard to establish — everyone claims to be "founder-friendly." Geographic dispersion fragments the market further — a founder in Lagos and an investor in Berlin might be a perfect match but will never meet at a Bay Area demo day.

**Boardy addresses this with thin market engineering tools.** Voice onboarding, semantic matching, progressive disclosure, persistent memory, proactive outreach. These are not "networking features." They are the same tools that the DeeperPoint whitepaper derives from first principles as the necessary interventions for any thin market.

**Boardy works.** It raised $11 million. It has thousands of users. It produces introductions that lead to real meetings, real investments, real hires. The tools produce results.

**Therefore the tools work.** Not just in theory, not just in a whitepaper, but in a funded, operational, growing application.

**And if they work for founders and investors — one of the most culturally homogeneous, English-speaking, digitally literate thin markets on earth — they certainly work for the harder cases.** For the Ethiopian farmer who speaks Amharic and has a feature phone. For the Ontario widow who needs a family lawyer with agricultural expertise. For the heritage timber framer in rural Quebec who has never heard of Cosolvent.

The thin market opportunity is not small enough to fight over. Boardy has demonstrated that the core principles are sound. DeeperPoint's contribution is the framework that generalizes those principles to *every* thin market — not just the one that VCs happen to care about.

---

## A Note on Complements, Not Competitors

It would be easy to frame Boardy and DeeperPoint as competitors. We use similar tools. We share a country of origin (both are Canadian). We both think AI can fix markets that are broken.

But the framing is wrong, for three reasons:

1. **DeeperPoint is a framework, not a product.** Cosolvent is open source. MarketForge is a deployment architecture for sponsors. DeeperPoint does not compete with anyone because it does not operate marketplaces — it builds tools for organizations that want to operate them.

2. **The market is measured in trillions.** Our recent analysis estimates [thin market friction at $5.7–10.4 trillion globally](thin-market-size.html). Startup networking is one vertical among thousands. There is no scarcity of problems to solve.

3. **Every successful thin market application validates every other one.** When Boardy proves that voice onboarding works for founders, that is evidence that voice onboarding works for grain farmers. When DeeperPoint proves that the Knowledge Slot works for legal matching, that is evidence that curated domain knowledge works for agricultural trade. We are exploring adjacent regions of the same landscape.

If Boardy can thicken the thin market of founders and funders, anything seems possible.

---

*[What makes a thin market tick? →](../thin-markets.html) · [How big is the thin market problem? →](thin-market-size.html) · [The MarketForge platform →](../marketforge.html) · [Twenty examples →](../examples.html)*
