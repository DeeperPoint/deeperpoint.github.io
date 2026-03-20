<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->

---
series: intro-series
series-title: "Why I'm Building Tools for Markets That Don't Exist Yet"
series-position: 3
title: "Workshop Notes: The Skeleton Key"
slug: intro-skeleton-key
date: 2026-03-20
tags: [thin-markets, market-design, cosolvent, marketforge, ai, explainer, roadmap]
summary: "You can't build 10,000 custom platforms for 10,000 niche markets. But you also can't smash the nuances into a generic template. DeeperPoint's answer: an open-source configurable framework — a skeleton key — that adapts to any vertical. Part 3 of a 4-part series."
estimated-read: 6 min read
---

<figure class="blog-hero">
  <img class="blog-hero__img" src="../images/blog/intro-skeleton-key-hero.png" alt="A skeleton key transforming into a network of doors opening to different market verticals" loading="lazy">
  <figcaption>One configurable framework. Many different markets.</figcaption>
</figure>

*Part 3 of 4 — Why I'm Building Tools for Markets That Don't Exist Yet*

In [Part 1](intro-veterinarians-xray.html) I described the pattern: thin markets that look wildly different on the surface all share the same five structural forces underneath. In [Part 2](intro-trillions-in-shadows.html) I quantified the scale: up to $10.4 trillion in missing global commerce. The problem is enormous and it is everywhere.

Whenever a problem is measured in trillions, the reflexive Silicon Valley response is to build a proprietary platform, capture the market, and extract a toll. That instinct is wrong here, and understanding *why* it's wrong is the key to understanding DeeperPoint.

## Why the platform playbook fails

A conventional marketplace — Shopify, Upwork, even Airbnb — works because it standardises the offering. You squeeze diverse goods or services into a uniform listing format, then match on a few sortable fields: price, location, rating. This strategy creates thickness by *destroying information*. It works beautifully for commodity goods and routine services.

In thin markets, the information you'd have to destroy is the entire reason the transaction has value. A heritage timber framer's capabilities cannot be reduced to a star rating. A specialty malting barley variety's characteristics cannot be captured in a product category dropdown. A collaborative family lawyer's particular expertise in high-conflict custody cases is precisely what makes her valuable — and precisely what a standard search filter cannot express.

You can't build 10,000 custom platforms for 10,000 niche verticals. The overhead would be absurd. But you also can't smash the nuances into a generic template and expect the matching to work.

What you need is something in between: a *configurable framework* — a skeleton key that opens many different doors because it understands the common underlying lock mechanism, while letting each door's owner furnish the room behind it to suit their needs.

## The DeeperPoint stack

This is what [DeeperPoint's toolkit](../marketforge.html) is designed to be. It has four layers, each solving a different piece of the puzzle:

**[Cosolvent](https://github.com/DeeperPoint/Cosolvent)** is the open-source core — MIT-licensed, free to use, free to modify. It handles the hardest universal problems of thin market engineering: AI-driven onboarding that lets participants describe complex offerings in natural language rather than rigid forms; semantic vector matching that understands "precision heritage restoration" and "historical masonry conservation" are the same thing even when they share zero keywords; and multilateral deal assembly that pulls in the insurers, certifiers, and logistics partners a complex transaction requires. The [Cosolvent explainer](cosolvent-toolkit.html) goes deeper on what it handles and — just as importantly — what it deliberately defers.

**KnowledgeSlot** is the domain intelligence layer. Cosolvent can match, but it needs to know *what matters* in a given vertical. What certifications does a heritage mason need? What grading standards apply to barley destined for craft brewing? What regulatory framework governs collaborative family law in Ontario? KnowledgeSlot captures, structures, and maintains this industry-specific knowledge using AI-assisted curation.

**ClientSynth** generates realistic synthetic populations of marketplace participants — buyers, sellers, intermediaries — so that a market sponsor can stress-test matching quality and deal flow *before* recruiting a single real user. These synthetic profiles are [used only for testing and demonstration](../mf-clientsynth.html) — never mixed with real users.

**MarketForge** is the integration layer that combines all three upstream tools into a deployable, sponsor-ready marketplace platform for a specific vertical.

## The open/proprietary boundary

People sometimes ask why the whole stack isn't open source. The answer is practical, not philosophical.

Cosolvent — the matching engine — is open because the core market physics are universal. Semantic matching, multilateral assembly, and role-based permissions work the same way regardless of whether you're matching timber framers or grain buyers. Democratising that infrastructure is the only strategy that matches the *scale* of the problem. No single company can build marketplaces for every thin market on earth. The community has to be able to do it.

But standing up a live marketplace in a specific vertical requires *domain-specific labour* that doesn't scale automatically. Someone has to map the ontology — learn the grading systems, the certification requirements, the trust norms, the cultural expectations of a particular industry. Someone has to generate and validate synthetic test populations. Someone has to coach the market sponsor through configuration. That work is irreducibly human, and I cannot afford to subsidise it indefinitely.

The upper layers are proprietary not because I want to gatekeep — but because the labour of customisation is real, and the project has to be financially sustainable to survive.

## The sponsor model — and the investor case

The toolkit doesn't replace the domain expert. It empowers them. DeeperPoint's architecture assumes that every thin market has a natural **sponsor** — an entity with the authority, the trust, and the industry knowledge to stand up a functioning marketplace: a grain cooperative, a provincial legal aid society, a trade association, a diaspora community network, a municipal economic development office.

The sponsor brings the vertical expertise and the community trust. The toolkit provides the [configurable software architecture](../market-diagnostic.html). Together, they can stand up a marketplace that neither could build alone.

There is also an **investor** angle. Some thin markets are large enough that a profitable business can be built on top of a functioning matching platform — transaction fees, premium placement, data services, fulfilment brokerage. A venture firm managing a portfolio of thin-market startups could use the shared DeeperPoint framework to mine the structural commonalities across its portfolio, making each individual venture more capital-efficient. The five-forces diagnostic is the same; the commercial opportunity differs by vertical.

## Where the toolkit stands today

I want to be transparent about readiness. The DeeperPoint stack is under active development — there is enough working code that the design direction is real and testable, but each component (Cosolvent, KnowledgeSlot, ClientSynth, MarketForge) has a published [roadmap](../marketforge.html) that I maintain and update. This is an honest R&D project, not a product launch.

One concrete milestone on that roadmap: DeeperPoint is building **GPSim**, a MarketForge-inspired market simulator that models the Canadian specialty grain-to-Asia scenario end to end. GPSim is well into development but still some months from public release. When it's ready, it will be the first full demonstration of how the toolkit handles a real cross-border thin market — from semantic onboarding through matching through deal assembly — against realistic synthetic participants.

You can examine the open-source core of Cosolvent [right now](https://github.com/DeeperPoint/Cosolvent). But a harness without people who use it is just code. What it needs is the right collaborators.

That's the subject of Part 4.

*Next: [Part 4 — An Open Invitation →](intro-open-invitation.html)*
