<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->

---
title: "Workshop Notes: How KnowledgeSlot Keeps Its Answers Relevant"
date: 2026-04-06
stream: workshop-notes
tags: [thin-markets, market-design, knowledgeslot, ai, cosolvent, explainer]
summary: A reference library without a metadata schema returns semantically similar text. A reference library with one returns contextually appropriate answers. The difference is the schema — and how it grows.
estimated-read: 8 min read
slug: knowledgeslot-schema-scoped-rag
---

<figure class="blog-hero">
  <img class="blog-hero__img" src="../images/blog/knowledgeslot-schema-scoped-rag-hero.png" alt="A conceptual illustration of semantic matching and metadata filtering." loading="lazy">
  <figcaption>A conceptual illustration of semantic matching and metadata filtering.</figcaption>
</figure>

Retrieval-Augmented Generation — RAG — is the mechanism that lets an AI system answer questions from a curated document library rather than from its training weights alone. It is the engine behind KnowledgeSlot's domain Q&A capability: ingest authoritative reference documents, chunk and embed them, and when a participant asks a question, retrieve the relevant chunks and let the model synthesize an answer.

The problem is that "relevant" is doing a lot of work in that sentence.

In a general-purpose RAG system, relevance is determined by vector similarity — the chunks whose embedding coordinates are closest to the query's embedding coordinates get retrieved. This works well when the document corpus is small and homogeneous. It works poorly when the library spans multiple trade corridors, regulatory jurisdictions, product categories, and document types, because "semantically similar to the query" and "actually applicable to this party's situation" are different things.

A grain buyer in Japan asking about protein measurement methods will get chunks that are semantically similar to "protein measurement" — possibly including chunks from Canadian Grain Commission grading standards, USDA/FGIS standards, EU grain regulations, and GAFTA contract boilerplate all at once. Some of those chunks apply to their situation. Many do not. A model synthesizing from that mixed retrieval set will produce an answer that is, at best, hedged and generic. At worst, it will confidently describe the wrong standard for the wrong jurisdiction.

KnowledgeSlot solves this with a metadata schema — a controlled vocabulary of attributes that describes each reference document in terms of *what it is about and who it applies to*. That schema is not fixed at deployment. It grows as new material is ingested. And it is used to narrow the retrieval scope before vector similarity is calculated.

## What the Schema Is

The metadata schema for a KnowledgeSlot deployment is vertical-specific. It is not a generic document tagging system. For a grain trading marketplace, the schema might include dimensions like `origin_region`, `destination_country`, `product_category`, `document_type`, `trade_corridor`, and `issuing_body`. For a remote mental health services marketplace, the dimensions would be entirely different: `jurisdiction`, `insurance_provider`, `clinical_area`, `license_type`, `regulatory_body`.

Each dimension takes values from a controlled vocabulary — a defined set of terms that mean the same thing across all documents in the library. "Canada" means the same thing whether the document is a Canadian Grain Commission standard or a GAFTA contract clause referencing Canadian origin. "FOB" means the same thing across every contract template, because the schema forces consistency.

This is not a trivial design decision. The reason most document libraries do not work this way is that building and maintaining a controlled vocabulary is overhead — it requires editorial judgment, not just ingestion. KnowledgeSlot's architecture makes this overhead visible and manageable by building the schema curation workflow into the ingestion process itself, rather than treating it as a separate, optional layer.

## How the Schema Grows

When a new document is added to the reference library, it goes through a curation step before it is indexed. A combination of LLM-assisted metadata extraction and human editorial review produces a tag set for the document against the current schema.

But the current schema is not always sufficient. A contract for FOB grain shipments from Ukraine introduces new values into `origin_region` and may introduce a new `trade_corridor` tag that did not exist when the library only contained Canadian corridor contracts. A regulatory update from a new destination country may require a new `regulatory_body` value. A reference document about a certification standard outside the existing `issuing_body` vocabulary requires a schema extension.

The curation process handles this through what the KnowledgeSlot design calls schema analysis: when a newly ingested document cannot be fully described by the existing schema, the system — using an LLM-assisted analysis prompt — proposes extensions. These proposals are reviewed and, when approved, merged into the schema. The vocabulary grows deliberately, with each new document either confirming existing schema dimensions or revealing gaps that need filling.

This progressive growth has an important consequence: the schema is always a description of what the library actually contains, not an aspirational taxonomy of what it might someday contain. Every tag dimension in the schema corresponds to actual documents in the library that carry that tag. This keeps the schema useful and the retrieval scoping accurate — there is no risk of filtering on a dimension that no documents satisfy.

## How the Schema Narrows Retrieval

When a participant asks a question, the retrieval pipeline does not immediately run a similarity search across the entire reference library. It first applies a metadata filter — a set of conditions derived from the schema — to narrow the candidate set.

The filter looks roughly like this:

```sql
SELECT chunk_text, source_document, metadata
FROM reference_library
WHERE destination_countries && ARRAY[$user_country]
  AND product_categories && ARRAY[$user_interests]
  AND document_type = ANY($relevant_types)
ORDER BY embedding <=> $query_embedding
LIMIT $k;
```

The vector similarity (`embedding <=> $query_embedding`) only runs on the rows that survive the metadata filter. The candidate set for similarity search is a slice of the library — the documents that are actually applicable to this party's corridor and product interests — not the entire library.

This matters for retrieval quality in two ways.

First, **precision improves**: the chunks that score highest for similarity are the most relevant chunks from an already-relevant set, not the most similar chunks from an irrelevant set. The Japanese grain buyer's question about protein measurement retrieves from chunks tagged with `destination_country: Japan` and `product_category: grain` — not from the full corpus including EU livestock feed regulations.

Second, **noise is suppressed**: chunks that are semantically similar but contextually inapplicable never enter the retrieval set. A USDA grading standard and a Canadian Grain Commission standard might use nearly identical language to describe protein measurement — but if the query context is a sale to Japan under a CIF Canada corridor, only the latter is applicable. Metadata pre-filtering makes this distinction before vector similarity has a chance to confuse them.

## Automatic User-Context Scoping

The filter parameters in the query above — `$user_country`, `$user_interests`, and so on — are not typed by the participant. They are injected automatically from the participant's registered profile.

When a grain buyer from Japan logs in and asks "what protein measurement method applies to this contract?", they do not say "show me Japanese regulations." The system already knows they are a Japanese buyer operating in grain markets. It injects their country registration and their declared product interests as implicit filter parameters. The question is answered from the relevant slice of the library without the participant having to articulate their context in every query.

This is the mechanism that makes domain Q&A feel like talking to an expert rather than querying a database. An expert in grain trading does not ask "what are your regulatory requirements, product categories, and destination jurisdiction?" before answering a question. They already know who they are talking to. The automatic scoping gives the KnowledgeSlot AI system the same baseline awareness.

## The Shared Vocabulary Guardrail

There is a third design dimension that the schema architecture enables, though it is not visible to participants: coherence between the Knowledge Slot and the Context Slot.

The Context Slot holds participant-supplied documents — profiles, capability descriptions, deal histories. These are tagged using a participant metadata schema derived from the marketplace's `MarketDefinition` — the field vocabulary that defines what participants disclose about themselves. The Knowledge Slot's `reference_metadata_schema` covers different content but overlapping concepts: both use geographical terms, product category identifiers, and certification types.

The architectural guardrail is that both schemas must draw from the same controlled vocabulary for these shared concepts. "Canada" in a participant's country-of-origin field and "Canada" in a reference document's `origin_region` tag are the same token. This shared vocabulary is what makes cross-slot retrieval possible in the future — queries that span participant profiles and the reference library in a single search, using the same embedding model and the same metadata dimensions.

The schema is not just a filtering tool. It is the connective tissue that makes the two-slot retrieval architecture coherent.

## Synthesizing the Match: Where Knowledge Meets Context

The true power of this shared metadata schema becomes evident when a marketplace uses Cosolvent to identify potential deals. In a thin market, traditional matching relies on exact criteria overlaps. A Cosolvent-powered architecture instead relies on a tri-part interaction:

1.  **User Context:** The declared profiles and capability descriptions of the two parties (managed via the Context Slot).
2.  **Semantic Matching:** Cosolvent's ability to identify latent or non-obvious alignment between the parties' qualitative needs and capabilities.
3.  **Industry Context:** The authoritative regulatory, technical, and structural constraints provided by KnowledgeSlot.

Because all three components rely on a shared metadata vocabulary, the system can evaluate a potential match not just on semantic similarity, but on practical feasibility. The metadata schema acts as the Rosetta Stone. It allows Cosolvent to ask: *Do these two participants align on product capabilities? And if they do, does KnowledgeSlot's industry context indicate any insurmountable regulatory hurdles for their specific jurisdictions?* 

When the schema aligns across all these dimensions, the system isolates deal combinations that don't just look good in theory, but make practical sense given the structure of the market. It can explain *why* the match works, citing both the participants' profiles and the underlying industry rules that validate the transaction.

## The Generative Match Story: A Neutral Starting Point

Once a practically viable match is surfaced, the participants still face the challenge of initiating a complex conversation. To bridge this gap, the platform can deploy a conceptual tool layered on top of the aligned information: the Generative Match Story.

When a promising match is identified, either prospective party can request the system to generate a narrative scenario illustrating how they could effectively work together. Drawing on the Cosolvent semantic alignment, the specific user contexts, and the KnowledgeSlot industry constraints, the system crafts a brief, realistic "story."

The content and format resemble a conversational use-case vignette (similar to a "Market Scenario" post). It doesn't write a contract or prescribe terms. Instead, it narrates a hypothetical successful transaction—from initial need to final satisfaction—incorporating the specific constraints and capabilities of both participants. 

This story serves a crucial market engineering function: it allows participants to start their discussions from a neutral, objectified scenario rather than defensively negotiating from their own starting positions. It translates abstract alignment and regulatory compliance into an easy-to-understand vision of mutual success, significantly lowering the friction of initial engagement.

## What This Looks Like in Practice

In the grain trading vertical that KnowledgeSlot is currently developing for, the schema has been built from the GAFTA No. 27 contract and is being extended as additional GAFTA contracts, Canadian Grain Commission standards, and destination-country regulatory documents are added. Each new document either maps cleanly onto existing schema dimensions or proposes new values that are reviewed and merged.

When a Canadian seller and a Philippine buyer are matched by Cosolvent, it is because their specialized capabilities align and the shared metadata confirms the trade corridor is viable. If the buyer requests a generative match story, the system will output a narrative of the grain shipment, specifically mentioning how the Canadian seller's product seamlessly meets the Philippine phytosanitary requirements pulled from KnowledgeSlot. The parties then open their conversation by discussing the narrative's assumptions, rather than staring at a blank screen.

The metadata schema is what turns a document library into a domain-aware advisor, and a matching engine into a practical dealmaker. Without it, RAG retrieves what is semantically similar, and matching engines surface what might technically connect. With it, the architecture retrieves what is actually applicable, and surfaces deals that can actually close.

---

*KnowledgeSlot is the domain knowledge component of DeeperPoint's marketplace toolkit. Its relationship to the Cosolvent harness and the matching architecture is described in the [MarketForge](../marketforge.html) overview. The theoretical case for authoritative information as a market engineering intervention is in the [DeeperPoint whitepaper](../whitepaper.html).*
