# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.

"""
Market Catalog Build Script for DeeperPoint

Reads structured YAML scenario files from catalog/scenarios/ and generates:
  - catalog/index.html   : filterable catalog index (hidden, no nav link)
  - catalog/<id>.html    : detail page per scenario (three-panel layout)

The catalog is intentionally hidden: no navigation links point to it from
the main site. It is accessible at /catalog/ for direct-URL visitors only.
Search engines are excluded via robots.txt.

Usage:
    python scripts/build_catalog.py

YAML schema for each scenario file:
    id, title, sector, sub_sector, forge_tier, status, tags
    market_example: {summary, dominant_forces, deeperpoint_fit, economic_upside}
    sponsor_opportunities: [{title, type, revenue_model, strategic_logic}]
    story: {title, status, blog_slug, characters, summary}
"""

import html
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SITE_ROOT = Path(__file__).resolve().parent.parent
SCENARIOS_DIR = SITE_ROOT / "catalog" / "scenarios"
CATALOG_OUT = SITE_ROOT / "catalog"
SITE_URL = "https://deeperpoint.com"

FORGE_TIER_LABELS = {1: "Tier 1 — Simple", 2: "Tier 2 — Moderate", 3: "Tier 3 — Complex"}
FORGE_TIER_COLORS = {1: "#22c55e", 2: "#f59e0b", 3: "#ec4899"}

STORY_STATUS_LABELS = {
    "published": "Published",
    "draft": "Draft",
    "none": "Not yet written",
}

# ---------------------------------------------------------------------------
# Shared page chrome (matches build_blog.py style)
# ---------------------------------------------------------------------------

PAGE_HEAD = """<!-- Copyright (c) 2026 Mustafa Uzumeri. All rights reserved. -->
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>{title} — DeeperPoint Lab</title>
  <meta name="description" content="{description}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700&display=swap"
    rel="stylesheet">
  <link rel="stylesheet" href="{css_path}">
  <style>
    /* ---- Catalog-specific styles ---- */
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
      max-width: 600px; margin: 0 auto 2rem; line-height: 1.65;
    }

    /* ---- Filters ---- */
    .cat-filters {
      display: flex; flex-wrap: wrap; gap: .5rem;
      justify-content: center; margin-bottom: 2.5rem;
    }
    .cat-filter-btn {
      padding: 4px 14px; border-radius: 20px; border: 1px solid rgba(99,102,241,.35);
      background: transparent; color: var(--color-text-secondary, #cbd5e1);
      font-size: .78rem; font-weight: 500; cursor: pointer;
      transition: background .15s, color .15s, border-color .15s;
    }
    .cat-filter-btn:hover,
    .cat-filter-btn.active {
      background: rgba(99,102,241,.2); border-color: #6366f1; color: #c7d2fe;
    }
    .cat-filter-btn--tier { border-color: rgba(245,158,11,.35); color: #fcd34d; }
    .cat-filter-btn--tier:hover,
    .cat-filter-btn--tier.active { background: rgba(245,158,11,.15); border-color: #f59e0b; }

    /* ---- Grid ---- */
    .cat-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.25rem;
      margin-bottom: 4rem;
    }

    /* ---- Scenario card ---- */
    .scenario-card {
      background: rgba(15,23,42,.6);
      border: 1px solid rgba(99,102,241,.2);
      border-radius: 16px; padding: 1.4rem 1.5rem;
      text-decoration: none; color: inherit;
      display: block;
      transition: transform .2s, box-shadow .2s, border-color .2s;
      cursor: pointer;
    }
    .scenario-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 12px 40px rgba(99,102,241,.18);
      border-color: rgba(99,102,241,.45);
    }
    .scenario-card__top {
      display: flex; align-items: flex-start;
      justify-content: space-between; gap: .5rem;
      margin-bottom: .75rem;
    }
    .scenario-card__sector {
      font-size: .65rem; font-weight: 700; letter-spacing: .1em;
      text-transform: uppercase; color: #818cf8;
    }
    .scenario-card__tier {
      font-size: .65rem; font-weight: 700; letter-spacing: .08em;
      text-transform: uppercase; padding: 2px 8px; border-radius: 10px;
      white-space: nowrap;
    }
    .scenario-card__title {
      font-size: 1.05rem; font-weight: 700;
      color: var(--color-text-primary, #f1f5f9);
      line-height: 1.35; margin-bottom: .5rem;
    }
    .scenario-card__summary {
      font-size: .82rem; color: var(--color-text-secondary, #cbd5e1);
      line-height: 1.55; margin-bottom: 1rem;
    }
    .scenario-card__tags {
      display: flex; flex-wrap: wrap; gap: .3rem;
      margin-bottom: .75rem;
    }
    .scenario-card__tag {
      font-size: .65rem; font-weight: 600; letter-spacing: .06em;
      text-transform: uppercase;
      padding: 2px 7px; border-radius: 8px;
      background: rgba(99,102,241,.12);
      border: 1px solid rgba(99,102,241,.2);
      color: #a5b4fc;
    }
    .scenario-card__footer {
      display: flex; align-items: center; gap: .75rem;
      font-size: .75rem; color: var(--color-text-muted, #94a3b8);
    }
    .scenario-card__story-dot {
      width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
    }

    /* ---- Hidden class for filtering ---- */
    .scenario-card--hidden { display: none; }

    /* ---- Detail page ---- */
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
      font-size: 2rem; font-weight: 700;
      color: var(--color-text-primary, #f1f5f9);
      line-height: 1.25; margin-bottom: .75rem;
    }
    .detail-meta {
      display: flex; flex-wrap: wrap; gap: .5rem;
      align-items: center; margin-bottom: 2rem;
    }

    /* ---- Tab navigation ---- */
    .tab-nav {
      display: flex; gap: 0; border-bottom: 1px solid rgba(99,102,241,.25);
      margin-bottom: 2rem; overflow-x: auto;
    }
    .tab-btn {
      padding: .65rem 1.5rem; font-size: .85rem; font-weight: 600;
      background: transparent; border: none; border-bottom: 2px solid transparent;
      color: var(--color-text-muted, #94a3b8); cursor: pointer;
      transition: color .15s, border-color .15s; white-space: nowrap;
      margin-bottom: -1px;
    }
    .tab-btn:hover { color: var(--color-text-secondary, #cbd5e1); }
    .tab-btn.active {
      color: #a5b4fc; border-bottom-color: #6366f1;
    }
    .tab-panel { display: none; }
    .tab-panel.active { display: block; }

    /* ---- Panel content ---- */
    .panel-section {
      background: rgba(15,23,42,.5);
      border: 1px solid rgba(99,102,241,.15);
      border-radius: 12px; padding: 1.5rem 1.75rem;
      margin-bottom: 1.25rem;
    }
    .panel-section__label {
      font-size: .68rem; font-weight: 700; letter-spacing: .12em;
      text-transform: uppercase; color: #818cf8; margin-bottom: .6rem;
    }
    .panel-section__title {
      font-size: 1.05rem; font-weight: 700;
      color: var(--color-text-primary, #f1f5f9);
      margin-bottom: .75rem;
    }
    .panel-section p {
      font-size: .88rem; color: var(--color-text-secondary, #cbd5e1);
      line-height: 1.65; margin-bottom: .75rem;
    }
    .panel-section p:last-child { margin-bottom: 0; }

    .force-list {
      list-style: none; padding: 0; margin: 0;
      display: flex; flex-direction: column; gap: .4rem;
    }
    .force-list li {
      font-size: .85rem; color: var(--color-text-secondary, #cbd5e1);
      display: flex; align-items: flex-start; gap: .5rem;
    }
    .force-list li::before {
      content: "\26A1"; font-size: .7rem; margin-top: 3px; flex-shrink: 0;
    }

    .opp-card {
      border: 1px solid rgba(99,102,241,.2);
      border-radius: 10px; padding: 1.1rem 1.25rem;
      margin-bottom: .85rem; background: rgba(99,102,241,.05);
    }
    .opp-card__title {
      font-size: .92rem; font-weight: 700;
      color: var(--color-text-primary, #f1f5f9); margin-bottom: .4rem;
    }
    .opp-card__type {
      font-size: .65rem; font-weight: 700; letter-spacing: .1em;
      text-transform: uppercase; color: #f59e0b; margin-bottom: .5rem;
    }
    .opp-card p {
      font-size: .83rem; color: var(--color-text-secondary, #cbd5e1);
      line-height: 1.55; margin-bottom: .4rem;
    }
    .opp-card p:last-child { margin-bottom: 0; }
    .opp-card__revenue {
      font-size: .8rem; font-weight: 600;
      color: #4ade80; margin-top: .5rem;
    }

    .story-placeholder {
      text-align: center; padding: 3rem 1.5rem;
      color: var(--color-text-muted, #94a3b8);
    }
    .story-placeholder__icon { font-size: 2.5rem; margin-bottom: 1rem; }
    .story-cta {
      display: inline-flex; align-items: center; gap: .5rem;
      margin-top: 1.25rem; padding: .5rem 1.25rem;
      border-radius: 20px; border: 1px solid rgba(99,102,241,.4);
      color: #818cf8; text-decoration: none; font-size: .85rem;
      font-weight: 600; transition: background .15s;
    }
    .story-cta:hover { background: rgba(99,102,241,.15); }

    /* ---- Count badge ---- */
    .cat-count {
      text-align: center; font-size: .82rem;
      color: var(--color-text-muted, #94a3b8);
      margin-bottom: 1.5rem;
    }
    #visible-count { font-weight: 700; color: #a5b4fc; }
  </style>
</head>

<body>

  <!-- Animated Background -->
  <div class="bg-mesh" aria-hidden="true">
    <div class="bg-mesh__orb bg-mesh__orb--1"></div>
    <div class="bg-mesh__orb bg-mesh__orb--2"></div>
    <div class="bg-mesh__orb bg-mesh__orb--3"></div>
  </div>

  <!-- Minimal nav (no catalog link exposed) -->
  <nav class="nav" id="nav">
    <div class="nav__inner">
      <a href="{root}index.html" class="nav__logo">Deeper<span>Point</span></a>
      <ul class="nav__links">
        <li><a href="{root}index.html" class="nav__link">Home</a></li>
        <li><a href="{root}thin-markets.html" class="nav__link">The Problem</a></li>
        <li><a href="{root}marketforge.html" class="nav__link">The Project</a></li>
        <li><a href="{root}examples.html" class="nav__link">Examples</a></li>
        <li><a href="{root}blog/index.html" class="nav__link">Blog</a></li>
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

  <script src="{root}reveal.js"></script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# YAML Loading
# ---------------------------------------------------------------------------


def loadScenarios():
    """Load and return all published scenario YAML files as a list of dicts."""
    if not SCENARIOS_DIR.exists():
        print(f"  Creating scenarios directory: {SCENARIOS_DIR}")
        SCENARIOS_DIR.mkdir(parents=True, exist_ok=True)
        return []

    scenarios = []
    for f in sorted(SCENARIOS_DIR.glob("*.yaml")):
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
            if data.get("status") == "published":
                scenarios.append(data)
                print(f"  Loaded: {f.name}")
            else:
                print(f"  Skipped (draft): {f.name}")
        except Exception as e:
            print(f"  ERROR loading {f.name}: {e}")
    return scenarios


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def tierBadge(tier):
    color = FORGE_TIER_COLORS.get(tier, "#94a3b8")
    label = {1: "Tier 1", 2: "Tier 2", 3: "Tier 3"}.get(tier, f"Tier {tier}")
    return (
        f'<span class="scenario-card__tier" '
        f'style="background:rgba(0,0,0,.25); color:{color}; border:1px solid {color}44;">'
        f"{label}</span>"
    )


def storyDot(story):
    """Return a colored dot indicating story status."""
    status = story.get("status", "none") if story else "none"
    colors = {"published": "#4ade80", "draft": "#f59e0b", "none": "#475569"}
    labels = {"published": "Story published", "draft": "Story in draft", "none": "No story yet"}
    color = colors.get(status, "#475569")
    label = labels.get(status, "Unknown")
    return (
        f'<span class="scenario-card__story-dot" '
        f'style="background:{color};" title="{html.escape(label)}"></span>'
        f'<span>{label}</span>'
    )


def escHtml(text):
    return html.escape(str(text)) if text else ""


# ---------------------------------------------------------------------------
# Catalog Index Page
# ---------------------------------------------------------------------------


def buildIndexPage(scenarios):
    """Generate the catalog index page with JS filtering."""
    sectors = sorted({s.get("sector", "other") for s in scenarios})

    sector_btns = '<button class="cat-filter-btn active" data-filter="sector" data-value="all">All Sectors</button>\n'
    for sec in sectors:
        label = sec.replace("-", " ").title()
        sector_btns += (
            f'<button class="cat-filter-btn" data-filter="sector" data-value="{escHtml(sec)}">'
            f"{escHtml(label)}</button>\n"
        )

    tier_btns = '<button class="cat-filter-btn cat-filter-btn--tier active" data-filter="tier" data-value="all">All Tiers</button>\n'
    for t in [1, 2, 3]:
        tier_btns += (
            f'<button class="cat-filter-btn cat-filter-btn--tier" data-filter="tier" data-value="{t}">'
            f"Tier {t}</button>\n"
        )

    cards_html = ""
    for s in scenarios:
        sid = escHtml(s.get("id", ""))
        title = escHtml(s.get("title", "Untitled"))
        sector = s.get("sector", "other")
        sector_label = sector.replace("-", " ").title()
        tier = s.get("forge_tier", 2)
        summary = escHtml(s.get("market_example", {}).get("summary", ""))
        tags = s.get("tags", [])
        story = s.get("story", {})
        sponsor_count = len(s.get("sponsor_opportunities", []))

        tags_html = "".join(
            f'<span class="scenario-card__tag">{escHtml(t)}</span>' for t in tags
        )
        story_html = storyDot(story)

        cards_html += f"""
        <a href="{sid}.html" class="scenario-card reveal"
           data-sector="{escHtml(sector)}"
           data-tier="{tier}"
           data-tags="{escHtml(' '.join(tags))}">
          <div class="scenario-card__top">
            <div class="scenario-card__sector">{escHtml(sector_label)}</div>
            {tierBadge(tier)}
          </div>
          <div class="scenario-card__title">{title}</div>
          <div class="scenario-card__summary">{summary}</div>
          <div class="scenario-card__tags">{tags_html}</div>
          <div class="scenario-card__footer">
            {story_html}
            <span style="margin-left:auto">{sponsor_count} sponsor opp{"s" if sponsor_count != 1 else ""}</span>
          </div>
        </a>"""

    filter_script = """
  <script>
    (function () {
      const cards = Array.from(document.querySelectorAll('.scenario-card'));
      const countEl = document.getElementById('visible-count');
      const totalEl = document.getElementById('total-count');
      if (totalEl) totalEl.textContent = cards.length;

      let activeSector = 'all';
      let activeTier = 'all';

      function applyFilters() {
        let visible = 0;
        cards.forEach(card => {
          const secMatch = activeSector === 'all' || card.dataset.sector === activeSector;
          const tierMatch = activeTier === 'all' || card.dataset.tier === activeTier;
          if (secMatch && tierMatch) { card.classList.remove('scenario-card--hidden'); visible++; }
          else { card.classList.add('scenario-card--hidden'); }
        });
        if (countEl) countEl.textContent = visible;
      }

      document.querySelectorAll('[data-filter]').forEach(btn => {
        btn.addEventListener('click', () => {
          const filter = btn.dataset.filter;
          const value = btn.dataset.value;
          if (filter === 'sector') {
            activeSector = value;
            document.querySelectorAll('[data-filter="sector"]').forEach(b => b.classList.remove('active'));
          } else if (filter === 'tier') {
            activeTier = value;
            document.querySelectorAll('[data-filter="tier"]').forEach(b => b.classList.remove('active'));
          }
          btn.classList.add('active');
          applyFilters();
        });
      });

      applyFilters();
    })();
  </script>"""

    total = len(scenarios)
    head = PAGE_HEAD.format(
        title="Market Catalog — Lab",
        description="DeeperPoint thin market scenario catalog. Internal use.",
        css_path="../styles.css",
        root="../",
    )

    content = f"""
  <section class="section cat-header" id="catalog-index">
    <div class="container">
      <div class="cat-label">&#128300; Lab \u2014 Internal Catalog</div>
      <h1 class="cat-title">Market Scenario Catalog</h1>
      <p class="cat-desc">
        Thin market opportunities analyzed through the DeeperPoint framework.
        Each entry includes a market analysis, sponsor revenue opportunities, and a story.
      </p>

      <div class="cat-filters">
        <div style="width:100%; text-align:center; font-size:.7rem; color:#64748b; margin-bottom:.3rem; letter-spacing:.08em; text-transform:uppercase;">Filter by Sector</div>
        {sector_btns}
      </div>
      <div class="cat-filters" style="margin-top:-.75rem;">
        <div style="width:100%; text-align:center; font-size:.7rem; color:#64748b; margin-bottom:.3rem; letter-spacing:.08em; text-transform:uppercase;">Filter by Forge Tier</div>
        {tier_btns}
      </div>

      <div class="cat-count">
        Showing <span id="visible-count">{total}</span> of <span id="total-count">{total}</span> scenarios
      </div>

      <div class="cat-grid">
        {cards_html}
      </div>
    </div>
  </section>
{filter_script}
"""
    footer = PAGE_FOOTER.format(root="../")
    return head + content + footer


# ---------------------------------------------------------------------------
# Detail Page
# ---------------------------------------------------------------------------


def buildDetailPage(s):
    """Generate the detail page for a single scenario."""
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
        tab2 = '<div class="panel-section"><p>No sponsor opportunities documented yet.</p></div>'

    story_status = story.get("status", "none") if story else "none"
    if story_status == "published" and story.get("blog_slug"):
        blog_url = f"../../blog/{story['blog_slug']}.html"
        tab3 = f"""
      <div class="panel-section">
        <div class="panel-section__label">Narrative Story</div>
        <div class="panel-section__title">{escHtml(story.get('title', ''))}</div>
        <p>{escHtml(story.get('summary', ''))}</p>
        {'<p><strong>Characters:</strong> ' + escHtml(', '.join(story.get('characters', []))) + '</p>' if story.get('characters') else ''}
        <a href="{blog_url}" class="story-cta">Read on the blog &rarr;</a>
      </div>"""
    elif story_status == "draft":
        tab3 = f"""
      <div class="panel-section">
        <div class="panel-section__label">Story \u2014 Draft</div>
        <div class="panel-section__title">{escHtml(story.get('title', 'Draft in progress'))}</div>
        <p>{escHtml(story.get('summary', ''))}</p>
        {'<p><strong>Characters:</strong> ' + escHtml(', '.join(story.get('characters', []))) + '</p>' if story.get('characters') else ''}
        <p style="color:#f59e0b; font-size:.82rem;">&#9998; This story is in draft. Publish it via the /story-post workflow.</p>
      </div>"""
    else:
        tab3 = f"""
      <div class="story-placeholder">
        <div class="story-placeholder__icon">&#128221;</div>
        <p>No story written yet for this scenario.</p>
        <p style="font-size:.8rem;">Use the <code>/story-post</code> workflow to generate a narrative for this market.</p>
        <a href="../index.html" class="story-cta">&larr; Back to catalog</a>
      </div>"""

    head = PAGE_HEAD.format(
        title=title,
        description=escHtml(me.get("summary", "")),
        css_path="../../styles.css",
        root="../../",
    )

    content = f"""
  <section class="section" id="scenario-detail" style="padding-top: calc(var(--space-4xl, 4rem) + 60px);">
    <div class="container container--narrow">
      <a href="../index.html" class="detail-back">&larr; Catalog</a>
      <div class="detail-label">{escHtml(sector)} &middot; {escHtml(sub_sector)}</div>
      <h1 class="detail-title">{title}</h1>
      <div class="detail-meta">
        {tierBadge(tier)}
        {tags_html}
      </div>

      <nav class="tab-nav" role="tablist">
        <button class="tab-btn active" role="tab" data-tab="market">&#128200; Market Analysis</button>
        <button class="tab-btn" role="tab" data-tab="sponsor">&#128181; Sponsor Opportunities</button>
        <button class="tab-btn" role="tab" data-tab="story">&#128214; Story</button>
      </nav>

      <div id="tab-market" class="tab-panel active">{tab1}</div>
      <div id="tab-sponsor" class="tab-panel">{tab2}</div>
      <div id="tab-story" class="tab-panel">{tab3}</div>
    </div>
  </section>

  <script>
    (function () {{
      const btns = document.querySelectorAll('.tab-btn');
      const panels = document.querySelectorAll('.tab-panel');
      btns.forEach(btn => {{
        btn.addEventListener('click', () => {{
          btns.forEach(b => b.classList.remove('active'));
          panels.forEach(p => p.classList.remove('active'));
          btn.classList.add('active');
          document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
        }});
      }});
    }})();
  </script>
"""
    footer = PAGE_FOOTER.format(root="../../")
    return head + content + footer


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
        out_path = CATALOG_OUT / f"{sid}.html"
        out_path.write_text(page_html, encoding="utf-8")
        print(f"  Wrote: catalog/{sid}.html")

    print(f"Catalog build complete. {len(scenarios)} scenarios published.")
    print(f"  Access at: {SITE_URL}/catalog/")


if __name__ == "__main__":
    main()
