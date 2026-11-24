---
description: Add one or more new entries to the MarketForge Opportunity Catalog and publish them to deeperpoint.com
---

# /add-catalog-entry — Complete Workflow

Use this workflow whenever adding new YAML scenario entries to the catalog.
It encodes all schema rules and the local build step. (Checked 2026-11-24: the
deploy Action now runs `build_catalog.py` as well, but the generated pages are
tracked in git, so build locally and commit them with the YAML.)

**Input:** `$ARGUMENTS` — the scenario(s) to add (a slug/topic or source doc); add-many is supported.

---

## Critical Rules (learned from past mistakes)

> [!CAUTION]
> Run `build_catalog.py` locally, then `python update_nav.py`, and commit the
> generated HTML with the YAML source. The builder writes its own navigation
> into every catalog page; `update_nav.py` puts the site's current navigation
> back. Skip it and about 250 existing pages show as modified.

| Mistake | Consequence | Prevention |
|---|---|---|
| YAML placed in `catalog/` root | File ignored silently; count stays the same | Always write to `catalog/scenarios/` |
| `status: draft` | File silently skipped; count stays the same | Use `status: published` |
| Using `vertical:` instead of `sector:` | Entry appears in catalog but in sector "other" | Use `sector:` — see valid values below |
| Not running `build_catalog.py` locally | Generated pages in git fall out of step with the YAML | Always run step 4 before committing |
| Not running `update_nav.py` after the build | Every existing catalog page shows as modified, with the builder's older navigation | Run it straight after the build |
| No `challenges:` line | The idea page has no "Challenges That Bind It" panel and the Home page box cannot match on it | Add two to four slugs from `cards/cards.json`, most binding first |

---

## Step 1 — Write the YAML file

**File location:** `catalog/scenarios/<id>.yaml`
**File naming:** Use the pattern `<sector-prefix>-<descriptive-slug>.yaml`

| Sector | Prefix convention |
|---|---|
| `manufacturing` | `mfg-` |
| `logistics` | `lgx-` |
| `construction` | `con-` |
| `canadian-food-last-stage` | `food-` |
| `municipal-government` | `muni-` |
| `real-estate-assembly` | `rea-` |
| `social-enterprise` | `svz-` |
| `canadian-sport` | `csport-` |
| `canadian-startup-ecosystem` | `cstartup-` |
| `canadian-defence-sector` | `cdef-` |
| `canadian-gov-expert-networks` | `cgov-` |
| `sme-service-consortium` | `sme-` |
| `ring-of-fire-hub` | `rof-` |
| `remote-town-renewal` | `rtr-` |
| `diaspora-connections` | `dia-` |
| `global-knowledge-equity` | `gke-` |
| `canadian-healthcare-support` | `chc-` |
| `canada-mexico-trade` | `cm-` |

---

## Step 2 — YAML Schema (complete)

Use this template exactly. Do not invent field names.

```yaml
# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.
id: <sector-prefix>-<slug>
title: "Full descriptive title"
card_title: "Short scan-friendly title (≤60 chars)"
sector: <value-from-table-above>          # NOT 'vertical:'
sub_sector: "Human-readable sub-category"
forge_tier: 1                             # 1=Easy, 2=Moderate, 3=Complex
status: published                         # NOT 'draft'
challenges: [slug, slug, slug]            # two to four slugs from cards/cards.json, most binding first (rubric: DeeperPointWiki/work/2026-11-24-catalog-tagging/rubric.md)
tags: [tag1, tag2, tag3]
# hidden: true                            # optional - suppresses without deleting

market_example:
  summary: "40–60 words. One tight paragraph naming the thin market problem
    and matching solution. This is the card abstract — treat it like a caption,
    not an intro. The detailed problem goes in 'problem'."
  problem: "Full problem description, multiple sentences."
  dominant_forces:
    - "Force 1 — brief explanation"
    - "Force 2 — brief explanation"
    - "Force 3 — brief explanation"
  deeperpoint_fit: "How CoSolvent, CommonContext, ClientSynth, and/or the
    Generative Match Story address the dominant forces."
  economic_upside: "Quantified opportunity — market size, transaction volume,
    platform revenue estimate."

sponsor_opportunities:
  - title: "Opportunity Title"
    type: saas                            # saas | managed-service | commerce-extension | logistics-extension
    revenue_model: "Rate, model, pricing range."
    strategic_logic: "Why a sponsor would fund this and why it's self-sustaining."
    recurring: true                       # true | false

  # Include 3–5 sponsor_opportunities per entry.
  # Aim for a mix of types: at least one saas, one managed-service,
  # and one commerce-extension or logistics-extension.

story:
  title: "Story Title"
  status: draft                           # none | draft | published
  blog_slug: ""                           # only set if promoted to blog; the entry page then links to the post and does not print this body
  characters:
    - "Name - role, location"
    - "Name - role, location"
  summary: "One-sentence story summary for the catalog detail page."
  body: |
    ## Act A - The Market Structure

    [Why the market is broken. No characters yet. Pure structural analysis.]

    ---

    ## Act B - The Story

    **Character A** ...

    **Character B** ...

    [The match happens. How the platform resolves the market failure.]

    ---

    ## Act C - Why This Market Stays Broken Without Infrastructure

    [Structural argument. What the platform does that no alternative can.
    Link to market-physics.html and marketforge.html.]

    *Characters are fictional. [Relevant domain facts] are real.
    [DeeperPoint](../marketforge.html) is building the infrastructure
    this story describes.*
```

---

## Step 3 — Validate the YAML

Run a quick check before building:

```powershell
# From deeperpoint.github.io root:
python -c "import yaml; yaml.safe_load(open('catalog/scenarios/<your-file>.yaml').read()); print('OK')"
```

If it prints `OK`, the YAML is well-formed. If it raises an error, fix the
indentation or quoting issue before proceeding.

---

## Step 4 — Build the catalog locally

```powershell
# From deeperpoint.github.io root:
python scripts/build_catalog.py
python update_nav.py
```

**Expected output of the build ends with:**
```
Catalog build complete. NNN scenarios published.
  Access at: https://deeperpoint.com/catalog/
```

Verify that NNN increased by the number of entries you added.
If any entries are skipped, the output will say `Skipped (draft): <file>`
or `Skipped (hidden): <file>` — fix accordingly.

---

## Step 5 — Commit and push

Both the YAML source files AND the generated HTML files must be committed together:

```powershell
git add catalog/scenarios/<your-new-entries>.yaml
git add catalog/<your-new-entries>.html
git add catalog/index.html
git commit -m "Add N new catalog entries: <brief description>"
git push
```

The `git add catalog/` shorthand is safe if you haven't touched other catalog HTML files,
but be explicit when in doubt to avoid accidentally staging unrelated changes.

---

## Valid `sector:` values

```
canada-mexico-trade
canadian-defence-sector
canadian-food-last-stage
canadian-gov-expert-networks
canadian-healthcare-support
canadian-sport
canadian-startup-ecosystem
construction
diaspora-connections
global-knowledge-equity
logistics
manufacturing
municipal-government
real-estate-assembly
remote-town-renewal
ring-of-fire-hub
sme-service-consortium
social-enterprise
```

The list above is partial (checked 2026-11-24). Sectors also in use, with their file prefixes:
`arts-cultural-markets` (art-), `canadian-agriculture` (cag-), `canadian-education` (edu-),
`canadian-energy` (cen-), `canadian-export` (export-), `canadian-financial-services` (cfs-),
`canadian-forestry` (for-), `canadian-justice-system` (cjs-), `canadian-natural-resources` (cnr-),
`canadian-research-institutions` (cri-), `developing-economy` (dev-),
`environmental-circular-economy` (eco-), `global-health-pharma` (ghp-), `pets-and-animals` (pet-),
`professional-services` (psvc-), `senior-expert-marketplace` (sem-), `talent-deep-match` (tdm-).
For the current list run `grep -h "^sector:" catalog/scenarios/*.yaml | sort | uniq -c`.

To add a new sector, use a lowercase hyphenated identifier. The builder will
display it title-cased in the sector filter dropdown automatically.

---

## Valid `sponsor_opportunities.type` values

```
saas
managed-service
commerce-extension
logistics-extension
```

---

## Valid `story.status` values

```
none        ← no story yet
draft       ← story written but not yet published to blog
published   ← story promoted to blog (blog_slug must be set)
```

Note: `story.status` is independent of the top-level `status` field.
The top-level `status: published` controls whether the catalog entry appears.
`story.status: draft` is fine — it just means the story hasn't been promoted
to the blog yet.

Since 2026-11-21 the site does not display `story.status`. The card label is
derived from content: "Full story on the blog" when `blog_slug` names a post,
"Short story included" when there is a `body`, and nothing otherwise.

---

## Notes

- Do **not** manually edit `catalog/index.html`. The builder regenerates it entirely.
- Do **not** commit the old `catalog/*.yaml` root-level files if they exist; they are
  ignored by the builder. The canonical location is `catalog/scenarios/`.
- The deploy Action builds the blog and the catalog on every push (checked 2026-11-24). The
  generated catalog pages are still tracked in git, so commit them.
- Research before writing. Every number, date, programme, law and company in an entry needs a
  source; do not estimate market size, prices or platform revenue. Say "would" for anything the
  engine does not do yet, and use "Content Match Story", not "Generative Match Story".
- Story links are relative to the catalog folder: `../market-physics.html`, `../marketforge.html`.
