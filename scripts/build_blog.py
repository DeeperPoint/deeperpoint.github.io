# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.

"""
Blog Build Script for DeeperPoint

Reads Markdown posts from blog/posts/, converts them to HTML using the site's
design system, and generates a blog index page and RSS feed.

Supports optional series grouping via frontmatter fields:
    series:             (str)  slug identifying the series, e.g. "manufacturing-fractional"
    series-title:       (str)  human-readable name for the series
    series-position:    (int)  1-indexed position within the series
    series-description: (str)  one-paragraph blurb for the series landing page

Usage:
    python scripts/build_blog.py

Posts must have YAML frontmatter with: title, date, tags, summary, author, slug.
"""

import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

import markdown
import yaml

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SITE_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = SITE_ROOT / "blog" / "posts"
BLOG_OUT = SITE_ROOT / "blog"
SITE_URL = "https://deeperpoint.com"
FEED_TITLE = "DeeperPoint Blog"
FEED_DESC = "Thin market science, engineering, and the DeeperPoint ecosystem."

MD_EXTENSIONS = ["fenced_code", "tables", "toc", "smarty", "attr_list", "footnotes", "md_in_html"]

# ---------------------------------------------------------------------------
# Series Component Styles (injected inline for pages that use them)
# ---------------------------------------------------------------------------

SERIES_STYLES = """  <style>
    /* ---- Series index card ---- */
    .series-card {
      background: linear-gradient(135deg, rgba(99,102,241,.09) 0%, rgba(139,92,246,.05) 100%);
      border: 1px solid rgba(99,102,241,.25);
      border-left: 4px solid #6366f1;
      border-radius: 16px;
      padding: 1.5rem 1.75rem;
      display: block;
      text-decoration: none;
      color: inherit;
      margin-bottom: 1.25rem;
      transition: transform .2s, box-shadow .2s;
    }
    .series-card:hover { transform: translateY(-2px); box-shadow: 0 8px 32px rgba(99,102,241,.2); }
    .series-card__label {
      font-size: .68rem; font-weight: 700; letter-spacing: .12em;
      text-transform: uppercase; color: #818cf8; margin-bottom: .4rem;
    }
    .series-card__title {
      font-size: 1.15rem; font-weight: 700;
      color: var(--color-text-primary, #f1f5f9);
      margin-bottom: .35rem; line-height: 1.35;
    }
    .series-card__meta {
      font-size: .78rem; color: var(--color-text-muted, #94a3b8); margin-bottom: .9rem;
    }
    .series-card__summary {
      font-size: .85rem; color: var(--color-text-secondary, #cbd5e1);
      margin-bottom: 1rem; line-height: 1.55;
    }
    .series-posts-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: .4rem; }
    .series-posts-list__item { display: flex; align-items: flex-start; gap: .6rem; }
    .series-posts-list__num {
      flex-shrink: 0; width: 20px; height: 20px; border-radius: 50%;
      background: rgba(99,102,241,.2); border: 1px solid rgba(99,102,241,.4);
      color: #818cf8; font-size: .65rem; font-weight: 700;
      display: flex; align-items: center; justify-content: center; margin-top: 2px;
    }
    .series-posts-list__link {
      font-size: .84rem; color: var(--color-text-secondary, #cbd5e1);
      text-decoration: none; line-height: 1.45; transition: color .15s;
    }
    .series-posts-list__link:hover { color: #a5b4fc; }

    /* ---- Pinned badge ---- */
    .pinned-badge {
      display: inline-flex; align-items: center; gap: 5px;
      font-size: .65rem; font-weight: 700; letter-spacing: .1em;
      text-transform: uppercase; color: #f59e0b;
      background: rgba(245,158,11,.12); border: 1px solid rgba(245,158,11,.3);
      border-radius: 20px; padding: 2px 10px; margin-bottom: .6rem;
    }
    .series-card--pinned {
      border-left-color: #f59e0b;
      background: linear-gradient(135deg, rgba(245,158,11,.07) 0%, rgba(99,102,241,.05) 100%);
    }

    /* ---- Series nav bar (in-post) ---- */
    .series-nav {
      background: linear-gradient(135deg, rgba(99,102,241,.09) 0%, rgba(139,92,246,.05) 100%);
      border: 1px solid rgba(99,102,241,.25);
      border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 2.5rem;
    }
    .series-nav__header {
      font-size: .68rem; font-weight: 700; letter-spacing: .12em;
      text-transform: uppercase; color: #818cf8; margin-bottom: .5rem;
    }
    .series-nav__title { font-size: .95rem; font-weight: 600; color: var(--color-text-primary, #f1f5f9); margin-bottom: .85rem; }
    .series-nav__steps { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: .85rem; }
    .series-nav__step {
      display: flex; align-items: center; gap: 5px; padding: 3px 10px 3px 4px;
      border-radius: 20px; text-decoration: none; font-size: .76rem; font-weight: 500;
      border: 1px solid rgba(99,102,241,.28); color: var(--color-text-secondary, #cbd5e1);
      background: transparent; transition: background .15s, color .15s;
    }
    .series-nav__step:hover { background: rgba(99,102,241,.15); color: #a5b4fc; }
    .series-nav__step--current { background: rgba(99,102,241,.22); border-color: #6366f1; color: #c7d2fe; }
    .series-nav__step-num {
      width: 18px; height: 18px; border-radius: 50%; background: rgba(99,102,241,.25);
      display: flex; align-items: center; justify-content: center;
      font-size: .65rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;
    }
    .series-nav__step--current .series-nav__step-num { background: #6366f1; color: #fff; }
    .series-nav__arrows { display: flex; gap: 1.25rem; flex-wrap: wrap; }
    .series-nav__arrow { font-size: .8rem; color: #818cf8; text-decoration: none; display: flex; align-items: center; gap: 4px; }
    .series-nav__arrow:hover { color: #a5b4fc; }
  </style>
"""

SERIES_PAGE_STYLES = """  <style>
    /* ---- Series landing page ---- */
    .series-back {
      display: inline-flex; align-items: center; gap: 6px;
      font-size: .82rem; color: #818cf8; text-decoration: none;
      margin-bottom: var(--space-xl); transition: color .15s;
    }
    .series-back:hover { color: #a5b4fc; }
    .series-page__label {
      font-size: .68rem; font-weight: 700; letter-spacing: .12em;
      text-transform: uppercase; color: #818cf8; margin-bottom: .5rem;
    }
    .series-page__title {
      font-size: 2rem; font-weight: 700;
      color: var(--color-text-primary, #f1f5f9);
      line-height: 1.25; margin-bottom: 1rem;
    }
    .series-page__desc {
      font-size: 1rem; color: var(--color-text-secondary, #cbd5e1);
      line-height: 1.65; margin-bottom: var(--space-2xl);
      border-left: 3px solid rgba(99,102,241,.4); padding-left: 1rem;
    }
    .series-page__entries { list-style: none; padding: 0; margin: 0; }
    .series-entry {
      display: flex; gap: 1.25rem; align-items: flex-start;
      padding: 1.25rem 0; border-bottom: 1px solid rgba(99,102,241,.12);
      text-decoration: none; color: inherit;
      transition: background .15s;
    }
    .series-entry:last-child { border-bottom: none; }
    .series-entry__num {
      flex-shrink: 0; width: 36px; height: 36px; border-radius: 50%;
      background: linear-gradient(135deg, #6366f1, #8b5cf6);
      color: #fff; font-size: .78rem; font-weight: 700;
      display: flex; align-items: center; justify-content: center;
      margin-top: 3px;
    }
    .series-entry__body { flex: 1; }
    .series-entry__title {
      font-size: 1rem; font-weight: 600;
      color: var(--color-text-primary, #f1f5f9);
      margin-bottom: .3rem; line-height: 1.4; transition: color .15s;
    }
    .series-entry:hover .series-entry__title { color: #a5b4fc; }
    .series-entry__summary {
      font-size: .83rem; color: var(--color-text-secondary, #cbd5e1);
      line-height: 1.55; margin-bottom: .4rem;
    }
    .series-entry__meta {
      font-size: .75rem; color: var(--color-text-muted, #94a3b8);
    }
  </style>
"""

# ---------------------------------------------------------------------------
# Stream metadata
# ---------------------------------------------------------------------------

STREAM_LABELS = {
    "market-scenario": "Market Scenario",
    "workshop-notes":  "Workshop Notes",
    "engineers-log":   "Engineer\u2019s Log",
}

# (text-color, background, border)
STREAM_COLORS = {
    "market-scenario": ("#f59e0b", "rgba(245,158,11,.13)",  "rgba(245,158,11,.32)"),
    "workshop-notes":  ("#818cf8", "rgba(99,102,241,.12)",   "rgba(99,102,241,.32)"),
    "engineers-log":   ("#22d3ee", "rgba(6,182,212,.1)",     "rgba(6,182,212,.28)"),
    "other":           ("#64748b", "rgba(100,116,139,.1)",   "rgba(100,116,139,.25)"),
}

BLOG_INDEX_STYLES = """  <style>
    /* --- Stream filter tabs --- */
    .blog-stream-tabs {
      display: flex; gap: .4rem; margin-bottom: 1.75rem;
      flex-wrap: wrap; justify-content: center;
    }
    .blog-stream-tab {
      padding: .42rem 1.1rem; border-radius: 20px;
      border: 1px solid rgba(99,102,241,.3);
      background: transparent; color: #94a3b8;
      font-size: .8rem; font-weight: 600; cursor: pointer;
      font-family: inherit;
      transition: background .15s, color .15s, border-color .15s;
      white-space: nowrap;
    }
    .blog-stream-tab:hover {
      background: rgba(99,102,241,.12); color: #c7d2fe;
      border-color: rgba(99,102,241,.55);
    }
    .blog-stream-tab.active {
      background: rgba(99,102,241,.22); color: #a5b4fc;
      border-color: #6366f1;
    }
    .blog-stream-tab[data-stream="market-scenario"].active {
      background: rgba(245,158,11,.17); color: #fcd34d; border-color: #f59e0b;
    }
    .blog-stream-tab[data-stream="engineers-log"].active {
      background: rgba(6,182,212,.14); color: #67e8f9; border-color: #22d3ee;
    }
    /* --- Post count line --- */
    .blog-index-count {
      text-align: center; font-size: .82rem;
      color: #64748b; margin-bottom: 1.75rem;
    }
    #blog-post-count { font-weight: 700; color: #a5b4fc; }
    /* --- 2-column grid --- */
    .blog-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1.25rem;
      align-items: start;
    }
    @media (max-width: 740px) {
      .blog-grid { grid-template-columns: 1fr; }
    }
    /* --- Year divider (spans both columns) --- */
    .blog-year-heading {
      grid-column: 1 / -1;
      font-size: .68rem; font-weight: 700; letter-spacing: .15em;
      text-transform: uppercase; color: #475569;
      border-bottom: 1px solid rgba(99,102,241,.12);
      padding-bottom: .45rem; margin-top: 1rem;
    }
    .blog-year-heading:first-child { margin-top: 0; }
    /* --- Featured card (full-width, most recent in All view) --- */
    .blog-card--featured { grid-column: 1 / -1; }
    .blog-card--featured .blog-card__title { font-size: 1.3rem; }
    .series-card { grid-column: 1 / -1; }  /* series cards always full-width */
    /* --- Stream badge --- */
    .blog-stream-badge {
      font-size: .62rem; font-weight: 700; letter-spacing: .1em;
      text-transform: uppercase; padding: 2px 9px;
      border-radius: 10px; display: inline-block;
      margin-bottom: .6rem;
    }
    /* --- Tag filter strip --- */
    .blog-tag-strip {
      display: flex; flex-wrap: wrap; gap: .35rem;
      justify-content: center; margin-bottom: 1.25rem;
    }
    .blog-tag-pill {
      padding: 3px 11px; border-radius: 14px;
      border: 1px solid rgba(99,102,241,.22);
      background: transparent; color: #64748b;
      font-size: .72rem; font-weight: 600; cursor: pointer;
      font-family: inherit; letter-spacing: .04em;
      transition: background .12s, color .12s, border-color .12s;
      white-space: nowrap;
    }
    .blog-tag-pill:hover {
      background: rgba(99,102,241,.1); color: #a5b4fc;
      border-color: rgba(99,102,241,.45);
    }
    .blog-tag-pill.active {
      background: rgba(99,102,241,.2); color: #c7d2fe;
      border-color: #6366f1;
    }
    /* --- Hidden (JS-managed) --- */
    .blog-index-item--hidden { display: none !important; }
  </style>"""

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

PAGE_HEAD = """<!-- Copyright (c) 2026 Mustafa Uzumeri. All rights reserved. -->
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — DeeperPoint</title>
  <meta name="description" content="{description}">

  <!-- Open Graph -->
  <meta property="og:type" content="{og_type}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="DeeperPoint">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700&display=swap"
    rel="stylesheet">
  <link rel="stylesheet" href="{css_path}">
  <link rel="alternate" type="application/rss+xml" title="{feed_title}" href="{feed_url}">
{extra_styles}</head>

<body>

  <!-- Animated Background -->
  <div class="bg-mesh" aria-hidden="true">
    <div class="bg-mesh__orb bg-mesh__orb--1"></div>
    <div class="bg-mesh__orb bg-mesh__orb--2"></div>
    <div class="bg-mesh__orb bg-mesh__orb--3"></div>
  </div>

  <!-- Navigation -->
  <nav class="nav" id="nav">
    <div class="nav__inner">
      <a href="{root}index.html" class="nav__logo">Deeper<span>Point</span></a>
      <button class="nav__toggle" id="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
        <span class="nav__toggle-bar"></span>
        <span class="nav__toggle-bar"></span>
        <span class="nav__toggle-bar"></span>
      </button>
      <ul class="nav__links">
        <li><a href="{root}index.html" class="nav__link">Home</a></li>
        <li><a href="{root}thin-markets.html" class="nav__link">Theory</a></li>
        <li><a href="{root}intervention-matrix.html" class="nav__link">Matrix</a></li>
        <li><a href="{root}ebook.html" class="nav__link">Ebook</a></li>
        <li><a href="{root}catalog/index.html" class="nav__link">Catalog</a></li>
        <li><a href="{root}marketmaps.html" class="nav__link">MarketMaps</a></li>
        <li><a href="{root}cosolvent.html" class="nav__link">Cosolvent</a></li>
        <li><a href="{root}blog/index.html" class="nav__link{blog_active}">Blog</a></li>
        <li><a href="{root}about.html" class="nav__link">About</a></li>
      </ul>
    </div>
  </nav>
"""

PAGE_FOOTER = """
  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer__inner">
        <div class="footer__copyright">
          &copy; 2026 Mustafa Uzumeri / DeeperPoint. All rights reserved.
        </div>
        <ul class="footer__links">
          <li><a href="{root}search.html" class="footer__link">Search</a></li>
          <li><a href="https://deeperpoint.com" class="footer__link" target="_blank" rel="noopener">deeperpoint.com</a></li>
          <li><a href="https://github.com/DeeperPoint" class="footer__link" target="_blank" rel="noopener">GitHub</a></li>
        </ul>
      </div>
    </div>
  </footer>

  <script src="{root}reveal.js"></script>
  <script src="{root}nav-mobile.js"></script>
  <script data-goatcounter="https://deeperpoint.goatcounter.com/count"
          async src="//gc.zgo.at/count.js"></script>
</body>

</html>
"""

# ---------------------------------------------------------------------------
# Post Parsing
# ---------------------------------------------------------------------------


def parsePost(filepath):
    """Parse a Markdown file with YAML frontmatter. Returns (metadata, html_body)."""
    text = filepath.read_text(encoding="utf-8")

    # Split frontmatter from body
    match = re.search(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, flags=re.DOTALL | re.MULTILINE)
    if not match:
        print(f"  SKIP {filepath.name} — no YAML frontmatter")
        return None, None

    meta = yaml.safe_load(match.group(1))
    body_md = match.group(2)

    # Validate required fields
    required = ["title", "date", "tags", "summary", "slug"]
    missing = [f for f in required if f not in meta]
    if missing:
        print(f"  SKIP {filepath.name} — missing fields: {', '.join(missing)}")
        return None, None

    # Ensure date is a datetime.date
    if isinstance(meta["date"], str):
        meta["date"] = datetime.strptime(meta["date"], "%Y-%m-%d").date()

    # Convert Markdown to HTML
    md = markdown.Markdown(extensions=MD_EXTENSIONS)
    body_html = md.convert(body_md)

    # Estimate reading time
    word_count = len(body_md.split())
    meta["reading_time"] = max(1, round(word_count / 250))

    return meta, body_html


# ---------------------------------------------------------------------------
# Series Support
# ---------------------------------------------------------------------------


def buildSeriesIndex(posts):
    """
    Group posts that share a 'series' slug into a series index.

    Returns:
        dict mapping series_slug -> {
            "title":  human-readable series title,
            "posts":  list of meta dicts sorted by series-position then date,
            "date":   date of the most recent post (for index ordering),
        }
    """
    series = {}
    for meta in posts:
        slug = meta.get("series")
        if not slug:
            continue
        if slug not in series:
            series[slug] = {
                "title": meta.get("series-title", slug.replace("-", " ").title()),
                "description": meta.get("series-description", ""),
                "posts": [],
            }
        # Pick up series-description from any post that carries it
        if not series[slug]["description"] and meta.get("series-description"):
            series[slug]["description"] = meta["series-description"]
        # Pin the series if any post in it is pinned
        if meta.get("pinned"):
            series[slug]["pinned"] = True
            if meta.get("pin-label"):
                series[slug]["pin-label"] = meta["pin-label"]
        series[slug]["posts"].append(meta)

    for slug, data in series.items():
        data["posts"].sort(key=lambda p: (p.get("series-position", 999), p["date"]))
        # Use the most recent post's date to position the series card in the index
        data["date"] = max(p["date"] for p in data["posts"])

    return series


def buildSeriesNavHtml(current_meta, series_posts):
    """
    Build the in-post series navigation bar HTML.
    Appears between the post header and the article body.
    """
    series_title = current_meta.get(
        "series-title",
        current_meta.get("series", "").replace("-", " ").title(),
    )
    current_slug = current_meta["slug"]
    total = len(series_posts)

    # Build step pills
    steps_html = ""
    prev_post = None
    next_post = None
    for i, post in enumerate(series_posts):
        pos = post.get("series-position", i + 1)
        is_current = post["slug"] == current_slug
        if is_current:
            if i > 0:
                prev_post = series_posts[i - 1]
            if i < total - 1:
                next_post = series_posts[i + 1]
            steps_html += (
                f'<span class="series-nav__step series-nav__step--current" '
                f'aria-current="true">'
                f'<span class="series-nav__step-num">{pos}</span>'
                f"{_shortTitle(post['title'])}"
                f"</span>"
            )
        else:
            steps_html += (
                f'<a href="{post["slug"]}.html" class="series-nav__step">'
                f'<span class="series-nav__step-num">{pos}</span>'
                f"{_shortTitle(post['title'])}"
                f"</a>"
            )

    # Prev / Next arrows
    arrows_html = ""
    if prev_post:
        arrows_html += (
            f'<a href="{prev_post["slug"]}.html" class="series-nav__arrow">'
            f"&larr; {_shortTitle(prev_post['title'])}"
            f"</a>"
        )
    if next_post:
        arrows_html += (
            f'<a href="{next_post["slug"]}.html" class="series-nav__arrow">'
            f"{_shortTitle(next_post['title'])} &rarr;"
            f"</a>"
        )

    return f"""
      <div class="series-nav">
        <div class="series-nav__header">Part of a {total}-post series</div>
        <div class="series-nav__title">{series_title}</div>
        <div class="series-nav__steps">{steps_html}</div>
        {f'<div class="series-nav__arrows">{arrows_html}</div>' if arrows_html else ''}
      </div>"""


def buildSeriesCardHtml(series_slug, series_data, pinned=False, pin_label=None, stream="other"):
    """Build the series group card for the blog index page."""
    posts = series_data["posts"]
    total = len(posts)
    series_title = series_data["title"]
    year = str(series_data["date"].year)

    # Use series-description if available, otherwise first post's summary
    teaser = series_data.get("description") or posts[0].get("summary", "")

    # Build numbered post list
    items_html = ""
    for post in posts:
        pos = post.get("series-position", "\u00b7")
        items_html += (
            f'<li class="series-posts-list__item">'
            f'<span class="series-posts-list__num">{pos}</span>'
            f'<a href="{post["slug"]}.html" class="series-posts-list__link">{post["title"]}</a>'
            f"</li>"
        )

    series_page_url = f"series/{series_slug}.html"
    date_str = series_data["date"].strftime("%B %Y")
    pinned_class = " series-card--pinned" if pinned else ""
    badge_text = pin_label or "&#9733; Start Here"
    pinned_badge = f'<div class="pinned-badge">{badge_text}</div>' if pinned else ""

    stream_label = STREAM_LABELS.get(stream, "")
    if stream_label:
        color, bg, border = STREAM_COLORS.get(stream, STREAM_COLORS["other"])
        stream_badge = (
            f'<div class="blog-stream-badge" '
            f'style="color:{color};background:{bg};border:1px solid {border};">'
            f'{stream_label}</div>\n          '
        )
    else:
        stream_badge = ""

    # Union of all tags across the series posts
    series_tags = sorted({t for p in posts for t in p.get("tags", [])})
    tags_attr = " ".join(series_tags)

    return f"""
        <div class="series-card{pinned_class} reveal" id="series-{series_slug}"
             data-stream="{stream}" data-year="{year}" data-tags="{tags_attr}">
          {pinned_badge}{stream_badge}<div class="series-card__label">Series &middot; {total} parts &middot; {date_str}</div>
          <a href="{series_page_url}" class="series-card__title" style="text-decoration:none; color:inherit; display:block; margin-bottom:.35rem;">{series_title} &rarr;</a>
          <div class="series-card__summary">{teaser}</div>
          <ul class="series-posts-list">
            {items_html}
          </ul>
        </div>"""


def _shortTitle(full_title):
    """
    Produce a short display label from a full post title.
    Strips the 'Stream Label: ' prefix if present, then truncates to ~30 chars.
    """
    # Remove stream prefix (e.g. "Market Scenario: ", "Workshop Notes: ")
    if ": " in full_title:
        short = full_title.split(": ", 1)[1]
    else:
        short = full_title
    # Truncate
    if len(short) > 32:
        short = short[:30].rstrip() + "…"
    return short


def buildSeriesPage(series_slug, series_data):
    """Generate a standalone series landing page at blog/series/<slug>.html."""
    posts = series_data["posts"]
    series_title = series_data["title"]
    description = series_data.get("description") or posts[0].get("summary", "")
    total = len(posts)
    date_str = series_data["date"].strftime("%B %Y")

    entries_html = ""
    for post in posts:
        pos = post.get("series-position", "·")
        post_date = post["date"].strftime("%B %d, %Y")
        entries_html += f"""
          <li>
            <a href="../{post['slug']}.html" class="series-entry">
              <div class="series-entry__num">{pos}</div>
              <div class="series-entry__body">
                <div class="series-entry__title">{post['title']}</div>
                <div class="series-entry__summary">{post.get('summary', '')}</div>
                <div class="series-entry__meta">{post_date} &middot; {post.get('reading_time', '?')} min read</div>
              </div>
            </a>
          </li>"""

    head = PAGE_HEAD.format(
        title=series_title,
        description=description,
        og_type="website",
        url=f"{SITE_URL}/blog/series/{series_slug}.html",
        css_path="../../styles.css",
        feed_title=FEED_TITLE,
        feed_url=f"{SITE_URL}/blog/feed.xml",
        root="../../",
        blog_active=" nav__link--active",
        extra_styles=SERIES_PAGE_STYLES,
    )

    content = f"""
  <section class="section" id="series-page" style="padding-top: calc(var(--space-4xl) + 60px);">
    <div class="container container--narrow">
      <a href="../index.html" class="series-back">&larr; All Posts</a>
      <div class="series-page__label">Series &middot; {total} parts &middot; {date_str}</div>
      <h1 class="series-page__title">{series_title}</h1>
      <p class="series-page__desc">{description}</p>
      <ul class="series-page__entries">
        {entries_html}
      </ul>
    </div>
  </section>
"""

    footer = PAGE_FOOTER.format(root="../../")
    return head + content + footer


# ---------------------------------------------------------------------------
# Page Generation
# ---------------------------------------------------------------------------


def buildPostPage(meta, body_html, series_posts=None):
    """Generate a full HTML page for a single blog post."""
    date_str = meta["date"].strftime("%B %d, %Y")
    tags_html = "".join(
        f'<span class="blog-tag">{tag}</span>' for tag in meta["tags"]
    )

    # Inject series nav between the post header and the article body
    series_nav_html = ""
    if series_posts:
        series_nav_html = buildSeriesNavHtml(meta, series_posts)

    extra_styles = SERIES_STYLES if series_posts else ""

    head = PAGE_HEAD.format(
        title=meta["title"],
        description=meta["summary"],
        og_type="article",
        url=f"{SITE_URL}/blog/{meta['slug']}.html",
        css_path="../styles.css",
        feed_title=FEED_TITLE,
        feed_url=f"{SITE_URL}/blog/feed.xml",
        root="../",
        blog_active=" nav__link--active",
        extra_styles=extra_styles,
    )

    content = f"""
  <section class="section" id="blog-post" style="padding-top: calc(var(--space-4xl) + 60px);">
    <div class="container container--narrow">
      <div class="reveal">
        <a href="index.html" class="blog-back">&larr; All Posts</a>
        <div class="blog-meta">
          <time datetime="{meta['date'].isoformat()}">{date_str}</time>
          <span class="blog-meta__sep">&middot;</span>
          <span>{meta['reading_time']} min read</span>
        </div>
        <h1 class="blog-post__title">{meta['title']}</h1>
        <div class="blog-meta" style="margin-bottom: var(--space-2xl);">
          {tags_html}
        </div>
      </div>
      {series_nav_html}
      <article class="blog-post">
        {body_html}
      </article>
    </div>
  </section>
"""

    footer = PAGE_FOOTER.format(root="../")

    return head + content + footer


def buildPostCardHtml(meta, stream="other", is_featured=False):
    """Build a standalone post card for the blog index."""
    date_str = meta["date"].strftime("%B %d, %Y")
    year = str(meta["date"].year)
    tags_html = "".join(
        f'<span class="blog-tag">{tag}</span>' for tag in meta["tags"]
    )
    featured_class = " blog-card--featured" if is_featured else ""
    stream_label = STREAM_LABELS.get(stream, "")
    if stream_label:
        color, bg, border = STREAM_COLORS.get(stream, STREAM_COLORS["other"])
        badge_html = (
            f'<div class="blog-stream-badge" '
            f'style="color:{color};background:{bg};border:1px solid {border};">'
            f'{stream_label}</div>\n          '
        )
    else:
        badge_html = ""
    tags_attr = " ".join(meta.get("tags", []))
    return f"""
        <a href="{meta['slug']}.html"
           class="blog-card card reveal{featured_class}"
           data-stream="{stream}" data-year="{year}" data-tags="{tags_attr}">
          {badge_html}<div class="blog-meta">
            <time datetime="{meta['date'].isoformat()}">{date_str}</time>
            <span class="blog-meta__sep">&middot;</span>
            <span>{meta['reading_time']} min read</span>
          </div>
          <h3 class="blog-card__title">{meta['title']}</h3>
          <p class="blog-card__summary">{meta['summary']}</p>
          <div class="blog-meta">{tags_html}</div>
        </a>"""


def detectStream(meta):
    """Detect stream slug from frontmatter 'stream' field or title prefix."""
    s = meta.get("stream", "")
    if s in STREAM_LABELS:
        return s
    title = meta.get("title", "")
    if title.startswith("Market Scenario:"):
        return "market-scenario"
    if title.startswith("Workshop Notes:"):
        return "workshop-notes"
    if title.startswith("Engineer\u2019s Log:") or title.startswith("Engineer's Log:"):
        return "engineers-log"
    return "other"


def detectSeriesStream(series_data):
    """Detect the dominant stream for a series from its posts."""
    streams = [detectStream(p) for p in series_data["posts"]]
    if not streams:
        return "other"
    return Counter(streams).most_common(1)[0][0]


def buildIndexPage(posts, series_index):
    """
    Generate the blog listing page.

    Features:
    - Stream filter tabs: All / Market Scenario / Workshop Notes / Engineer's Log
    - Year-divider headings spanning both grid columns
    - 2-column responsive card grid
    - Featured (full-width) card for the most recent post in "All" view
    """
    extra_styles = (SERIES_STYLES if series_index else "") + BLOG_INDEX_STYLES
    head = PAGE_HEAD.format(
        title="Blog",
        description="Thin market science, engineering, and the DeeperPoint ecosystem.",
        og_type="website",
        url=f"{SITE_URL}/blog/",
        css_path="../styles.css",
        feed_title=FEED_TITLE,
        feed_url=f"{SITE_URL}/blog/feed.xml",
        root="../",
        blog_active=" nav__link--active",
        extra_styles=extra_styles,
    )

    # Slugs that belong to any series (suppressed as standalone cards)
    series_post_slugs = {
        post["slug"]
        for data in series_index.values()
        for post in data["posts"]
    }

    # Build unified item list: (date, stream, type, payload)
    items = []
    for meta in posts:
        if meta["slug"] not in series_post_slugs:
            stream = detectStream(meta)
            items.append((meta["date"], stream, "post", meta))
    for slug, data in series_index.items():
        stream = detectSeriesStream(data)
        items.append((data["date"], stream, "series", (slug, data)))

    def _is_pinned(itype, payload):
        if itype == "post":
            return bool(payload.get("pinned"))
        _, data = payload
        return bool(data.get("pinned"))

    def _pin_weight(itype, payload):
        if itype == "post":
            return payload.get("pin-weight", 99)
        _, data = payload
        return min((p.get("pin-weight", 99) for p in data["posts"]), default=99)

    # Pinned items first, then by pin-weight, then newest-first within each group
    items.sort(key=lambda x: (
        0 if _is_pinned(x[2], x[3]) else 1,
        _pin_weight(x[2], x[3]) if _is_pinned(x[2], x[3]) else 99,
        -x[0].toordinal()
    ))
    total = len(items)

    # Group by year, preserving sort order
    year_groups: dict = {}
    year_order: list = []
    for item in items:
        yr = str(item[0].year)
        if yr not in year_groups:
            year_groups[yr] = []
            year_order.append(yr)
        year_groups[yr].append(item)

    # Render grid
    grid_html = ""
    is_first = True
    for yr in year_order:
        grid_html += f'\n        <div class="blog-year-heading" data-year="{yr}">{yr}</div>'
        for date, stream, itype, payload in year_groups[yr]:
            is_pinned = _is_pinned(itype, payload)
            if itype == "post":
                grid_html += buildPostCardHtml(payload, stream=stream, is_featured=is_first)
            else:
                slug, data = payload
                pin_label = data.get("pin-label")
                grid_html += buildSeriesCardHtml(slug, data, pinned=is_pinned, pin_label=pin_label, stream=stream)
            is_first = False

    # Stream tab counts
    stream_counts: dict = {}
    for _, s, _, _ in items:
        stream_counts[s] = stream_counts.get(s, 0) + 1

    tab_defs = [
        ("all",             "All"),
        ("market-scenario", "Market Scenario"),
        ("workshop-notes",  "Workshop Notes"),
        ("engineers-log",   "Engineer\u2019s Log"),
    ]
    tabs_html = ""
    for stream_key, label in tab_defs:
        count = total if stream_key == "all" else stream_counts.get(stream_key, 0)
        if stream_key != "all" and count == 0:
            continue
        tabs_html += (
            f'<button class="blog-stream-tab" data-stream="{stream_key}">'
            f'{label} <span style="opacity:.55;font-size:.78em;">({count})</span>'
            f"</button>\n        "
        )

    # Collect all unique tags sorted alphabetically
    all_tags = sorted({
        t
        for _, _, itype, payload in items
        for t in (
            payload.get("tags", []) if itype == "post"
            else [tag for p in payload[1]["posts"] for tag in p.get("tags", [])]
        )
    })

    tags_strip_html = "".join(
        f'<button class="blog-tag-pill" data-tag="{t}">{t}</button>\n        '
        for t in all_tags
    )

    filter_js = """
  <script>
  (function () {
    var items     = Array.from(document.querySelectorAll('[data-stream]'));
    var yearHeads = Array.from(document.querySelectorAll('.blog-year-heading'));
    var countEl   = document.getElementById('blog-post-count');
    var clearBtn  = document.getElementById('blog-clear-btn');
    var activeStream = 'all';
    var activeTag    = '';

    function cardTags(el) {
      return el.dataset.tags ? el.dataset.tags.split(' ').filter(Boolean) : [];
    }

    function applyFilter() {
      var vis = 0;
      items.forEach(function (el) {
        var streamOk = activeStream === 'all' || el.dataset.stream === activeStream;
        var tagOk    = !activeTag || cardTags(el).indexOf(activeTag) !== -1;
        var show = streamOk && tagOk;
        el.classList.toggle('blog-index-item--hidden', !show);
        if (show) vis++;
      });

      // Featured: first visible card gets full-width only in full 'All' view
      var first = items.find(function (el) {
        return !el.classList.contains('blog-index-item--hidden');
      });
      items.forEach(function (el) { el.classList.remove('blog-card--featured'); });
      if (activeStream === 'all' && !activeTag && first)
        first.classList.add('blog-card--featured');

      // Hide year headings with no visible items
      yearHeads.forEach(function (h) {
        var yr  = h.dataset.year;
        var has = items.some(function (el) {
          return el.dataset.year === yr && !el.classList.contains('blog-index-item--hidden');
        });
        h.classList.toggle('blog-index-item--hidden', !has);
      });

      if (countEl) countEl.textContent = vis;

      // Clear button: visible when any filter is active
      var filtered = activeStream !== 'all' || activeTag !== '';
      if (clearBtn) clearBtn.style.display = filtered ? 'inline-flex' : 'none';

      // Update stream tab active states
      document.querySelectorAll('.blog-stream-tab').forEach(function (btn) {
        btn.classList.toggle('active', btn.dataset.stream === activeStream);
      });

      // Update tag pill active states
      document.querySelectorAll('.blog-tag-pill').forEach(function (btn) {
        btn.classList.toggle('active', btn.dataset.tag === activeTag);
      });
    }

    // Stream tabs
    document.querySelectorAll('.blog-stream-tab').forEach(function (btn) {
      btn.addEventListener('click', function () {
        activeStream = this.dataset.stream;
        applyFilter();
      });
    });

    // Tag pills: click active tag to deselect; click new tag to select
    document.querySelectorAll('.blog-tag-pill').forEach(function (btn) {
      btn.addEventListener('click', function () {
        activeTag = activeTag === this.dataset.tag ? '' : this.dataset.tag;
        applyFilter();
      });
    });

    // Clear all
    if (clearBtn) {
      clearBtn.addEventListener('click', function () {
        activeStream = 'all';
        activeTag    = '';
        applyFilter();
      });
    }

    applyFilter();
  })();
  </script>"""

    content = f"""
  <section class="section" id="blog-index" style="padding-top: calc(var(--space-4xl) + 60px);">
    <div class="container container--narrow">
      <div class="reveal text-center" style="margin-bottom: var(--space-2xl);">
        <span class="section__label">Blog</span>
        <h1 class="section__title">Dispatches from the Thin Market Frontier</h1>
        <p class="section__desc section__desc--centered">
          Science, engineering, and lessons learned building markets that work.
        </p>
      </div>
      <div class="blog-stream-tabs">
        {tabs_html}
      </div>
      <div class="blog-tag-strip">
        {tags_strip_html}
      </div>
      <div class="blog-index-count">
        Showing <span id="blog-post-count">{total}</span> of {total} posts
        <button id="blog-clear-btn"
                style="display:none;margin-left:.75rem;padding:2px 10px;border-radius:14px;
                       border:1px solid rgba(239,68,68,.4);background:transparent;
                       color:#fca5a5;font-size:.74rem;font-weight:600;
                       cursor:pointer;font-family:inherit;
                       transition:background .15s;"
                onmouseover="this.style.background='rgba(239,68,68,.12)'"
                onmouseout="this.style.background='transparent'">&#10005; Show all</button>
      </div>
      <div class="blog-grid">
        {grid_html}
      </div>
    </div>
  </section>
{filter_js}
"""

    footer = PAGE_FOOTER.format(root="../")

    return head + content + footer


# ---------------------------------------------------------------------------
# RSS Feed
# ---------------------------------------------------------------------------


def buildRssFeed(posts):
    """Generate an RSS 2.0 XML feed."""
    rss = Element("rss", version="2.0")
    channel = SubElement(rss, "channel")

    SubElement(channel, "title").text = FEED_TITLE
    SubElement(channel, "link").text = f"{SITE_URL}/blog/"
    SubElement(channel, "description").text = FEED_DESC
    SubElement(channel, "language").text = "en"
    SubElement(channel, "lastBuildDate").text = datetime.now(
        tz=__import__("datetime").timezone.utc
    ).strftime(
        "%a, %d %b %Y %H:%M:%S +0000"
    )

    for meta in posts:
        item = SubElement(channel, "item")
        SubElement(item, "title").text = meta["title"]
        SubElement(item, "link").text = f"{SITE_URL}/blog/{meta['slug']}.html"
        SubElement(item, "description").text = meta["summary"]
        SubElement(item, "pubDate").text = meta["date"].strftime(
            "%a, %d %b %Y 00:00:00 +0000"
        )
        SubElement(item, "guid").text = f"{SITE_URL}/blog/{meta['slug']}.html"
        for tag in meta["tags"]:
            SubElement(item, "category").text = tag

    xml_bytes = tostring(rss, encoding="unicode", xml_declaration=False)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_bytes


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    """Build all blog pages from Markdown sources."""
    print("Blog build starting...")
    print(f"  Posts dir: {POSTS_DIR}")
    print(f"  Output dir: {BLOG_OUT}")

    if not POSTS_DIR.exists():
        print(f"  Creating posts directory: {POSTS_DIR}")
        POSTS_DIR.mkdir(parents=True, exist_ok=True)
        print("  No posts found. Done.")
        return

    # Collect and parse all posts
    md_files = sorted(POSTS_DIR.glob("*.md"))
    if not md_files:
        print("  No .md files found in posts directory.")
        return

    posts = []
    for filepath in md_files:
        meta, body_html = parsePost(filepath)
        if meta is None:
            continue
        meta["_body_html"] = body_html
        posts.append(meta)
        print(f"  Parsed: {filepath.name} -> {meta['slug']}.html")

    # Sort by date, newest first
    posts.sort(key=lambda p: p["date"], reverse=True)

    # Separate public posts from unlisted posts
    public_posts = [p for p in posts if not p.get("unlisted", False)]

    # Build series index BEFORE the post loop (while _body_html still exists)
    series_index = buildSeriesIndex(public_posts)
    if series_index:
        for slug, data in series_index.items():
            print(f"  Series '{slug}': {len(data['posts'])} posts")

    # Generate individual post pages
    BLOG_OUT.mkdir(parents=True, exist_ok=True)
    for meta in posts:
        body_html = meta.pop("_body_html")
        series_posts = None
        if meta.get("series"):
            series_posts = series_index.get(meta["series"], {}).get("posts", [])
        page = buildPostPage(meta, body_html, series_posts)
        out_path = BLOG_OUT / f"{meta['slug']}.html"
        out_path.write_text(page, encoding="utf-8")
        print(f"  Wrote: {out_path.name}")

    # Generate index
    index_html = buildIndexPage(public_posts, series_index)
    index_path = BLOG_OUT / "index.html"
    index_path.write_text(index_html, encoding="utf-8")
    print(f"  Wrote: index.html ({len(public_posts)} public posts)")

    # Generate series landing pages
    if series_index:
        series_dir = BLOG_OUT / "series"
        series_dir.mkdir(parents=True, exist_ok=True)
        for slug, data in series_index.items():
            series_page = buildSeriesPage(slug, data)
            series_path = series_dir / f"{slug}.html"
            series_path.write_text(series_page, encoding="utf-8")
            print(f"  Wrote: series/{slug}.html -> {SITE_URL}/blog/series/{slug}.html")

    # Generate RSS feed
    feed_xml = buildRssFeed(public_posts)
    feed_path = BLOG_OUT / "feed.xml"
    feed_path.write_text(feed_xml, encoding="utf-8")
    print("  Wrote: feed.xml")

    print(f"Blog build complete. {len(public_posts)} public posts published, {len(posts) - len(public_posts)} unlisted.")


if __name__ == "__main__":
    main()
