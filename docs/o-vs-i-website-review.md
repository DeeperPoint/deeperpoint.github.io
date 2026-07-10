# O-vs-I Website Consistency Review

*Date: 2026-07-09. Companion to `DeeperPointWiki/O-vs-I-consistency-review.md`, which covers the canonical source docs. This record covers the published site (`deeperpoint.github.io`), extending the reframing that makes the **decision-unit axis (Organization vs. Individual)** primary and treats the B2B/B2C/C2B/C2C taxonomy as a familiar proxy for it.*

**Status: all edits applied and pushed on 2026-07-09.** Catalog and blog were excluded by instruction (legacy; they need not track every theory change).

## Litmus test

For each `B2B`/`B2C`/`C2C` reference: **structural/physics claim about organizational decision units → promote to `O2O`;** genuinely commercial subset, audience-facing register, or illustrative example → **keep**. This mirrors the canonical sweep, where FX/margin passages were deliberately left as B2B.

## Changes made

- **whitepaper.html** (web version of the whitepaper)
  - Removed the standalone "Business and Consumer Combinations" heading; folded its point into "Decision Units."
  - Rewrote the Decision Units opening to make O/I primary, and **added the O/I ↔ B/C 2×2 mapping table** (O2O≈B2B, O2I≈B2C, I2O≈C2B, I2I≈C2C).
  - Scope table out-of-scope cell: `C2C` → `I2I (the familiar C2C)`.
  - (Decision-Units prose, scope table in-scope cell, and the organizational-attenuation passage already used O2O.)

- **intervention-matrix.html** — two structural claims promoted to O2O (mirrors canonical `InterventionMatrix.md`):
  - Trust tooltip: "In B2B markets, trust has an additional dimension" → "In O2O and professional-services markets…"
  - AI-Intermediary/Opacity tooltip: "most destructive form of opacity in B2B markets" → "…in O2O markets."

- **market-diagnostic.html** (interactive diagnostic tool)
  - Participant-type dropdown reframed from B2B/B2C/C2C/C2B to **O2O / O2I / I2O / I2I**, each glossed with its familiar-taxonomy equivalent, plus a "classify by who holds the veto, not who hears the pitch" instruction.
  - Result JS updated: the "Good Fit for DeeperPoint Tools" branch now keys on `par === 'O2O'` and its text reads "(many-to-many, O2O)". (Verified `par` is consumed only in that one branch.)
  - EMU result text generalized: "Standard B2B matching tools are insufficient" → "Standard matching tools are insufficient."

- **about.html** — corrected the challenge count from **11 to 14** to match the current framework (`intervention-matrix.html` v4.0 = 10 endogenous + 4 exogenous). Updated the "three that can kill / eight that grind" split to "five … / nine …" and added the three missing challenges to the enumerated list: **Geopolitical & trade volatility** and **Macro & FX exposure** (existential), and **Technological obsolescence** (resistance). *(Not an O/I change — a separate theory-version drift noticed during the sweep and fixed on request.)*

## Deliberately left unchanged (litmus: commercial / audience register / example)

- **intervention-matrix.html** AI Risk Insulation tooltips ("insulates B2B transactions", currency collars, long-execution-window) — commercial FX/margin; the "B2B procurement" and "B2B data entry" tooltips — illustrative.
- **guide-\*.html** (accelerators, investors, associations, government) — "B2B economic growth", "B2B SaaS playbook", "international B2B trade": audience-facing marketing register, not physics claims.
- **marketmaps.html** — "complex B2B markets" (methodology description).
- **index.html**, **market-physics.html** — "consumer e-commerce" / "everyday consumer goods" as thick-market examples.

## Not affected

Core theory pages with no participant-taxonomy content — how-it-works, precis, architecture, platform, who-should-care, testbeds — had nothing to reconcile.
