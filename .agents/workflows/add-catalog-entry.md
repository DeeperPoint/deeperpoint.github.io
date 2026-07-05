---
description: Add one or more new entries to the MarketForge Opportunity Catalog and publish them to deeperpoint.com
---

# /add-catalog-entry — Complete Workflow

Use this workflow whenever adding new YAML scenario entries to the catalog.
It encodes all schema rules and the mandatory local build step that the
GitHub Action does NOT run automatically.

---

## Critical Rules (learned from past mistakes)

> [!CAUTION]
> The GitHub Action only runs `build_blog.py`. It does **not** run
> `build_catalog.py`. You MUST run the catalog builder locally and commit
> the generated HTML files along with the YAML source.

| Mistake | Consequence | Prevention |
|---|---|---|
| YAML placed in `catalog/` root | File ignored silently; count stays the same | Always write to `catalog/scenarios/` |
| `status: draft` | File silently skipped; count stays the same | Use `status: published` |
| Using `vertical:` instead of `sector:` | Entry appears in catalog but in sector "other" | Use `sector:` — see valid values below |
| Not running `build_catalog.py` locally | HTML never generated; site unchanged | Always run step 4 before committing |

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
  blog_slug: ""                           # only set if promoted to blog
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
    [DeeperPoint](../../marketforge.html) is building the infrastructure
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
```

**Expected output ends with:**
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

---

## Notes

- Do **not** manually edit `catalog/index.html`. The builder regenerates it entirely.
- Do **not** commit the old `catalog/*.yaml` root-level files if they exist; they are
  ignored by the builder. The canonical location is `catalog/scenarios/`.
- The GitHub Action rebuilds the blog but NOT the catalog. Any catalog changes
  pushed without running `build_catalog.py` locally will not appear on the live site.
