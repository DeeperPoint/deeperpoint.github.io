<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->

---
title: "Workshop Notes: The Knowledge Problem at the Heart of Every Thin Market"
date: 2026-04-05
slug: tribal-knowledge-thin-markets
stream: workshop-notes
tags: [thin-markets, market-design, explainer, trade, founders]
summary: In thin markets, the goods are complex and the counterparties are strangers. Standardization doesn't help — it destroys the value. The only substitute is tribal knowledge. And tribal knowledge has a lifespan.
estimated-read: 6 min read
---

<figure class="blog-hero">
  <img class="blog-hero__img" src="../images/blog/tribal-knowledge-thin-markets-hero.png" alt="A seasoned broker stands at the center of a trading floor, the only connection between buyers and sellers on either side" loading="lazy">
  <figcaption>The knowledge that closes deals lives in one person's memory. That is both the strength and the problem.</figcaption>
</figure>

There is a standard explanation for why markets fail to form. The textbook version involves transaction costs, information asymmetry, and trust deficits. These are real, but they miss something more fundamental.

In a thin market, the thing being exchanged resists description.

This is not an accident. It is the definition. A grain shipment with standard specs, standard delivery terms, and standard pricing is a commodity — it trades in a thick market, with many buyers, many sellers, and price discovery that happens in real time. The moment those specifications become unusual — a specific protein content, a particular origin corridor, a storage history that matters for end use — the market thins. The more specific the requirement, the fewer parties can fill it. The fewer parties, the harder it is to find each other and agree.

The complexity is the value. And the complexity is the problem.

## The Stranger Problem

Human beings have been navigating complex exchanges with known counterparties for millennia. Business relationships built on repeated interaction, shared networks, common professional vocabulary, and mutual accountability produce surprisingly efficient outcomes even without formal contracts or regulatory oversight. The grain merchant who buys from the same cooperative every harvest, the manufacturer who has sourced specialty components from the same family shop for thirty years — these are relationships that encode enormous amounts of mutual knowledge without anyone writing it down.

Thin markets destroy this comfort. By definition, a thin market is one where there are not enough known counterparties to sustain the exchange. The buyer who needs a specific product or service has to find a seller they have never dealt with. The seller has to trust a buyer whose reliability is unproven. Both have to communicate about something complex — something that resists the kind of shorthand that familiarity normally provides.

Two parties, barely known to each other, trying to negotiate something neither can describe in simple terms. This is the structure of every thin market transaction.

## What Tribal Knowledge Does

The term "tribal knowledge" captures something specific: the domain understanding that circulates within a professional community and is never written down. It includes the vocabulary that practitioners use among themselves, the standards that are technically optional but practically mandatory, the difference between what a contract says and what it means in practice, the judgment about which specifications matter and which ones are pro forma.

In thick markets, this knowledge is distributed across enough participants that most parties already have it, or can acquire it cheaply. In thin markets, it is concentrated in the hands of a few — usually the brokers and intermediaries who have spent careers working the specific corridor, vertical, or domain where the exchange happens.

This creates a dependency that is productive but fragile.

Productive, because a good broker doesn't just find counterparties — they translate between them. They know that a buyer in Southeast Asia asking for "high-protein wheat" means something different than a European mill asking for the same thing. They know which contract template applies in which corridor, which quality inspectors are trusted by which ports, which regulatory requirements are enforced strictly and which are routinely waived. They make complex exchanges intelligible to parties who do not share a common professional vocabulary.

Fragile, because this knowledge is personal. It lives in the broker's memory. It does not transfer reliably when brokers retire, change firms, or simply move on. And it has a darker dimension: knowledge that cannot easily be acquired elsewhere is knowledge that can be rationed. A broker who controls access to a market has leverage — leverage that is generally benign when times are good, and that becomes something else when an industry comes under pressure.

## The Structural Question

Any system that wants to reduce friction in thin markets has to grapple with this directly. The tribal knowledge problem is not a bug in how specific markets are organized. It is a structural feature of thinness itself — an unavoidable consequence of trading in complex, heterogeneous goods with counterparties who are not already part of your network.

You cannot standardize your way out of it. Standardization sacrifices the very specificity that makes the goods valuable. You cannot simply scale the broker model — there are not enough brokers, and scaling the model would reproduce its fragility and its incentive problems.

The question is whether you can make the relevant domain knowledge available to parties who do not already have it — at the moment they need it, in a form they can use, without requiring either party to first become an expert in the other's operating context.

AI technology is the most plausible candidate for taking on this role at scale. A system trained on the authoritative reference material of a specific domain — the contracts, regulations, standards, and procedural knowledge that constitute the tribal knowledge of that vertical — could in principle serve every participant on a marketplace as a shared resource. It would not retire. It would carry no client relationships that create conflicting loyalties. It would have no financial incentive to ration the information it holds.

Whether that actually works in practice is a different matter. The theoretical case is reasonable. The engineering is feasible. But translating the nuanced, contextual judgment of a seasoned human broker into a system that reliably serves unfamiliar parties across diverse corridors and edge cases is not a solved problem. It is a hypothesis. A plausible one — but a hypothesis.

DeeperPoint is building the scaffolding that allows sponsors of specific thin market platforms to test it. Not a demonstration, not a proof of concept — a working set of tools that a sponsor can deploy in a real market vertical, with real participants, and find out whether the hypothesis holds where it matters: in the field.

---

*This post introduces a series on why thin markets fail to close even after parties have found each other. The next two posts go deeper into the architecture: [why a semantic match isn't enough](why-industry-context-closes-deals.html) to close a deal, and [how a metadata schema makes domain knowledge retrievable](knowledgeslot-schema-scoped-rag.html) at the right level of specificity.*
