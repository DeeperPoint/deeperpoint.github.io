# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.

"""
Market Catalog Build Script for DeeperPoint  v2

Changes from v1:
  - Stories are self-contained in each YAML scenario file (story.body, markdown format).
    Blog publication is optional: story.blog_slug is only set when the user explicitly
    promotes the story to the blog via a separate workflow.
  - Catalog index page has full-text search + multi-select sector/tag dropdowns
    + tier buttons, designed to handle 20–300+ entries without degrading UX.

YAML schema for each scenario file:
    id, title, sector, sub_sector, forge_tier, status, tags
    card_title: "Short scan-friendly title for the index card (≤60 chars, 1 line ideal)"
    hidden: true        <- optional; suppresses the scenario from the catalog without deleting the YAML
    market_example:
      summary:          <- CARD ABSTRACT: ~40–60 words. One tight paragraph that names the thin market
                           problem and the matching solution. NOT a full problem description.
                           Treat it like a caption, not an intro — the full problem goes in 'problem'.
      problem, dominant_forces, deeperpoint_fit, economic_upside
    sponsor_opportunities: [{title, type, revenue_model, strategic_logic, recurring}]  # sponsor or investor opportunities
    story:
      title, status (none|draft|published), summary, characters
      body: |          <- inline markdown story (all three acts)
      blog_slug: ...   <- optional; only set when promoted to blog

Usage:
    python scripts/build_catalog.py
"""

import html
from pathlib import Path

import markdown as mdlib
import yaml

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SITE_ROOT = Path(__file__).resolve().parent.parent
SCENARIOS_DIR = SITE_ROOT / "catalog" / "scenarios"
CATALOG_OUT = SITE_ROOT / "catalog"
SITE_URL = "https://deeperpoint.com"

FORGE_TIER_COLORS = {1: "#22c55e", 2: "#f59e0b", 3: "#ec4899"}
FORGE_TIER_LABELS = {1: "Easy", 2: "Moderate", 3: "Complex"}

# ---------------------------------------------------------------------------
# Shared page chrome
# __TOKEN__ substitution avoids CSS brace conflicts with str.format()
# ---------------------------------------------------------------------------

PAGE_HEAD = """<!-- Copyright (c) 2026 Mustafa Uzumeri. All rights reserved. -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__TITLE__ \u2014 DeeperPoint</title>
  <meta name="description" content="__DESCRIPTION__">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="__CSS_PATH__">
  <style>
    /* --- Header --- */
    .cat-header {
      padding-top: calc(var(--space-4xl, 4rem) + 60px);
      padding-bottom: var(--space-2xl, 2rem);
      text-align: center;
    }
    .cat-label {
      font-size: .68rem; font-weight: 700; letter-spacing: .14em;
      text-transform: uppercase; color: #f59e0b; margin-bottom: .5rem;
    }
    .cat-title {
      font-size: 2.2rem; font-weight: 700;
      color: var(--color-text-primary, #f1f5f9); margin-bottom: .75rem;
    }
    .cat-desc {
      font-size: .95rem; color: var(--color-text-secondary, #cbd5e1);
      max-width: 820px; margin: 0 auto 2rem; padding: 0 1.5rem; line-height: 1.65;
    }

    /* --- Search bar --- */
    .cat-search-wrap {
      position: relative; max-width: 580px; margin: 0 auto 1.25rem;
    }
    .cat-search-icon {
      position: absolute; left: .85rem; top: 50%; transform: translateY(-50%);
      color: #475569; font-size: 1rem; pointer-events: none;
    }
    .cat-search {
      width: 100%; padding: .65rem 1rem .65rem 2.6rem;
      background: rgba(15,23,42,.7); border: 1px solid rgba(99,102,241,.3);
      border-radius: 8px; color: #f1f5f9; font-size: .9rem; font-family: inherit;
      transition: border-color .15s, box-shadow .15s;
      box-sizing: border-box;
    }
    .cat-search::placeholder { color: #475569; }
    .cat-search:focus {
      outline: none; border-color: #6366f1;
      box-shadow: 0 0 0 3px rgba(99,102,241,.15);
    }

    /* --- Filter row --- */
    .filter-row {
      display: flex; flex-wrap: wrap; gap: .6rem;
      justify-content: center; align-items: flex-start;
      margin-bottom: .75rem;
    }

    /* --- Custom dropdown (fdd) --- */
    .fdd { position: relative; }
    .fdd__btn {
      display: inline-flex; align-items: center; gap: .5rem;
      padding: .45rem 1rem; border-radius: 8px;
      border: 1px solid rgba(99,102,241,.35);
      background: rgba(15,23,42,.6); color: #cbd5e1;
      font-size: .8rem; font-weight: 500; cursor: pointer;
      transition: background .15s, border-color .15s;
      font-family: inherit; white-space: nowrap;
    }
    .fdd__btn:hover, .fdd--open .fdd__btn {
      background: rgba(99,102,241,.15); border-color: #6366f1; color: #c7d2fe;
    }
    .fdd__arrow { font-size: .6rem; transition: transform .15s; }
    .fdd--open .fdd__arrow { transform: rotate(180deg); }
    .fdd__panel {
      display: none; position: absolute; top: calc(100% + 6px); left: 0;
      z-index: 200; min-width: 260px; max-width: 340px;
      background: #1e293b; border: 1px solid rgba(99,102,241,.35);
      border-radius: 10px; overflow: hidden;
      box-shadow: 0 12px 40px rgba(0,0,0,.4);
    }
    .fdd--open .fdd__panel { display: block; }
    .fdd__search-wrap { padding: .5rem .6rem; border-bottom: 1px solid rgba(99,102,241,.15); }
    .fdd__search {
      width: 100%; padding: .35rem .6rem;
      background: rgba(15,23,42,.7); border: 1px solid rgba(99,102,241,.25);
      border-radius: 6px; color: #f1f5f9; font-size: .78rem; font-family: inherit;
      box-sizing: border-box;
    }
    .fdd__search:focus { outline: none; border-color: #6366f1; }
    .fdd__list { max-height: 240px; overflow-y: auto; padding: .35rem 0; }
    .fdd__item {
      display: flex; align-items: center; gap: .6rem;
      padding: .45rem .85rem; cursor: pointer;
      font-size: .8rem; color: #cbd5e1; text-align: left;
      transition: background .1s;
    }
    .fdd__item:hover { background: rgba(99,102,241,.12); }
    .fdd__item input[type=checkbox] { accent-color: #6366f1; width: 14px; height: 14px; flex-shrink: 0; }
    .fdd__count {
      padding: .35rem .85rem .5rem;
      font-size: .68rem; color: #64748b; border-top: 1px solid rgba(99,102,241,.1);
    }

    /* --- Tier buttons (in filter row) --- */
    .tier-btns { display: inline-flex; border-radius: 8px; overflow: hidden; border: 1px solid rgba(245,158,11,.35); }
    .tier-btn {
      padding: .45rem .85rem; font-size: .78rem; font-weight: 600;
      background: transparent; border: none; border-right: 1px solid rgba(245,158,11,.25);
      color: #fcd34d; cursor: pointer; font-family: inherit;
      transition: background .15s;
    }
    .tier-btn:last-child { border-right: none; }
    .tier-btn:hover { background: rgba(245,158,11,.1); }
    .tier-btn.active { background: rgba(245,158,11,.2); color: #f59e0b; }

    /* --- Clear all button --- */
    .btn-clear {
      padding: .45rem 1rem; border-radius: 8px;
      border: 1px solid rgba(239,68,68,.35);
      background: transparent; color: #fca5a5;
      font-size: .78rem; font-weight: 600; cursor: pointer;
      font-family: inherit; transition: background .15s;
      display: none;
    }
    .btn-clear:hover { background: rgba(239,68,68,.12); }

    /* --- Active filter chips --- */
    .filter-chips {
      display: flex; flex-wrap: wrap; gap: .35rem;
      justify-content: center; min-height: 0; margin-bottom: .75rem;
    }
    .filter-chip {
      display: inline-flex; align-items: center; gap: .35rem;
      padding: 3px 10px 3px 10px;
      background: rgba(99,102,241,.18); border: 1px solid rgba(99,102,241,.35);
      border-radius: 20px; font-size: .72rem; color: #c7d2fe; font-weight: 500;
    }
    .filter-chip__x {
      background: none; border: none; color: #818cf8;
      font-size: .85rem; cursor: pointer; padding: 0; line-height: 1;
      font-family: inherit;
    }
    .filter-chip__x:hover { color: #fca5a5; }

    /* --- Count --- */
    .cat-count {
      text-align: center; font-size: .82rem;
      color: var(--color-text-muted, #94a3b8);
      margin-bottom: 1.5rem;
    }
    #visible-count { font-weight: 700; color: #a5b4fc; }

    /* --- Grid --- */
    .cat-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.25rem; margin-bottom: 4rem;
    }
    .cat-grid--empty {
      grid-column: 1 / -1; text-align: center;
      padding: 3rem 1rem; color: #64748b;
    }

    /* --- Scenario card --- */
    .scenario-card {
      background: rgba(15,23,42,.6); border: 1px solid rgba(99,102,241,.2);
      border-radius: 16px; padding: 1.4rem 1.5rem;
      text-decoration: none; color: inherit; display: block;
      transition: transform .2s, box-shadow .2s, border-color .2s; cursor: pointer;
    }
    .scenario-card:hover {
      transform: translateY(-3px); box-shadow: 0 12px 40px rgba(99,102,241,.18);
      border-color: rgba(99,102,241,.45);
    }
    .scenario-card--hidden { display: none; }
    .scenario-card__top {
      display: flex; align-items: flex-start;
      justify-content: space-between; gap: .5rem; margin-bottom: .75rem;
    }
    .scenario-card__sector {
      font-size: .65rem; font-weight: 700; letter-spacing: .1em;
      text-transform: uppercase; color: #818cf8;
    }
    .scenario-card__tier {
      font-size: .65rem; font-weight: 700; letter-spacing: .08em;
      text-transform: uppercase; padding: 2px 8px; border-radius: 10px; white-space: nowrap;
    }
    .scenario-card__title {
      font-size: 1.05rem; font-weight: 700; color: var(--color-text-primary, #f1f5f9);
      line-height: 1.35; margin-bottom: .5rem;
    }
    .scenario-card__summary {
      font-size: .82rem; color: var(--color-text-secondary, #cbd5e1);
      line-height: 1.55; margin-bottom: 1rem;
    }
    .scenario-card__tags { display: flex; flex-wrap: wrap; gap: .3rem; margin-bottom: .75rem; }
    .scenario-card__tag {
      font-size: .65rem; font-weight: 600; letter-spacing: .06em; text-transform: uppercase;
      padding: 2px 7px; border-radius: 8px; background: rgba(99,102,241,.12);
      border: 1px solid rgba(99,102,241,.2); color: #a5b4fc;
    }
    .scenario-card__footer {
      display: flex; align-items: center; gap: .75rem;
      font-size: .75rem; color: var(--color-text-muted, #94a3b8);
    }
    .scenario-card__story-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

    /* --- Detail page --- */
    .detail-back {
      display: inline-flex; align-items: center; gap: 6px;
      font-size: .82rem; color: #818cf8; text-decoration: none;
      margin-bottom: var(--space-xl, 2rem); transition: color .15s;
    }
    .detail-back:hover { color: #a5b4fc; }
    .detail-label {
      font-size: .68rem; font-weight: 700; letter-spacing: .14em;
      text-transform: uppercase; color: #818cf8; margin-bottom: .4rem;
    }
    .detail-title {
      font-size: 2rem; font-weight: 700; color: var(--color-text-primary, #f1f5f9);
      line-height: 1.25; margin-bottom: .75rem;
    }
    .detail-meta { display: flex; flex-wrap: wrap; gap: .5rem; align-items: center; margin-bottom: 2rem; }

    /* --- Tabs --- */
    .tab-nav {
      display: flex; gap: 0; border-bottom: 1px solid rgba(99,102,241,.25);
      margin-bottom: 2rem;
    }
    .tab-btn {
      padding: .65rem 1.5rem; font-size: .85rem; font-weight: 600;
      background: transparent; border: none; border-bottom: 2px solid transparent;
      color: var(--color-text-muted, #94a3b8); cursor: pointer;
      transition: color .15s, border-color .15s; white-space: nowrap; margin-bottom: -1px;
      font-family: inherit;
    }
    .tab-btn:hover { color: var(--color-text-secondary, #cbd5e1); }
    .tab-btn.active { color: #a5b4fc; border-bottom-color: #6366f1; }
    .tab-panel { display: none; }
    .tab-panel.active { display: block; }

    /* --- Panel sections --- */
    .panel-section {
      background: rgba(15,23,42,.5); border: 1px solid rgba(99,102,241,.15);
      border-radius: 12px; padding: 1.5rem 1.75rem; margin-bottom: 1.25rem;
    }
    .panel-section__label {
      font-size: .68rem; font-weight: 700; letter-spacing: .12em;
      text-transform: uppercase; color: #818cf8; margin-bottom: .6rem;
    }
    .panel-section__title {
      font-size: 1.05rem; font-weight: 700; color: var(--color-text-primary, #f1f5f9); margin-bottom: .75rem;
    }
    .panel-section p {
      font-size: .88rem; color: var(--color-text-secondary, #cbd5e1);
      line-height: 1.65; margin-bottom: .75rem;
    }
    .panel-section p:last-child { margin-bottom: 0; }
    .force-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: .4rem; }
    .force-list li {
      font-size: .85rem; color: var(--color-text-secondary, #cbd5e1);
      line-height: 1.6; padding: .4rem .85rem;
      border-left: 2px solid rgba(6,182,212,.35);
      background: rgba(6,182,212,.03);
      border-radius: 0 6px 6px 0;
    }

    /* --- Sponsor opportunity card --- */
    .opp-card {
      border: 1px solid rgba(99,102,241,.2); border-radius: 10px; padding: 1.1rem 1.25rem;
      margin-bottom: .85rem; background: rgba(99,102,241,.05);
    }
    .opp-card__title {
      font-size: .92rem; font-weight: 700; color: var(--color-text-primary, #f1f5f9); margin-bottom: .4rem;
    }
    .opp-card__type {
      font-size: .65rem; font-weight: 700; letter-spacing: .1em;
      text-transform: uppercase; color: #f59e0b; margin-bottom: .5rem;
    }
    .opp-card p { font-size: .83rem; color: var(--color-text-secondary, #cbd5e1); line-height: 1.55; margin-bottom: .4rem; }
    .opp-card p:last-child { margin-bottom: 0; }
    .opp-card__revenue { font-size: .8rem; font-weight: 600; color: #4ade80; margin-top: .5rem; }

    /* --- Inline story body (rendered markdown) --- */
    .story-body { font-size: .9rem; line-height: 1.7; color: var(--color-text-secondary, #cbd5e1); }
    .story-body h2 {
      font-size: 1.05rem; font-weight: 700; color: #a5b4fc;
      margin: 2rem 0 .75rem; letter-spacing: .02em;
    }
    .story-body h2:first-child { margin-top: 0; }
    .story-body p { margin-bottom: 1rem; }
    .story-body p:last-child { margin-bottom: 0; }
    .story-body strong { color: var(--color-text-primary, #f1f5f9); font-weight: 600; }
    .story-body em { color: #c7d2fe; font-style: italic; }
    .story-body hr {
      border: none; border-top: 1px solid rgba(99,102,241,.2); margin: 1.75rem 0;
    }
    .story-body a { color: #818cf8; text-decoration: underline; text-decoration-color: rgba(129,140,248,.35); }
    .story-body a:hover { color: #a5b4fc; }
    .story-body ul { padding-left: 1.25rem; margin-bottom: 1rem; }
    .story-body li { margin-bottom: .4rem; }
    .story-body blockquote {
      border-left: 3px solid rgba(99,102,241,.4); padding-left: 1rem;
      margin: 1rem 0; color: #94a3b8; font-style: italic;
    }
    .story-blog-link {
      display: inline-flex; align-items: center; gap: .5rem;
      margin-top: 1.5rem; padding: .5rem 1.25rem;
      border-radius: 20px; border: 1px solid rgba(99,102,241,.4);
      color: #818cf8; text-decoration: none; font-size: .82rem;
      font-weight: 600; transition: background .15s;
    }
    .story-blog-link:hover { background: rgba(99,102,241,.15); }

    /* --- Curated collections panel --- */
    .collections-panel {
      margin: 0 auto 1rem;
      max-width: 820px;
      padding: 0 1.5rem;
    }
    .collections-panel__label {
      font-size: .65rem; font-weight: 700; letter-spacing: .12em;
      text-transform: uppercase; color: #64748b;
      margin-bottom: .45rem; text-align: center;
    }
    .collections-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: .4rem;
    }
    .col-card {
      display: flex; align-items: center; gap: .5rem;
      padding: .45rem .7rem;
      background: rgba(15,23,42,.55);
      border: 1px solid rgba(99,102,241,.22);
      border-radius: 8px;
      cursor: pointer;
      transition: background .15s, border-color .15s;
      text-align: left;
    }
    .col-card:hover {
      background: rgba(99,102,241,.14);
      border-color: rgba(99,102,241,.5);
    }
    .col-card.active {
      background: rgba(99,102,241,.2);
      border-color: #6366f1;
    }
    .col-card__icon { font-size: .9rem; flex-shrink: 0; }
    .col-card__body { min-width: 0; }
    .col-card__name {
      font-size: .75rem; font-weight: 700;
      color: #c7d2fe; line-height: 1.2;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .col-card__count {
      font-size: .63rem; color: #64748b; line-height: 1;
    }
    @media (max-width: 540px) {
      .collections-grid { grid-template-columns: repeat(2, 1fr); }
    }

    /* --- Story placeholder --- */
    .story-placeholder {
      text-align: center; padding: 3rem 1.5rem; color: var(--color-text-muted, #94a3b8);
    }
    .story-placeholder__icon { font-size: 2.5rem; margin-bottom: 1rem; }
    .story-cta {
      display: inline-flex; align-items: center; gap: .5rem;
      margin-top: 1.25rem; padding: .5rem 1.25rem; border-radius: 20px;
      border: 1px solid rgba(99,102,241,.4); color: #818cf8; text-decoration: none;
      font-size: .85rem; font-weight: 600; transition: background .15s;
    }
    .story-cta:hover { background: rgba(99,102,241,.15); }
  </style>
</head>
<body>
  <div class="bg-mesh" aria-hidden="true">
    <div class="bg-mesh__orb bg-mesh__orb--1"></div>
    <div class="bg-mesh__orb bg-mesh__orb--2"></div>
    <div class="bg-mesh__orb bg-mesh__orb--3"></div>
  </div>
  <nav class="nav" id="nav">
    <div class="nav__inner">
      <a href="__ROOT__index.html" class="nav__logo">Deeper<span>Point</span></a>
      <button class="nav__toggle" id="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
        <span class="nav__toggle-bar"></span>
        <span class="nav__toggle-bar"></span>
        <span class="nav__toggle-bar"></span>
      </button>
      <ul class="nav__links">
        <li><a href="__ROOT__index.html" class="nav__link">Home</a></li>
        <li><a href="__ROOT__thin-markets.html" class="nav__link">The Problem</a></li>
        <li><a href="__ROOT__marketforge.html" class="nav__link">The Project</a></li>
        <li><a href="__ROOT__examples.html" class="nav__link nav__link--active">Examples</a></li>
        <li><a href="__ROOT__blog/index.html" class="nav__link">Blog</a></li>
        <li><a href="__ROOT__ebook.html" class="nav__link">Ebook</a></li>
        <li><a href="__ROOT__history.html" class="nav__link">About</a></li>
      </ul>
    </div>
  </nav>
"""

PAGE_FOOTER = """
  <footer class="footer">
    <div class="container">
      <div class="footer__inner">
        <div class="footer__copyright">
          &copy; 2026 Mustafa Uzumeri / DeeperPoint. All rights reserved.
          &nbsp;&mdash;&nbsp; <em style="color:#64748b">Lab catalog &mdash; internal use</em>
        </div>
      </div>
    </div>
  </footer>
  <script src="__ROOT__reveal.js"></script>
</body>
</html>
"""


def renderHead(title, description, css_path, root):
    """Substitute __TOKEN__ placeholders in PAGE_HEAD safely (avoids CSS brace conflicts)."""
    return (
        PAGE_HEAD
        .replace("__TITLE__", title)
        .replace("__DESCRIPTION__", description)
        .replace("__CSS_PATH__", css_path)
        .replace("__ROOT__", root)
    )


def renderFooter(root):
    """Substitute __ROOT__ in PAGE_FOOTER."""
    return PAGE_FOOTER.replace("__ROOT__", root)


# ---------------------------------------------------------------------------
# YAML loading
# ---------------------------------------------------------------------------


def loadScenarios():
    """Load and return all published, non-hidden scenario YAML files as a list of dicts.

    The returned list is interleaved by sector using round-robin so that cards from
    different sectors alternate across the grid rather than clustering alphabetically.
    """
    if not SCENARIOS_DIR.exists():
        SCENARIOS_DIR.mkdir(parents=True, exist_ok=True)
        return []
    scenarios = []
    for f in sorted(SCENARIOS_DIR.glob("*.yaml")):
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
            if data.get("hidden") is True:
                print(f"  Skipped (hidden): {f.name}")
            elif data.get("status") == "published":
                scenarios.append(data)
                print(f"  Loaded: {f.name}")
            else:
                print(f"  Skipped (draft): {f.name}")
        except Exception as e:
            print(f"  ERROR loading {f.name}: {e}")
    return roundRobinBySector(scenarios)


def roundRobinBySector(scenarios):
    """Interleave scenarios across sectors so no sector clusters in the grid.

    Sectors are ordered by their first appearance in the alphabetical file list
    (stable across builds). Within each sector, entries keep their original order.
    Returns a flat list that alternates sectors: s0[0], s1[0], s2[0], ..., s0[1], ...
    """
    from collections import defaultdict, OrderedDict
    buckets = OrderedDict()
    for s in scenarios:
        sec = s.get("sector", "other")
        if sec not in buckets:
            buckets[sec] = []
        buckets[sec].append(s)
    result = []
    queues = list(buckets.values())
    while any(q for q in queues):
        for q in queues:
            if q:
                result.append(q.pop(0))
    return result



# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def escHtml(text):
    """HTML-escape a value; return empty string for None."""
    return html.escape(str(text)) if text else ""


def markdownToHtml(text):
    """Convert a markdown string to HTML using python-markdown."""
    if not text:
        return ""
    return mdlib.markdown(str(text), extensions=["extra"])


def tierBadge(tier):
    """Render a coloured build-complexity badge span."""
    color = FORGE_TIER_COLORS.get(tier, "#94a3b8")
    label = FORGE_TIER_LABELS.get(tier, f"Tier {tier}")
    return (
        f'<span class="scenario-card__tier" '
        f'style="background:rgba(0,0,0,.25);color:{color};border:1px solid {color}44;">'
        f"{label}</span>"
    )


def storyDot(story):
    """Return coloured dot + label for story status."""
    status = story.get("status", "none") if story else "none"
    colors = {"published": "#4ade80", "draft": "#f59e0b", "none": "#475569"}
    labels = {"published": "Story included", "draft": "Story in draft", "none": "No story yet"}
    color = colors.get(status, "#475569")
    label = labels.get(status, "Unknown")
    return (
        f'<span class="scenario-card__story-dot" style="background:{color};" title="{html.escape(label)}"></span>'
        f"<span>{label}</span>"
    )


# ---------------------------------------------------------------------------
# Catalog Index Page  (search + multi-select filters)
# ---------------------------------------------------------------------------


def buildIndexPage(scenarios):
    """Generate the filterable catalog index page."""

    # Collect unique sectors and tags for filter controls
    sectors = sorted({s.get("sector", "other") for s in scenarios})
    all_tags = sorted({t for s in scenarios for t in s.get("tags", [])})

    # --- Sector dropdown options ---
    sector_options = ""
    for sec in sectors:
        label = sec.replace("-", " ").title()
        sector_options += (
            f'<label class="fdd__item">'
            f'<input type="checkbox" class="sector-cb" value="{escHtml(sec)}"> {escHtml(label)}'
            f"</label>\n"
        )

    # --- Tag dropdown options ---
    tag_options = ""
    for tag in all_tags:
        tag_options += (
            f'<label class="fdd__item">'
            f'<input type="checkbox" class="tag-cb" value="{escHtml(tag)}"> {escHtml(tag)}'
            f"</label>\n"
        )

    # --- Scenario cards ---
    cards_html = ""
    total = len(scenarios)
    for s in scenarios:
        sid = escHtml(s.get("id", ""))
        title = escHtml(s.get("title", "Untitled"))
        card_title = escHtml(s.get("card_title") or s.get("title", "Untitled"))
        sector = s.get("sector", "other")
        sector_label = sector.replace("-", " ").title()
        tier = s.get("forge_tier", 2)
        me = s.get("market_example", {})
        summary = escHtml(me.get("summary", ""))
        tags = s.get("tags", [])
        story = s.get("story", {})
        sponsor_count = len(s.get("sponsor_opportunities", []))
        # Search text: title + summary + tags (lowercased for client-side match)
        search_text = " ".join([s.get("title", ""), me.get("summary", ""), " ".join(tags)]).lower()
        tags_html = "".join(f'<span class="scenario-card__tag">{escHtml(t)}</span>' for t in tags)
        s_label = f"{sponsor_count} sponsor/investor opp" + ("s" if sponsor_count != 1 else "")
        cards_html += f"""
        <a href="{sid}.html" class="scenario-card reveal"
           data-sector="{escHtml(sector)}"
           data-tier="{tier}"
           data-tags="{escHtml(' '.join(tags))}"
           data-search="{escHtml(search_text)}">
          <div class="scenario-card__top">
            <div class="scenario-card__sector">{escHtml(sector_label)}</div>
            {tierBadge(tier)}
          </div>
          <div class="scenario-card__title">{card_title}</div>
          <div class="scenario-card__summary">{summary}</div>
          <div class="scenario-card__tags">{tags_html}</div>
          <div class="scenario-card__footer">
            {storyDot(story)}
            <span style="margin-left:auto">{s_label}</span>
          </div>
        </a>"""

    # --- Inline JS for search + filters ---
    filter_js = """
  <script>
  (function () {
    var cards = Array.from(document.querySelectorAll('.scenario-card'));
    var countEl = document.getElementById('visible-count');
    var chipsEl = document.getElementById('filter-chips');
    var clearBtn = document.getElementById('btn-clear');
    var totalEl = document.getElementById('total-count');
    if (totalEl) totalEl.textContent = cards.length;

    // -- State --
    var query = '';
    var activeSectors = {};
    var activeTags = {};
    var activeTier = 'all';

    // -- Core filter logic --
    function cardVisible(card) {
      if (query && card.dataset.search.indexOf(query) === -1) return false;
      var sec = card.dataset.sector;
      if (Object.keys(activeSectors).length && !activeSectors[sec]) return false;
      var cardTags = card.dataset.tags ? card.dataset.tags.split(' ') : [];
      if (Object.keys(activeTags).length) {
        var hit = false;
        for (var i = 0; i < cardTags.length; i++) { if (activeTags[cardTags[i]]) { hit = true; break; } }
        if (!hit) return false;
      }
      if (activeTier !== 'all' && card.dataset.tier !== activeTier) return false;
      return true;
    }

    function applyFilters() {
      var vis = 0;
      cards.forEach(function (c) {
        var show = cardVisible(c);
        c.classList.toggle('scenario-card--hidden', !show);
        if (show) vis++;
      });
      if (countEl) countEl.textContent = vis;
      renderChips();
      updateDropdownLabels();
    }

    // -- Chip rendering --
    function renderChips() {
      var chips = [];
      Object.keys(activeSectors).forEach(function (v) {
        chips.push({ type: 'sector', value: v, label: v.replace(/-/g, ' ') });
      });
      Object.keys(activeTags).forEach(function (v) {
        chips.push({ type: 'tag', value: v, label: v });
      });
      var tierLabels = {'1':'Easy','2':'Moderate','3':'Complex'};
      if (activeTier !== 'all') chips.push({ type: 'tier', value: activeTier, label: (tierLabels[activeTier] || ('Tier ' + activeTier)) });
      chipsEl.innerHTML = chips.map(function (c) {
        return '<span class="filter-chip" data-type="' + c.type + '" data-value="' + c.value + '">' +
          c.label + '<button class="filter-chip__x" title="Remove">&times;</button></span>';
      }).join('');
      chipsEl.querySelectorAll('.filter-chip__x').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var chip = btn.closest('.filter-chip');
          var t = chip.dataset.type, v = chip.dataset.value;
          if (t === 'sector') { delete activeSectors[v]; setCheckbox('.sector-cb', v, false); }
          if (t === 'tag')    { delete activeTags[v];    setCheckbox('.tag-cb', v, false); }
          if (t === 'tier')   { activeTier = 'all'; updateTierBtns(); }
          applyFilters();
        });
      });
      if (clearBtn) clearBtn.style.display = chips.length ? 'inline-flex' : 'none';
    }

    function updateDropdownLabels() {
      var secCount = Object.keys(activeSectors).length;
      var tagCount = Object.keys(activeTags).length;
      document.getElementById('sector-label').textContent = secCount ? 'Sectors (' + secCount + ')' : 'All Sectors';
      document.getElementById('tag-label').textContent    = tagCount ? 'Tags (' + tagCount + ')' : 'All Tags';
    }

    // -- Helpers --
    function setCheckbox(selector, value, checked) {
      document.querySelectorAll(selector).forEach(function (cb) {
        if (cb.value === value) cb.checked = checked;
      });
    }
    function updateTierBtns() {
      document.querySelectorAll('.tier-btn').forEach(function (b) {
        b.classList.toggle('active', b.dataset.value === activeTier);
      });
    }

    // -- Search --
    var searchInput = document.getElementById('cat-search');
    if (searchInput) {
      searchInput.addEventListener('input', function () {
        query = this.value.toLowerCase().trim();
        applyFilters();
      });
    }

    // -- Sector checkboxes --
    document.querySelectorAll('.sector-cb').forEach(function (cb) {
      cb.addEventListener('change', function () {
        if (this.checked) activeSectors[this.value] = true;
        else delete activeSectors[this.value];
        applyFilters();
      });
    });

    // -- Tag checkboxes --
    document.querySelectorAll('.tag-cb').forEach(function (cb) {
      cb.addEventListener('change', function () {
        if (this.checked) activeTags[this.value] = true;
        else delete activeTags[this.value];
        applyFilters();
      });
    });

    // -- Dropdown search boxes (filter visible items in panel) --
    document.querySelectorAll('.fdd__search').forEach(function (inp) {
      inp.addEventListener('input', function () {
        var q = this.value.toLowerCase();
        var panel = this.closest('.fdd__panel');
        panel.querySelectorAll('.fdd__item').forEach(function (item) {
          item.style.display = item.textContent.toLowerCase().includes(q) ? '' : 'none';
        });
      });
    });

    // -- Tier buttons --
    document.querySelectorAll('.tier-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        activeTier = this.dataset.value;
        updateTierBtns();
        applyFilters();
      });
    });

    // -- Clear all --
    if (clearBtn) {
      clearBtn.addEventListener('click', function () {
        query = ''; activeSectors = {}; activeTags = {}; activeTier = 'all';
        if (searchInput) searchInput.value = '';
        document.querySelectorAll('.sector-cb, .tag-cb').forEach(function (cb) { cb.checked = false; });
        updateTierBtns();
        applyFilters();
      });
    }

    // -- Dropdown toggle --
    document.querySelectorAll('.fdd__btn').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var fdd = btn.closest('.fdd');
        var isOpen = fdd.classList.contains('fdd--open');
        document.querySelectorAll('.fdd').forEach(function (f) { f.classList.remove('fdd--open'); });
        if (!isOpen) {
          fdd.classList.add('fdd--open');
          var si = fdd.querySelector('.fdd__search');
          if (si) setTimeout(function() { si.focus(); }, 50);
        }
      });
    });
    document.addEventListener('click', function () {
      document.querySelectorAll('.fdd').forEach(function (f) { f.classList.remove('fdd--open'); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') document.querySelectorAll('.fdd').forEach(function (f) { f.classList.remove('fdd--open'); });
    });

    // -- Select collection (curated preset) --
    window.selectCollection = function (sectors, tags, activeCardId) {
      query = ''; activeSectors = {}; activeTags = {}; activeTier = 'all';
      if (searchInput) searchInput.value = '';
      document.querySelectorAll('.sector-cb, .tag-cb').forEach(function (cb) { cb.checked = false; });
      updateTierBtns();
      sectors.forEach(function (s) {
        activeSectors[s] = true;
        setCheckbox('.sector-cb', s, true);
      });
      tags.forEach(function (t) {
        activeTags[t] = true;
        setCheckbox('.tag-cb', t, true);
      });
      document.querySelectorAll('.col-card').forEach(function (c) { c.classList.remove('active'); });
      var card = document.getElementById(activeCardId);
      if (card) card.classList.add('active');
      var countEl = document.querySelector('.cat-count');
      if (countEl) countEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      applyFilters();
    };

    applyFilters();
  })();
  </script>"""

    head = renderHead(
        title="Markets in Waiting \u2014 Scenarios for the MarketForge Opportunity Catalog",
        description="One hundred speculative thin market scenarios analyzed through the DeeperPoint framework. Each describes a market that could exist if the right matching infrastructure were built \u2014 with a market analysis, sponsor revenue model, and a narrative story illustrating how a match would work.",
        css_path="../styles.css",
        root="../",
    )

    content = f"""
  <section class="section cat-header" id="catalog-index">
    <div class="container">
      <div class="cat-label">&#128200; DeeperPoint &#8212; MarketForge Opportunity Catalog</div>
      <h1 class="cat-title">Markets in Waiting</h1>
      <p class="cat-desc">
        Each entry describes a thin market that could be transformed by the right matching
        infrastructure &#8212; but has not been yet. Individual scenarios are speculative and
        details can always be argued. The point is not any single entry: it is the sheer
        number of plausible opportunities across entirely different sectors, geographies, and
        participant types. That pattern is harder to dismiss than any one example. Browse by
        sector, tag, or build complexity, and see how many you find compelling.
      </p>

      <!-- Curated Collections -->
      <div class="collections-panel">
        <div class="collections-panel__label">&#128204; Browse by collection</div>
        <div class="collections-grid">
          <button class="col-card" id="col-education"
            onclick="selectCollection(['canadian-education'], [], 'col-education')"
            title="Canadian Education">
            <span class="col-card__icon">&#127891;</span>
            <span class="col-card__body">
              <span class="col-card__name">Canadian Education</span>
              <span class="col-card__count">10 scenarios</span>
            </span>
          </button>
          <button class="col-card" id="col-crossborder"
            onclick="selectCollection(['canadian-education'], ['cross-border'], 'col-crossborder')"
            title="Cross-Border Learning">
            <span class="col-card__icon">&#127758;</span>
            <span class="col-card__body">
              <span class="col-card__name">Cross-Border Learning</span>
              <span class="col-card__count">4 scenarios</span>
            </span>
          </button>
          <button class="col-card" id="col-developing"
            onclick="selectCollection(['developing-economy'], [], 'col-developing')"
            title="Developing Economies">
            <span class="col-card__icon">&#127807;</span>
            <span class="col-card__body">
              <span class="col-card__name">Developing Economies</span>
              <span class="col-card__count">10 scenarios</span>
            </span>
          </button>
          <button class="col-card" id="col-manufacturing"
            onclick="selectCollection(['manufacturing'], [], 'col-manufacturing')"
            title="Manufacturing &amp; Trades">
            <span class="col-card__icon">&#9881;&#65039;</span>
            <span class="col-card__body">
              <span class="col-card__name">Manufacturing &amp; Trades</span>
              <span class="col-card__count">12 scenarios</span>
            </span>
          </button>
          <button class="col-card" id="col-social"
            onclick="selectCollection(['social-enterprise'], [], 'col-social')"
            title="Social Enterprise">
            <span class="col-card__icon">&#129309;</span>
            <span class="col-card__body">
              <span class="col-card__name">Social Enterprise</span>
              <span class="col-card__count">10 scenarios</span>
            </span>
          </button>
          <button class="col-card" id="col-realestate"
            onclick="selectCollection(['construction','real-estate-assembly'], [], 'col-realestate')"
            title="Real Estate &amp; Construction">
            <span class="col-card__icon">&#127959;&#65039;</span>
            <span class="col-card__body">
              <span class="col-card__name">Real Estate &amp; Build</span>
              <span class="col-card__count">15 scenarios</span>
            </span>
          </button>
        </div>
      </div>

      <!-- Search -->
      <div class="cat-search-wrap">
        <span class="cat-search-icon">&#128269;</span>
        <input id="cat-search" class="cat-search" type="search"
               placeholder="Search by title, summary, or tag&hellip;" autocomplete="off">
      </div>

      <!-- Filter row -->
      <div class="filter-row">

        <!-- Sector multi-select dropdown -->
        <div class="fdd" id="fdd-sector">
          <button class="fdd__btn" type="button" aria-haspopup="listbox">
            <span id="sector-label">All Sectors</span>
            <span class="fdd__arrow">&#9660;</span>
          </button>
          <div class="fdd__panel">
            <div class="fdd__search-wrap">
              <input class="fdd__search" type="search" placeholder="Filter sectors&hellip;" autocomplete="off">
            </div>
            <div class="fdd__list">
              {sector_options}
            </div>
            <div class="fdd__count">{len(sectors)} sector{'s' if len(sectors) != 1 else ''}</div>
          </div>
        </div>

        <!-- Tag multi-select dropdown -->
        <div class="fdd" id="fdd-tag">
          <button class="fdd__btn" type="button" aria-haspopup="listbox">
            <span id="tag-label">All Tags</span>
            <span class="fdd__arrow">&#9660;</span>
          </button>
          <div class="fdd__panel">
            <div class="fdd__search-wrap">
              <input class="fdd__search" type="search" placeholder="Filter tags&hellip;" autocomplete="off">
            </div>
            <div class="fdd__list">
              {tag_options}
            </div>
            <div class="fdd__count">{len(all_tags)} unique tag{'s' if len(all_tags) != 1 else ''}</div>
          </div>
        </div>

        <!-- Build Complexity buttons -->
        <div class="tier-btns" role="group" aria-label="Filter by build complexity">
          <button class="tier-btn active" data-value="all">All</button>
          <button class="tier-btn" data-value="1" title="Easy (~30–60 hrs to prototype)">Easy</button>
          <button class="tier-btn" data-value="2" title="Moderate (~72–144 hrs to prototype)">Moderate</button>
          <button class="tier-btn" data-value="3" title="Complex (~156–356 hrs to prototype)">Complex</button>
        </div>

        <!-- Clear all -->
        <button class="btn-clear" id="btn-clear" type="button">&#10005; Clear filters</button>
      </div>

      <!-- Active filter chips -->
      <div class="filter-chips" id="filter-chips"></div>

      <!-- Count -->
      <div class="cat-count">
        Showing <span id="visible-count">{total}</span> of <span id="total-count">{total}</span> scenarios
      </div>

      <!-- Grid -->
      <div class="cat-grid">
        {cards_html}
        <div class="cat-grid--empty" id="no-results" style="display:none">No scenarios match your filters.</div>
      </div>
    </div>
  </section>
{filter_js}
"""
    return head + content + renderFooter(root="../")


# ---------------------------------------------------------------------------
# Detail Page
# ---------------------------------------------------------------------------


def buildDetailPage(s):
    """Generate the three-tab detail page for a single scenario."""
    sid = s.get("id", "unknown")
    title = escHtml(s.get("title", "Untitled"))
    sector = s.get("sector", "other").replace("-", " ").title()
    sub_sector = escHtml(s.get("sub_sector", ""))
    tier = s.get("forge_tier", 2)
    tags = s.get("tags", [])
    me = s.get("market_example", {})
    opps = s.get("sponsor_opportunities", [])
    story = s.get("story", {})

    tags_html = "".join(f'<span class="blog-tag">{escHtml(t)}</span>' for t in tags)

    # --- Tab 1: Market Example ---
    forces = me.get("dominant_forces", [])
    forces_html = "".join(f"<li>{escHtml(f)}</li>" for f in forces)
    tab1 = f"""
      <div class="panel-section">
        <div class="panel-section__label">The Thin Market Problem</div>
        <p>{escHtml(me.get('problem', me.get('summary', '')))}</p>
      </div>
      <div class="panel-section">
        <div class="panel-section__label">Dominant Forces</div>
        <ul class="force-list">{forces_html}</ul>
      </div>
      <div class="panel-section">
        <div class="panel-section__label">How DeeperPoint Helps</div>
        <p>{escHtml(me.get('deeperpoint_fit', ''))}</p>
      </div>
      <div class="panel-section">
        <div class="panel-section__label">Economic Upside</div>
        <p>{escHtml(me.get('economic_upside', ''))}</p>
      </div>"""

    # --- Tab 2: Sponsor Opportunities ---
    if opps:
        opps_html = ""
        for opp in opps:
            opp_type = opp.get("type", "").replace("-", " ").title()
            opps_html += f"""
      <div class="opp-card">
        <div class="opp-card__type">{escHtml(opp_type)}</div>
        <div class="opp-card__title">{escHtml(opp.get('title', ''))}</div>
        <p>{escHtml(opp.get('strategic_logic', ''))}</p>
        <div class="opp-card__revenue">&#128181; {escHtml(opp.get('revenue_model', ''))}</div>
      </div>"""
        tab2 = opps_html
    else:
        tab2 = '<div class="panel-section"><p>No sponsor or investor opportunities documented yet.</p></div>'

    # --- Tab 3: Story (self-contained inline) ---
    story_status = story.get("status", "none") if story else "none"
    story_body_md = story.get("body", "") if story else ""
    story_blog_slug = story.get("blog_slug", "") if story else ""
    chars = story.get("characters", []) if story else []
    chars_html = f"<p><strong>Characters:</strong> {escHtml(', '.join(chars))}</p>" if chars else ""

    if story_body_md:
        # Render inline markdown story
        story_html_body = markdownToHtml(story_body_md)
        blog_link = ""
        if story_blog_slug:
            blog_url = f"../../blog/{story_blog_slug}.html"
            blog_link = f'<p style="margin-top:1.5rem"><a href="{blog_url}" class="story-blog-link">Also published on the blog &rarr;</a></p>'
        draft_banner = ""
        if story_status == "draft":
            draft_banner = '<p style="color:#f59e0b;font-size:.82rem;margin-bottom:1.25rem;">&#9998; This story is in draft.</p>'
        tab3 = f"""
      <div class="panel-section">
        <div class="panel-section__label">Narrative Story</div>
        <div class="panel-section__title">{escHtml(story.get('title', ''))}</div>
        {chars_html}
        {draft_banner}
        <div class="story-body">
          {story_html_body}
        </div>
        {blog_link}
      </div>"""
    elif story_status == "draft":
        tab3 = """
      <div class="story-placeholder">
        <div class="story-placeholder__icon">&#9998;</div>
        <p>Story draft in progress.</p>
        <a href="../index.html" class="story-cta">&larr; Back to catalog</a>
      </div>"""
    else:
        tab3 = """
      <div class="story-placeholder">
        <div class="story-placeholder__icon">&#128221;</div>
        <p>No story written yet for this scenario.</p>
        <p style="font-size:.8rem;">Add a <code>story.body</code> field to the scenario YAML to include a narrative.</p>
        <a href="../index.html" class="story-cta">&larr; Back to catalog</a>
      </div>"""

    head = renderHead(
        title=title,
        description=escHtml(me.get("summary", "")),
        css_path="../../styles.css",
        root="../../",
    )

    content = f"""
  <section class="section" id="scenario-detail" style="padding-top:calc(var(--space-4xl,4rem) + 60px);">
    <div class="container container--narrow">
      <a href="index.html" class="detail-back">&larr; Catalog</a>
      <div class="detail-label">{escHtml(sector)} &middot; {escHtml(sub_sector)}</div>
      <h1 class="detail-title">{title}</h1>
      <div class="detail-meta">
        {tierBadge(tier)}
        {tags_html}
      </div>
      <nav class="tab-nav" role="tablist">
        <button class="tab-btn active" role="tab" data-tab="market">&#128200; Market Analysis</button>
        <button class="tab-btn" role="tab" data-tab="story">&#128214; Story</button>
        <button class="tab-btn" role="tab" data-tab="sponsor">&#128181; Sponsor or Investor Opportunities</button>
      </nav>
      <div id="tab-market" class="tab-panel active">{tab1}</div>
      <div id="tab-story" class="tab-panel">{tab3}</div>
      <div id="tab-sponsor" class="tab-panel">{tab2}</div>
    </div>
  </section>
  <script>
    (function () {{
      var btns = document.querySelectorAll('.tab-btn');
      var panels = document.querySelectorAll('.tab-panel');
      btns.forEach(function (btn) {{
        btn.addEventListener('click', function () {{
          btns.forEach(function (b) {{ b.classList.remove('active'); }});
          panels.forEach(function (p) {{ p.classList.remove('active'); }});
          btn.classList.add('active');
          document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
        }});
      }});
    }})();
  </script>
"""
    return head + content + renderFooter(root="../../")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    """Build catalog index and all scenario detail pages."""
    print("Catalog build starting...")
    print(f"  Scenarios dir: {SCENARIOS_DIR}")
    print(f"  Output dir:    {CATALOG_OUT}")

    scenarios = loadScenarios()
    if not scenarios:
        print("  No published scenarios found. Creating output dir and exiting.")
        CATALOG_OUT.mkdir(parents=True, exist_ok=True)
        return

    CATALOG_OUT.mkdir(parents=True, exist_ok=True)

    index_html = buildIndexPage(scenarios)
    (CATALOG_OUT / "index.html").write_text(index_html, encoding="utf-8")
    print(f"  Wrote: catalog/index.html ({len(scenarios)} scenarios)")

    for s in scenarios:
        sid = s.get("id", "unknown")
        page_html = buildDetailPage(s)
        (CATALOG_OUT / f"{sid}.html").write_text(page_html, encoding="utf-8")
        print(f"  Wrote: catalog/{sid}.html")

    print(f"Catalog build complete. {len(scenarios)} scenarios published.")
    print(f"  Access at: {SITE_URL}/catalog/")


if __name__ == "__main__":
    main()
