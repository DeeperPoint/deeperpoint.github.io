# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.

"""
Blog Build Script for DeeperPoint

Reads Markdown posts from blog/posts/, converts them to HTML using the site's
design system, and generates a blog index page and RSS feed.

Usage:
    python scripts/build_blog.py

Posts must have YAML frontmatter with: title, date, tags, summary, author, slug.
"""

import re
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

MD_EXTENSIONS = ["fenced_code", "tables", "toc", "smarty", "attr_list"]

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
</head>

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
      <ul class="nav__links">
        <li><a href="{root}thin-markets.html" class="nav__link">The Problem</a></li>
        <li><a href="{root}marketforge.html" class="nav__link">The Project</a></li>
        <li><a href="{root}testbeds-detail.html" class="nav__link">Examples</a></li>
        <li><a href="{root}who-should-care.html" class="nav__link">Who's It For</a></li>
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
          <li><a href="https://deeperpoint.com" class="footer__link" target="_blank" rel="noopener">deeperpoint.com</a></li>
          <li><a href="https://github.com/DeeperPoint" class="footer__link" target="_blank" rel="noopener">GitHub</a></li>
        </ul>
      </div>
    </div>
  </footer>

  <script src="{root}reveal.js"></script>
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
# Page Generation
# ---------------------------------------------------------------------------


def buildPostPage(meta, body_html):
    """Generate a full HTML page for a single blog post."""
    date_str = meta["date"].strftime("%B %d, %Y")
    tags_html = "".join(
        f'<span class="blog-tag">{tag}</span>' for tag in meta["tags"]
    )

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
      <article class="blog-post">
        {body_html}
      </article>
    </div>
  </section>
"""

    footer = PAGE_FOOTER.format(root="../")

    return head + content + footer


def buildIndexPage(posts):
    """Generate the blog listing page."""
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
    )

    cards = []
    for meta in posts:
        date_str = meta["date"].strftime("%B %d, %Y")
        tags_html = "".join(
            f'<span class="blog-tag">{tag}</span>' for tag in meta["tags"]
        )
        cards.append(f"""
        <a href="{meta['slug']}.html" class="blog-card card reveal">
          <div class="blog-meta">
            <time datetime="{meta['date'].isoformat()}">{date_str}</time>
            <span class="blog-meta__sep">&middot;</span>
            <span>{meta['reading_time']} min read</span>
          </div>
          <h3 class="blog-card__title">{meta['title']}</h3>
          <p class="blog-card__summary">{meta['summary']}</p>
          <div class="blog-meta">{tags_html}</div>
        </a>
""")

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
      <div class="blog-index">
        {''.join(cards)}
      </div>
    </div>
  </section>
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

    # Collect all posts
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

    # Generate individual post pages
    BLOG_OUT.mkdir(parents=True, exist_ok=True)
    for meta in posts:
        body_html = meta.pop("_body_html")
        page = buildPostPage(meta, body_html)
        out_path = BLOG_OUT / f"{meta['slug']}.html"
        out_path.write_text(page, encoding="utf-8")
        print(f"  Wrote: {out_path.name}")

    # Generate index
    index_html = buildIndexPage(posts)
    index_path = BLOG_OUT / "index.html"
    index_path.write_text(index_html, encoding="utf-8")
    print(f"  Wrote: index.html ({len(posts)} posts)")

    # Generate RSS feed
    feed_xml = buildRssFeed(posts)
    feed_path = BLOG_OUT / "feed.xml"
    feed_path.write_text(feed_xml, encoding="utf-8")
    print("  Wrote: feed.xml")

    print(f"Blog build complete. {len(posts)} posts published.")


if __name__ == "__main__":
    main()
