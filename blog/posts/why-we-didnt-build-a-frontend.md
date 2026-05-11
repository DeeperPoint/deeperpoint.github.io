---
title: "Workshop Notes: Why We Didn't Build a Frontend"
date: 2026-05-11
stream: workshop-notes
tags: [market-design, cosolvent, ai, architecture]
summary: The reasoning behind making Cosolvent a headless engine and why standardizing the participant interface destroys the very heterogeneity that makes thin markets valuable.
estimated-read: 5 min read
slug: why-we-didnt-build-a-frontend
---

When we set out to build Cosolvent, our objective was to dramatically reduce the time it takes to test a new thin market platform. If you see a structural matching failure in the artisanal craft sector or a regulatory bottleneck in diaspora property investments, you should be able to spin up the infrastructure to solve it in days, not quarters.

We needed matching logic. We needed permission roles. We needed a sponsor dashboard to govern the transactions.

But we explicitly decided *not* to build a participant frontend.

Cosolvent is a headless marketplace engine. It provides a robust, deterministic backend API for participants, but no out-of-the-box user interface for the buyers and sellers actually using the market. The sponsor has to build that themselves.

To many software engineers, this sounds like an incomplete product. Why build the engine but leave out the steering wheel? The answer lies in the physics of thin markets themselves.

### The Standardization Trap

Thick markets—like ride-sharing or consumer e-commerce—thrive on standardization. An Uber ride in Toronto is the same transaction as an Uber ride in Tokyo. The interface can be rigid and universal because the service being exchanged has been deliberately commoditized.

Thin markets are the exact opposite. Their value comes from their heterogeneity. 

A platform matching junior mining exploration projects to joint-venture capital requires an interface that understands NI 43-101 compliance reports, geological survey maps, and complex earn-in equity structures. A platform matching heritage restoration craftspeople to historical society commissions needs an interface that understands conservation standards, portfolio verification, and apprenticeship lineage.

If we had tried to build a universal participant frontend for Cosolvent, we would have inevitably forced standardization onto these markets. We would have reduced complex, high-stakes, context-dependent deals into generic "item" and "price" fields. 

In trying to make the software easier to deploy, we would have destroyed the very nuance that makes these markets work.

### The Separation of Engine and Context

The solution was to draw a hard architectural boundary. 

**The engine defines structure.** Cosolvent handles the universal physics of market engineering: semantic vector matching, three-tier data visibility, state-persisted communication channels, role-based permissions, and the deterministic generation of APIs from a central configuration file.

**The vertical defines content.** The market sponsor—the industry association, the specialized broker, the domain expert—defines what the market actually is. They dictate the ontology, the rules of engagement, and most importantly, the participant experience.

By remaining headless, Cosolvent forces the sponsor to design an interface that makes sense for their specific buyers and sellers. It preserves the local context.

### The Role of AI in Frontend Generation

A few years ago, telling a non-technical domain expert to "just build the frontend yourself" against a REST API would have been a death sentence for adoption. It would have required a dedicated engineering team and months of bespoke development.

Today, the landscape has changed.

Cosolvent automatically generates a comprehensive, deterministic OpenAPI specification based on the sponsor's unique market configuration. Because this specification is rigid and explicitly typed, modern AI coding assistants can consume it and generate a fully functional client SDK—and a tailored frontend interface—in a matter of hours.

The sponsor doesn't need to write the boilerplate wiring. They can use AI to build a custom participant frontend that respects the specific vernacular, workflow, and trust signals of their industry.

### The Right Tool for the Job

Software architecture is always a reflection of market structure. Standardized, high-volume markets get monolithic, one-size-fits-all platforms. 

Thin markets require something different. They require a powerful engine that does the heavy lifting of coordination and matching, paired with a hyper-local, context-aware interface that speaks the language of the participants. 

By making Cosolvent headless, we ensured it could be the former, without ever pretending to be the latter.
