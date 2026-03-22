---
series: ai-cooperative-manufacturing
series-title: "New Frontier: AI Powered Cooperative Manufacturing"
slug: csss-software-ecosystem
series-position: 6
title: "Workshop Notes: The Software Stack That Surrounds a CSSS"
date: 2026-03-22
stream: workshop-notes
tags: [thin-markets, market-design, ontario, manufacturing, ai, marketforge, explainer, roadmap]
summary: A Cooperative Specialization Support System does not land in a vacuum. Every manufacturing firm it touches already runs CAD/CAM, ERP, PLM, and possibly TMS or WMS software. Here is a realistic, four-phase map of how a CSSS can enter that ecosystem without disrupting it — and without cutting off a future where the systems speak fluently with each other.
estimated-read: 9 min read
---

## The Software Already in the Room

When we describe a Cooperative Specialization Support System (CSSS) — an AI-mediated cooperation marketplace that helps manufacturing SMEs discover and engage each other's idle capacity, skills, and equipment — it is tempting to describe it in isolation. A clean new system. A blank slate.

To be precise about what we are describing: a CSSS is an operator application built on DeeperPoint's open **Cosolvent** protocol — the same semantic matching and trust infrastructure that governs firm-level cooperation in the Ontario Pocket scenarios. **MarketForge** is DeeperPoint's prototype implementation of that operator layer, the deployment vehicle a sponsor organization would configure to run a real regional manufacturing CSSS. It is this system — Cosolvent as the protocol engine, MarketForge as the configurable application on top — that will have to coexist with the software already running on every shop floor it touches.

That is not the reality.

Every manufacturing firm a regional CSSS would touch already runs software. Most of it is old, expensive to replace, deeply integrated into daily operations, and operated by people who are not eager to learn new systems. Specifically:

- **CAD/CAM software** (SolidWorks, AutoCAD, Mastercam, Siemens NX, Fusion 360) — the tools that design parts and generate machine programs. These systems hold precise 3D geometry, tolerances, and process parameters. They are also, depending on the shop, the most sensitive intellectual property the firm possesses.
- **ERP systems** (Epicor, JobBoss, Infor, SAP Business One, Syspro, even Excel) — enterprise resource planning, which tracks customer orders, inventory, purchase orders, machine scheduling, labour, and financial accounting. An ERP is effectively the operating model of the business, expressed in data.
- **PLM software** (Windchill, Teamcenter, Arena) — product lifecycle management, tracking design revisions, engineering change orders, and document controlled processes across the life of a product. More common in aerospace and automotive Tier 1 than in typical job shops, but present wherever certification matters.
- **TMS and WMS** (transportation management and warehouse management systems) — logistics software governing inbound materials, outbound shipments, and physical inventory movement. Less universal in job shops, but significant in any operation that manages a supply chain.

A CSSS that ignores these systems will fail. Shop floor managers will not tolerate re-entering data across platforms they didn't ask for. ERP systems will not cheerfully surrender scheduling data to a new external marketplace without explicit integration. CAD files will not flow between companies through a cooperation marketplace if there is no governed mechanism for managing their confidentiality and version control.

The question is not whether the CSSS needs to coexist with this software ecosystem. It does. The question is *how* — and at what pace.

We propose a four-phase integration roadmap that begins grounded and pragmatic, and progresses incrementally toward deep, programmatic interoperability. No phase requires abandoning the previous one. Each phase delivers real value while keeping the door to the next phase open.

---

## Phase 1 — Awareness Without Integration

**The CSSS exists. The other systems ignore it.**

In Phase 1, the CSSS operates as an entirely stand-alone system. It maintains its own capability profiles — machine specs, certifications, scheduling availability, operator skills — entered by participants directly into the CSSS interface. It runs its own matching engine. It generates its own transaction records. It does not read from, write to, or authenticate against any external software in the participant's stack.

The other systems — ERP, CAD/CAM, PLM — are simply aware that the CSSS exists, in the same way a shop is aware that a trade directory exists: as a resource they might consult, not a system they are connected to.

In practice, this means:
- A shop owner logs into the CSSS separately from their ERP
- Capacity availability is manually entered ("Machine 3 is available second shift Tuesday through Thursday for the next six weeks")
- Order information from the ERP is not automatically reflected in the CSSS
- Design files are not transmitted through the CSSS; they are shared through separate channels (email, FTP, USB) once a match is made and parties have agreed to disclosure

**Why start here?** Because it works, and because it is deployable without requiring any software vendor's cooperation. The CSSS can prove its value — revealing matches, enabling transactions, reducing friction — without touching the incumbent systems. Critically, no design decisions made in Phase 1 should *close off* Phases 2, 3, or 4. The CSSS's data schema, API surface, and authentication model must be built from day one as if integration will eventually come, even if it is not yet happening.

Phase 1 is also the phase where the CSSS earns trust. Participants need to experience the system working, correctly and securely, before they are willing to grant it access to anything sensitive.

---

## Phase 2 — File Exchange and Supervised API

**The systems can talk. Humans decide when they do.**

In Phase 2, the CSSS gains the ability to exchange structured data with its companion systems — but every exchange is initiated and supervised by a human. The machines do not automatically talk to each other; rather, the platform provides buttons and exports that humans press when they are ready.

This takes two forms:

**Standard file exchange.** The most common enterprise data formats — STEP and IGES for 3D geometry, PDF for documents, CSV for scheduling data, XML or JSON for ERP exports — are universally supported by the major manufacturing software packages. The CSSS should be able to import and export in these formats natively. A participant who wants to share a part geometry with a potential capacity partner can export a STEP file from SolidWorks and upload it to the CSSS's secure match-scoped data room in three clicks. A participant who wants to update their CSSS availability to reflect their current ERP schedule can export a CSV from JobBoss and import it into the CSSS in two steps. These are not integrations; they are file exchanges. The human carries the data from one system to the other.

**Supervised API connectors.** The larger enterprise software vendors — SAP, Epicor, Infor, Siemens — publish APIs that allow authorized external applications to read (and in some cases write) data. In Phase 2, the CSSS offers pre-built API connectors to the most common platforms in the target market. These connectors are *opt-in* and *human-supervised*: a participant must explicitly authorize the connector, specify exactly which data fields the CSSS is allowed to read, and is presented with a clear preview of what the CSSS will import before any sync occurs. There are no background jobs that pull data automatically. The human initiates every synchronization.

What does a Phase 2 API connector actually do? A useful example: the CSSS reads a participant's current machine schedule from their ERP (available with approval) and automatically updates the participant's capacity availability profile in the CSSS. Instead of manually entering "Machine 3 is available second shift Tuesday through Thursday," the shop's production planner clicks "Sync from ERP" and the CSSS updates itself from live scheduling data. The planner reviews the result, confirms it, and publishes. The CSSS never writes back to the ERP without explicit instruction.

**The MCP dimension.** As the Model Context Protocol (MCP) matures as a standard for LLM-to-application communication, Phase 2 can also introduce MCP-based connectors as an alternative to REST APIs for systems that support it. MCP allows an AI agent to query a connected application in structured natural language ("What is Machine 3's schedule for next week?") and receive a structured response — a more flexible and semantically richer exchange than a fixed API endpoint. In Phase 2, MCP connectors, like API connectors, are human-supervised: the CSSS's AI agent can be instructed to query a connected ERP via MCP, but a human reviews and approves the result before it affects match output.

The principle of Phase 2 is **supervised interoperability**. The systems can exchange data. The human remains in the loop for every exchange.

---

## Phase 3 — Programmatic Context Retrieval

**The CSSS can ask. The other systems answer. For specific, bounded purposes.**

In Phase 3, the CSSS gains the ability to programmatically query its companion systems in real time — but only for information relevant to matching, and only within a strictly defined scope of access that the participant has pre-configured.

The key distinction from Phase 2 is that Phase 3 queries are initiated by the CSSS, not by a human. When a potential match is forming — when the AI matching engine is evaluating whether a specific shop can fulfill a specific requirement — it can call out to the shop's connected ERP or scheduling system to retrieve current availability data, without waiting for a human to run a synchronization job.

Concretely, this might look like:

- **Machine availability queries:** The CSSS's AI matching engine issues a real-time query to a participant's connected ERP and retrieves the current schedule for a specific machine, confirming (or disconfirming) availability within the match timeline.
- **Certification status queries:** For participants whose PLM system tracks document-controlled certifications (AS9100D, ISO 13485, IATF 16949), the CSSS can query the current certification status and expiry date directly from the PLM, rather than relying on a manually maintained profile field that may be out of date.
- **Material stock queries:** For capacity-sharing transactions that require the receiving shop to have specific raw materials available, the CSSS can query a connected inventory or ERP system to verify stock levels before presenting a match.

All queries in Phase 3 are bounded by a **participant-defined consent model** established during configuration. The participant specifies:
- Which systems the CSSS is authorized to query
- Which specific data fields or query types are permitted
- Whether query results require human review before being used in a match calculation, or whether they can be used automatically

Confidentiality is a first principle. The CSSS does not expose a participant's internal data to their match counterparties. An availability query confirms whether a machine is available for a proposed window — it does not expose the name of the other customer occupying that machine's schedule, the price of that contract, or any other commercially sensitive information from the ERP.

Phase 3 is the phase where matching quality improves dramatically. Phase 1 and Phase 2 matches are based on manually curated capability profiles, which are inherently backward-looking (they reflect what a shop was doing when someone last updated their profile). Phase 3 matches are based on live system state. The difference between "we nominally have two Makino five-axis machines" and "right now, today, Machine 2 has fourteen hours of open schedule time next week at second shift" is the difference between a match that might work and a match that will work.

---

## Phase 4 — Full Integration

**The systems collaborate. The CSSS is woven into the fabric.**

Phase 4 is the horizon we can see but cannot fully specify today. It is the state where the CSSS is not a parallel system that has learned to query its companions, but a peer member of the firm's software ecosystem — reading and writing across the stack in real time, with appropriate authorization, to orchestrate productive engagements from beginning to end.

In a Phase 4 world, a confirmed capacity-sharing engagement between two firms might automatically:
- Insert a work order into the receiving firm's ERP
- Update the supplying firm's machine schedule with the reserved block
- Trigger a design file transfer through a governed, version-controlled data room tied to the PLM system
- Generate a logistics routing request to the firms' TMS or freight broker

Phase 4 implies a level of industry-wide software standardization and interoperability that does not yet exist. ERP systems from different vendors do not share a common data model. CAD files from different software packages require translation. PLM systems are notoriously siloed. Achieving Phase 4 integration broadly will require either a sustained effort by software vendors to adopt open data standards for manufacturing interoperability, or a CSSS large enough to justify custom integration with each major platform individually, or — most likely — both.

**The critical design constraint for Phases 1 through 3:** Do not build anything that makes Phase 4 harder. The CSSS's API design, data schema, authentication model, and consent framework must be designed as if Phase 4 will eventually arrive, even if the current implementation is only Phase 1. Proprietary data locks, platform-specific encodings, and architectural shortcuts that make current integration cheaper but future integration impossible are the enemy. The open-standard principle — data portability, vendor independence, auditable schemas — that governs the Cosolvent cooperation marketplace at the firm level applies equally to the CSSS's own software integration architecture.

---

## Where This Puts Us Today

For current planning purposes, any CSSS deployment should be designed and launched as a Phase 1 system — stand-alone, self-consistent, and fully functional without external software integration. The matching engine, the capability registry, the trust and confidentiality architecture, the transaction protocols — all of these must work completely in Phase 1, without a single API call to an ERP or CAD system.

Phase 1 is not a limitation. It is a deliberate and defensible starting point. It lets the cooperation marketplace prove its value on real transactions. It lets participants build trust in the system before granting it access to sensitive internal data. And it lets the CSSS team learn which integrations are actually needed — by watching what data participants manually carry between systems — rather than speculating in advance about which API connectors to build.

The phases that follow are not a product roadmap; they are a structural promise. The design decisions made in Phase 1 determine whether the path to deep integration remains open. Make them carefully.

---

*[The DeeperPoint thin market framework →](https://deeperpoint.com/thin-markets.html) · [The MarketForge platform →](https://deeperpoint.com/marketforge.html) · [The Cosolvent open protocol →](https://github.com/DeeperPoint/Cosolvent)*
