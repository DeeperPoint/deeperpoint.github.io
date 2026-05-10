<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->

---
title: "Workshop Notes: How CommonContext Keeps Its Answers Relevant"
date: 2026-04-06
stream: workshop-notes
tags: [thin-markets, market-design, commoncontext, clientsynth, ai, cosolvent, explainer]
summary: A reference library without a metadata schema returns semantically similar text. A reference library with one returns contextually appropriate answers. The difference is the schema — and how it grows.
estimated-read: 5 min read
slug: commoncontext-schema-scoped-rag
---

<figure class="blog-hero">
  <img class="blog-hero__img" src="../images/blog/commoncontext-schema-scoped-rag-hero.png" alt="A conceptual illustration of semantic matching and metadata filtering." loading="lazy">
  <figcaption>A conceptual illustration of semantic matching and metadata filtering.</figcaption>
</figure>

Retrieval-Augmented Generation — RAG — is the mechanism that lets an AI system answer questions from a curated document library rather than from its training weights alone. It is the engine behind CommonContext's domain Q&A capability: ingest authoritative reference documents, chunk and embed them, and when a participant asks a question, retrieve the relevant chunks and let the model synthesize an answer.

The problem is that "relevant" is doing a lot of work in that sentence.

In a general-purpose RAG system, relevance is determined by vector similarity — the chunks whose embedding coordinates are closest to the query's embedding coordinates get retrieved. This works well when the document corpus is small and homogeneous. It works poorly when the library spans multiple trade corridors, regulatory jurisdictions, product categories, and document types, because "semantically similar to the query" and "actually applicable to this party's situation" are different things.

A grain buyer in Japan asking about protein measurement methods will get chunks that are semantically similar to "protein measurement" — possibly including chunks from Canadian Grain Commission grading standards, USDA/FGIS standards, EU grain regulations, and GAFTA contract boilerplate all at once. Some of those chunks apply to their situation. Many do not. A model synthesizing from that mixed retrieval set will produce an answer that is, at best, hedged and generic. At worst, it will confidently describe the wrong standard for the wrong jurisdiction.

CommonContext solves this with a metadata schema — a controlled vocabulary of attributes that describes each reference document in terms of *what it is about and who it applies to*. That schema is not fixed at deployment. It grows as new material is ingested. And it is used to narrow the retrieval scope before vector similarity is calculated.

## What the Schema Is

The metadata schema for a CommonContext deployment is vertical-specific. It is not a generic document tagging system. For a grain trading marketplace, the schema might include dimensions like `origin_region`, `destination_country`, `product_category`, `document_type`, `trade_corridor`, and `issuing_body`. For a remote mental health services marketplace, the dimensions would be entirely different: `jurisdiction`, `insurance_provider`, `clinical_area`, `license_type`, `regulatory_body`.

Each dimension takes values from a controlled vocabulary — a defined set of terms that mean the same thing across all documents in the library. "Canada" means the same thing whether the document is a Canadian Grain Commission standard or a GAFTA contract clause referencing Canadian origin. "FOB" means the same thing across every contract template, because the schema forces consistency.

This is not a trivial design decision. The reason most document libraries do not work this way is that building and maintaining a controlled vocabulary is overhead — it requires editorial judgment, not just ingestion. CommonContext's architecture makes this overhead visible and manageable by building the schema curation workflow into the ingestion process itself, rather than treating it as a separate, optional layer.

## How the Schema Grows

When a new document is added to the reference library, it goes through a curation step before it is indexed. A combination of LLM-assisted metadata extraction and human editorial review produces a tag set for the document against the current schema.

But the current schema is not always sufficient. A contract for FOB grain shipments from Ukraine introduces new values into `origin_region` and may introduce a new `trade_corridor` tag that did not exist when the library only contained Canadian corridor contracts. A regulatory update from a new destination country may require a new `regulatory_body` value. A reference document about a certification standard outside the existing `issuing_body` vocabulary requires a schema extension.

The curation process handles this through what the CommonContext design calls schema analysis: when a newly ingested document cannot be fully described by the existing schema, the system — using an LLM-assisted analysis prompt — proposes extensions. These proposals are reviewed and, when approved, merged into the schema. The vocabulary grows deliberately, with each new document either confirming existing schema dimensions or revealing gaps that need filling.

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

This is the mechanism that makes domain Q&A feel like talking to an expert rather than querying a database. An expert in grain trading does not ask "what are your regulatory requirements, product categories, and destination jurisdiction?" before answering a question. They already know who they are talking to. The automatic scoping gives the CommonContext AI system the same baseline awareness.

## The Shared Vocabulary Guardrail

There is a third design dimension that the schema architecture enables, though it is not visible to participants: coherence between the CommonContext and the Context Slot.

The Context Slot holds participant-supplied documents — profiles, capability descriptions, deal histories. These are tagged using a participant metadata schema derived from the marketplace's `MarketDefinition` — the field vocabulary that defines what participants disclose about themselves. The CommonContext's `reference_metadata_schema` covers different content but overlapping concepts: both use geographical terms, product category identifiers, and certification types.

The architectural guardrail is that both schemas must draw from the same controlled vocabulary for these shared concepts. "Canada" in a participant's country-of-origin field and "Canada" in a reference document's `origin_region` tag are the same token. This shared vocabulary is what makes cross-slot retrieval possible in the future — queries that span participant profiles and the reference library in a single search, using the same embedding model and the same metadata dimensions.

The shared vocabulary guardrail also applies to ClientSynth, DeeperPoint's synthetic agent simulator. When bootstrapping or testing a thin market platform, the schema defines the categorical space within which synthetic profiles are generated — their declared geographies, product categories, and capability types. This means ClientSynth-generated agents land in the same matchable positions as eventual real-world participants, and Cosolvent can route them consistently. Schema conformance doesn't replicate a participant's business judgement or negotiation history — but it does ensure the synthetic population inhabits the right corners of the market's structure.

The schema is not just a filtering tool. It is the connective tissue of the entire platform: it makes the two-slot retrieval architecture coherent, grounds synthetic simulation in the real vocabulary of the market, and — as described in the companion piece — provides the structured foundation on which schema-aware participant matching and deal-specific scenario generation become possible.

---

*CommonContext is the domain knowledge component of DeeperPoint's marketplace toolkit. This article covers the schema architecture that makes domain-specific retrieval reliable. A companion piece covers how that same schema enables Cosolvent's matching engine and a generative tool that helps matched participants open their first conversation. The theoretical case for authoritative information as a market engineering intervention is in the [DeeperPoint whitepaper](../whitepaper.html).*
