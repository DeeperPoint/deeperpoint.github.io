# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.

"""
Market Catalog Build Script for DeeperPoint  v2

Changes from v1:
  - Stories are self-contained in each YAML scenario file (story.body, markdown format).
    Blog publication is optional: story.blog_slug is only set when the user explicitly
    promotes the story to the blog via a separate workflow.
  - Catalog index page has full-text search + multi-select sector/tag dropdowns
    + tier buttons, designed to handle 20–300+ entries without degrading UX.
  - 2026-11-24: the index page is a dense list of titles grouped by sector, with a
    reading panel beside it (a bottom sheet on phones), search that says where it
    matched, and the old cards kept as a second view. The page leads with the count.

YAML schema for each scenario file:
    id, title, sector, sub_sector, forge_tier, status, tags
    card_title: "Short title for the index title list (≤60 chars; avoid ending in 'Matching')"
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
import re
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
BLOG_POSTS_DIR = SITE_ROOT / "blog" / "posts"
REDIRECTS_FILE = CATALOG_OUT / "redirects.yaml"

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
      padding-top: calc(var(--space-2xl, 2rem) + 60px);
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
      max-width: 820px; margin: 0 auto 1.25rem; padding: 0 1.5rem; line-height: 1.65;
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
    .idea-note {
      border-left: 3px solid rgba(245,158,11,.55); background: rgba(245,158,11,.07);
      padding: .7rem 1rem; margin: 0 0 1.5rem; border-radius: 0 8px 8px 0;
      font-size: .85rem; line-height: 1.55; color: var(--color-text-secondary, #cbd5e1);
    }
    .idea-note strong { color: #fbbf24; font-weight: 600; }

    /* --- Lead number --- */
    .cat-lead {
      font-family: 'Outfit', 'Inter', sans-serif; font-size: 1.15rem; font-weight: 500;
      color: var(--color-text-secondary, #cbd5e1); margin: 0 auto 1.1rem; line-height: 1.4;
    }
    .cat-lead__num {
      display: block; font-size: 5rem; font-weight: 700; line-height: 1; color: #f59e0b;
      letter-spacing: -.02em; margin-bottom: .35rem;
    }
    .cat-lead strong { color: var(--color-text-primary, #f1f5f9); font-weight: 600; }
    .cat-wide { max-width: 1560px; }

    /* --- View buttons (list / cards) --- */
    .view-btns { display: inline-flex; border-radius: 8px; overflow: hidden; border: 1px solid rgba(99,102,241,.35); }
    .view-btn {
      padding: .45rem .85rem; font-size: .78rem; font-weight: 600;
      background: transparent; border: none; border-right: 1px solid rgba(99,102,241,.25);
      color: #a5b4fc; cursor: pointer; font-family: inherit; transition: background .15s;
    }
    .view-btn:last-child { border-right: none; }
    .view-btn:hover { background: rgba(99,102,241,.1); }
    .view-btn.active { background: rgba(99,102,241,.25); color: #e0e7ff; }

    /* --- Title list with a reading panel beside it --- */
    .cat-layout {
      display: grid; grid-template-columns: minmax(0, 1fr) 380px; gap: 2rem;
      align-items: start; text-align: left; margin-bottom: 4rem;
    }
    .idea-groups { columns: 270px; column-gap: 2rem; }
    .idea-group { break-inside: avoid; margin: 0 0 1.1rem; }
    .idea-group--hidden { display: none; }
    .idea-group__head {
      list-style: none; cursor: pointer; display: flex; align-items: baseline; gap: .5rem;
      font-size: .68rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase;
      color: #818cf8; padding: .3rem 0; margin-bottom: .3rem;
      border-bottom: 1px solid rgba(99,102,241,.25);
    }
    .idea-group__head::-webkit-details-marker { display: none; }
    .idea-group__name { flex: 1; }
    .idea-group__count { color: #64748b; letter-spacing: .04em; white-space: nowrap; }
    .idea-group__caret { display: none; color: #64748b; transition: transform .15s; }
    .idea-group[open] .idea-group__caret { transform: rotate(90deg); }
    .idea {
      display: block; text-decoration: none; color: var(--color-text-secondary, #cbd5e1);
      font-size: .84rem; line-height: 1.35; padding: .22rem .5rem;
      border-radius: 6px; border-left: 2px solid transparent;
    }
    .idea:hover { background: rgba(99,102,241,.12); color: #f1f5f9; }
    .idea:focus-visible { outline: 2px solid #6366f1; outline-offset: 1px; }
    .idea--active, .idea--active:hover { background: rgba(99,102,241,.22); border-left-color: #6366f1; color: #fff; }
    .idea--hidden { display: none; }
    .idea__title { display: block; }
    .idea__meta, .idea__summary, .idea__tags, .idea__footer { display: none; }
    .idea__hit { display: block; font-size: .72rem; line-height: 1.4; color: #94a3b8; margin-top: .1rem; }
    .idea__hit:empty { display: none; }
    .idea__hit b { color: #818cf8; font-weight: 600; }
    .cat-layout mark { background: rgba(245,158,11,.3); color: #fde68a; border-radius: 2px; padding: 0 1px; }
    .cat-empty { text-align: center; padding: 3rem 1rem; color: #64748b; display: none; }

    .idea-panel {
      position: sticky; top: 90px; max-height: calc(100vh - 110px); overflow: auto;
      background: rgba(15,23,42,.85); border: 1px solid rgba(99,102,241,.3);
      border-radius: 16px; padding: 1.4rem 1.5rem;
    }
    .idea-panel__empty { font-size: .88rem; line-height: 1.6; color: var(--color-text-muted, #94a3b8); margin: 0; }
    .idea-panel__empty strong { color: var(--color-text-primary, #f1f5f9); }
    .idea-panel__close {
      display: none; position: absolute; top: .5rem; right: .75rem; background: none; border: none;
      color: #94a3b8; font-size: 1.8rem; line-height: 1; cursor: pointer; padding: .25rem .5rem;
    }
    .idea-panel__title {
      font-size: 1.2rem; font-weight: 700; line-height: 1.3; margin: 0 0 .4rem;
      color: var(--color-text-primary, #f1f5f9);
    }
    .idea-panel__full { font-size: .78rem; line-height: 1.45; color: var(--color-text-muted, #94a3b8); margin: 0 0 .75rem; }
    .idea-panel__summary { font-size: .9rem; line-height: 1.6; color: var(--color-text-secondary, #cbd5e1); margin: 0 0 1rem; }
    .idea-panel__cta {
      display: inline-flex; align-items: center; margin-top: 1rem; padding: .55rem 1.2rem;
      border-radius: 20px; background: #6366f1; color: #fff; font-size: .85rem; font-weight: 600;
      text-decoration: none; transition: background .15s;
    }
    .idea-panel__cta:hover { background: #4f46e5; }
    .idea-panel__nav { display: flex; justify-content: space-between; gap: .5rem; margin-top: 1.1rem;
      padding-top: .85rem; border-top: 1px solid rgba(99,102,241,.2); }
    .idea-panel__nav button {
      background: none; border: none; color: #818cf8; font-size: .78rem; font-weight: 600;
      cursor: pointer; font-family: inherit; padding: .3rem 0;
    }
    .idea-panel__nav button:hover { color: #c7d2fe; }
    .idea-backdrop { display: none; }

    /* --- Card view: the same entries drawn as cards, no panel --- */
    .cat-layout--cards { grid-template-columns: minmax(0, 1fr); }
    .cat-layout--cards .idea-panel { display: none; }
    .cat-layout--cards .idea-groups { columns: auto; }
    .cat-layout--cards .idea-group__items {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.25rem; margin: .9rem 0 2rem;
    }
    .cat-layout--cards .idea {
      background: rgba(15,23,42,.6); border: 1px solid rgba(99,102,241,.2);
      border-radius: 16px; padding: 1.4rem 1.5rem; color: inherit;
      transition: transform .2s, box-shadow .2s, border-color .2s;
    }
    .cat-layout--cards .idea:hover {
      transform: translateY(-3px); box-shadow: 0 12px 40px rgba(99,102,241,.18);
      border-color: rgba(99,102,241,.45);
    }
    .cat-layout--cards .idea__meta { display: flex; }
    .cat-layout--cards .idea__summary { display: block; }
    .cat-layout--cards .idea__tags { display: flex; }
    .cat-layout--cards .idea__footer { display: flex; }
    .cat-layout--cards .idea__title {
      font-size: 1.05rem; font-weight: 700; line-height: 1.35; margin-bottom: .5rem;
      color: var(--color-text-primary, #f1f5f9);
    }
    .cat-layout--cards .idea__hit { font-size: .78rem; margin: 0 0 .6rem; }

    /* --- Phones and narrow windows: sectors fold, the panel becomes a bottom sheet --- */
    @media (max-width: 900px) {
      .cat-header { padding-top: calc(2rem + 80px); }
      .cat-desc { padding: 0; }
      .cat-lead__num { font-size: 3.6rem; }
      .cat-layout { grid-template-columns: minmax(0, 1fr); }
      .idea-groups { columns: auto; }
      .idea-group { margin-bottom: .2rem; }
      .idea-group__head { padding: .85rem 0; font-size: .74rem; margin-bottom: 0; }
      .idea-group[open] .idea-group__head { margin-bottom: .4rem; }
      .idea-group__caret { display: inline-block; }
      .idea { padding: .6rem .5rem; font-size: .92rem; }
      .idea-panel {
        position: fixed; left: 0; right: 0; bottom: 0; top: auto; z-index: 300;
        max-height: 72vh; border-radius: 16px 16px 0 0; border-bottom: none;
        background: #111827; box-shadow: 0 -12px 40px rgba(0,0,0,.6);
        padding: 1.5rem 1.25rem calc(1.25rem + env(safe-area-inset-bottom, 0px));
        transform: translateY(105%); transition: transform .2s;
      }
      .idea-panel--open { transform: none; }
      .idea-panel__close { display: block; }
      .idea-panel .scenario-card__top { padding-right: 2.5rem; }
      .idea-backdrop--open { display: block; position: fixed; inset: 0; z-index: 290; background: rgba(0,0,0,.55); }
      .cat-layout--cards .idea-group__items { grid-template-columns: minmax(0, 1fr); }
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
        <li><a href="__ROOT__market-physics.html" class="nav__link">Why Markets Don&rsquo;t Form</a></li>
        <li><a href="__ROOT__platform.html" class="nav__link">What We&rsquo;re Building</a></li>
        <li><a href="__ROOT__catalog/index.html" class="nav__link nav__link--active">Catalog</a></li>
        <li><a href="__ROOT__demos.html" class="nav__link">Demos</a></li>
        <li><a href="__ROOT__blog/index.html" class="nav__link">Blog</a></li>
        <li><a href="__ROOT__cost-model.html" class="nav__link">Cost</a></li>
        <li><a href="__ROOT__library.html" class="nav__link">Library</a></li>
        <li><a href="__ROOT__about.html" class="nav__link">About</a></li>
        <li><a href="__ROOT__contribute.html" class="nav__link nav__link--cta">Contribute</a></li>
        <li><a href="__ROOT__search.html" class="nav__link nav__link--icon" aria-label="Search the site">&#x1f50d;</a></li>
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
    """Return coloured dot + label saying where the idea's story can be read.

    Derived from content, not from story.status: that field recorded whether a
    story had been promoted to the blog, drifted out of step with the facts, and
    read to visitors as "unfinished". It is no longer displayed (2026-11-21).
    """
    story = story or {}
    blog_slug = story.get("blog_slug", "")
    if blog_slug and (BLOG_POSTS_DIR / f"{blog_slug}.md").exists():
        color, label = "#818cf8", "Full story on the blog"
    elif story.get("body"):
        color, label = "#4ade80", "Short story included"
    else:
        return ""
    return (
        f'<span class="scenario-card__story-dot" style="background:{color};" title="{html.escape(label)}"></span>'
        f"<span>{label}</span>"
    )


# ---------------------------------------------------------------------------
# Catalog Index Page  (search + multi-select filters)
# ---------------------------------------------------------------------------


def sectorLabel(sector):
    """Readable name for a sector slug: 'pets-and-animals' -> 'Pets and Animals'."""
    return sector.replace("-", " ").title().replace(" And ", " and ")


def buildIndexPage(scenarios):
    """Generate the catalog index: a dense list of titles grouped by sector, with a
    reading panel beside it, search that says where it matched, and a card view."""

    # Group by sector; sectors and the titles inside them run alphabetically.
    by_sector = {}
    for s in scenarios:
        by_sector.setdefault(s.get("sector", "other"), []).append(s)
    sectors = sorted(by_sector, key=sectorLabel)
    all_tags = sorted({t for s in scenarios for t in s.get("tags", [])})
    total = len(scenarios)

    # --- Sector dropdown options ---
    sector_options = ""
    for sec in sectors:
        sector_options += (
            f'<label class="fdd__item">'
            f'<input type="checkbox" class="sector-cb" value="{escHtml(sec)}"> {escHtml(sectorLabel(sec))}'
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

    # --- One entry per idea. The list view shows only the title; the card view and the
    #     reading panel draw on the rest, so each idea is written into the page once. ---
    groups_html = ""
    for sec in sectors:
        label = escHtml(sectorLabel(sec))
        members = sorted(by_sector[sec], key=lambda s: (s.get("card_title") or s.get("title", "")).lower())
        items_html = ""
        for s in members:
            sid = escHtml(s.get("id", ""))
            title = escHtml(s.get("title", "Untitled"))
            card_title = escHtml(s.get("card_title") or s.get("title", "Untitled"))
            tier = s.get("forge_tier", 2)
            me = s.get("market_example", {})
            summary = escHtml(me.get("summary", ""))
            tags = s.get("tags", [])
            sponsor_count = len(s.get("sponsor_opportunities", []))
            tags_html = "".join(f'<span class="scenario-card__tag">{escHtml(t)}</span>' for t in tags)
            s_label = f"{sponsor_count} sponsor/investor opp" + ("s" if sponsor_count != 1 else "")
            items_html += f"""
            <a href="{sid}.html" class="idea" data-id="{sid}" data-tier="{tier}"
               data-tags="{escHtml(' '.join(tags))}" data-title="{title}">
              <span class="idea__meta scenario-card__top"><span class="scenario-card__sector">{label}</span>{tierBadge(tier)}</span>
              <span class="idea__title">{card_title}</span>
              <span class="idea__hit"></span>
              <span class="idea__summary scenario-card__summary">{summary}</span>
              <span class="idea__tags scenario-card__tags">{tags_html}</span>
              <span class="idea__footer scenario-card__footer">{storyDot(s.get("story", {}))}<span style="margin-left:auto">{s_label}</span></span>
            </a>"""
        groups_html += f"""
          <details class="idea-group" open data-sector="{escHtml(sec)}">
            <summary class="idea-group__head">
              <span class="idea-group__caret" aria-hidden="true">&#9656;</span>
              <span class="idea-group__name">{label}</span>
              <span class="idea-group__count">{len(members)}</span>
            </summary>
            <div class="idea-group__items">{items_html}
            </div>
          </details>"""

    # --- Inline JS: search, filters, the reading panel and the view switch ---
    filter_js = r"""
  <script>
  (function () {
    var layout = document.getElementById('cat-layout');
    var panel = document.getElementById('idea-panel');
    var backdrop = document.getElementById('idea-backdrop');
    var countEl = document.getElementById('visible-count');
    var chipsEl = document.getElementById('filter-chips');
    var clearBtn = document.getElementById('btn-clear');
    var emptyEl = document.getElementById('no-results');
    var searchInput = document.getElementById('cat-search');
    var narrow = window.matchMedia('(max-width: 900px)');
    var placeholder = panel.innerHTML;

    // -- Read the ideas out of the page --
    var groups = [], ideas = [];
    Array.prototype.forEach.call(document.querySelectorAll('.idea-group'), function (el) {
      var g = { el: el, sector: el.dataset.sector, total: 0, vis: 0,
                label: el.querySelector('.idea-group__name').textContent,
                countEl: el.querySelector('.idea-group__count') };
      g.labelLow = g.label.toLowerCase();
      groups.push(g);
      Array.prototype.forEach.call(el.querySelectorAll('.idea'), function (a) {
        var it = { el: a, group: g, id: a.dataset.id, tier: a.dataset.tier, shown: true,
                   tags: a.dataset.tags ? a.dataset.tags.split(' ') : [],
                   titleEl: a.querySelector('.idea__title'), hitEl: a.querySelector('.idea__hit'),
                   full: a.dataset.title || '',
                   summary: a.querySelector('.idea__summary').textContent };
        it.title = it.titleEl.textContent;
        it.titleLow = it.title.toLowerCase();
        it.fullLow = it.full.toLowerCase();
        it.summaryLow = it.summary.toLowerCase();
        g.total++;
        ideas.push(it);
      });
    });

    // -- State --
    var query = '';
    var activeSectors = {};
    var activeTags = {};
    var activeTier = 'all';
    var active = null;
    var view = 'list';

    // -- Text helpers --
    function esc(s) {
      return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
    function mark(text, q) {
      if (!q) return esc(text);
      var low = text.toLowerCase(), out = '', i = 0, j;
      while ((j = low.indexOf(q, i)) !== -1) {
        out += esc(text.slice(i, j)) + '<mark>' + esc(text.slice(j, j + q.length)) + '</mark>';
        i = j + q.length;
      }
      return out + esc(text.slice(i));
    }
    function snippet(text, q) {
      var j = text.toLowerCase().indexOf(q);
      var start = Math.max(0, j - 45), end = Math.min(text.length, j + q.length + 70);
      if (start > 0) { var sp = text.indexOf(' ', start); if (sp !== -1 && sp < j) start = sp + 1; }
      if (end < text.length) { var ep = text.lastIndexOf(' ', end); if (ep > j + q.length) end = ep; }
      return (start > 0 ? '&hellip;' : '') + mark(text.slice(start, end), q) + (end < text.length ? '&hellip;' : '');
    }

    // -- Where does the search text occur in this idea? null when it does not. --
    function findHit(it) {
      if (!query) return { where: 'none' };
      if (it.titleLow.indexOf(query) !== -1) return { where: 'title' };
      if (it.fullLow.indexOf(query) !== -1) return { where: 'Full title', text: it.full };
      for (var i = 0; i < it.tags.length; i++) {
        var spaced = it.tags[i].replace(/-/g, ' ');
        if (it.tags[i].indexOf(query) !== -1) return { where: 'Tag', text: it.tags[i] };
        if (spaced.indexOf(query) !== -1) return { where: 'Tag', text: spaced };
      }
      if (it.group.labelLow.indexOf(query) !== -1) return { where: 'Sector', text: it.group.label };
      if (it.summaryLow.indexOf(query) !== -1) return { where: 'Summary', text: it.summary };
      return null;
    }
    function showHit(it, hit) {
      it.titleEl.innerHTML = hit.where === 'title' ? mark(it.title, query) : esc(it.title);
      it.hitEl.innerHTML = hit.text ? '<b>' + hit.where + ':</b> ' + snippet(hit.text, query) : '';
    }

    // -- Filters --
    function passesFilters(it) {
      if (Object.keys(activeSectors).length && !activeSectors[it.group.sector]) return false;
      if (Object.keys(activeTags).length) {
        var ok = false;
        for (var i = 0; i < it.tags.length; i++) { if (activeTags[it.tags[i]]) { ok = true; break; } }
        if (!ok) return false;
      }
      if (activeTier !== 'all' && it.tier !== activeTier) return false;
      return true;
    }

    function applyFilters() {
      var vis = 0;
      var filtering = !!query || activeTier !== 'all' ||
        Object.keys(activeSectors).length > 0 || Object.keys(activeTags).length > 0;
      groups.forEach(function (g) { g.vis = 0; });
      ideas.forEach(function (it) {
        var hit = passesFilters(it) ? findHit(it) : null;
        it.shown = !!hit;
        it.el.classList.toggle('idea--hidden', !hit);
        if (hit) { vis++; it.group.vis++; showHit(it, hit); }
      });
      groups.forEach(function (g) {
        g.el.classList.toggle('idea-group--hidden', g.vis === 0);
        g.countEl.textContent = g.vis === g.total ? g.total : g.vis + ' of ' + g.total;
        if (filtering && g.vis) g.el.open = true;
      });
      if (countEl) countEl.textContent = vis;
      if (emptyEl) emptyEl.style.display = vis ? 'none' : 'block';
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
        return '<span class="filter-chip" data-type="' + c.type + '" data-value="' + esc(c.value) + '">' +
          esc(c.label) + '<button class="filter-chip__x" title="Remove">&times;</button></span>';
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
      if (clearBtn) clearBtn.style.display = (chips.length || query) ? 'inline-flex' : 'none';
    }

    function updateDropdownLabels() {
      var secCount = Object.keys(activeSectors).length;
      var tagCount = Object.keys(activeTags).length;
      document.getElementById('sector-label').textContent = secCount ? 'Sectors (' + secCount + ')' : 'All Sectors';
      document.getElementById('tag-label').textContent    = tagCount ? 'Tags (' + tagCount + ')' : 'All Tags';
    }

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

    // -- Reading panel --
    function part(it, cls) { return it.el.querySelector(cls).innerHTML; }
    function openIdea(it) {
      if (active) active.el.classList.remove('idea--active');
      active = it;
      it.el.classList.add('idea--active');
      it.group.el.open = true;
      panel.innerHTML =
        '<button class="idea-panel__close" type="button" aria-label="Close">&times;</button>' +
        '<div class="scenario-card__top">' + part(it, '.idea__meta') + '</div>' +
        '<h2 class="idea-panel__title">' + esc(it.title) + '</h2>' +
        (it.full && it.full !== it.title ? '<p class="idea-panel__full">' + esc(it.full) + '</p>' : '') +
        '<p class="idea-panel__summary">' + mark(it.summary, query) + '</p>' +
        '<div class="scenario-card__tags">' + part(it, '.idea__tags') + '</div>' +
        '<div class="scenario-card__footer">' + part(it, '.idea__footer') + '</div>' +
        '<a class="idea-panel__cta" href="' + it.el.getAttribute('href') + '">Read the full idea &rarr;</a>' +
        '<div class="idea-panel__nav">' +
          '<button type="button" data-step="-1">&larr; Previous</button>' +
          '<button type="button" data-step="1">Next &rarr;</button></div>';
      panel.scrollTop = 0;
      panel.classList.add('idea-panel--open');
      backdrop.classList.add('idea-backdrop--open');
      try { history.replaceState(null, '', '#' + it.id); } catch (e) {}
    }
    function closeIdea() {
      if (active) active.el.classList.remove('idea--active');
      active = null;
      panel.innerHTML = placeholder;
      panel.classList.remove('idea-panel--open');
      backdrop.classList.remove('idea-backdrop--open');
      try { history.replaceState(null, '', location.pathname + location.search); } catch (e) {}
    }
    function step(n) {
      var shown = ideas.filter(function (it) { return it.shown; });
      if (!shown.length) return;
      var i = shown.indexOf(active);
      var next = i === -1 ? shown[0] : shown[i + n];
      if (!next) return;
      openIdea(next);
      if (narrow.matches) next.el.scrollIntoView({ block: 'center' });
      else next.el.focus();
    }

    document.getElementById('idea-groups').addEventListener('click', function (e) {
      var a = e.target.closest('.idea');
      if (!a || view === 'cards') return;                               // card view: follow the link
      if (e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;  // new tab etc.
      e.preventDefault();
      for (var i = 0; i < ideas.length; i++) { if (ideas[i].el === a) { openIdea(ideas[i]); break; } }
    });
    panel.addEventListener('click', function (e) {
      if (e.target.closest('.idea-panel__close')) { closeIdea(); return; }
      var s = e.target.closest('[data-step]');
      if (s) step(parseInt(s.dataset.step, 10));
    });
    backdrop.addEventListener('click', closeIdea);

    // -- List / cards --
    function setView(v) {
      view = v === 'cards' ? 'cards' : 'list';
      layout.classList.toggle('cat-layout--cards', view === 'cards');
      document.querySelectorAll('.view-btn').forEach(function (b) {
        b.classList.toggle('active', b.dataset.value === view);
      });
      if (view === 'cards') closeIdea();
      try { localStorage.setItem('dp-catalog-view', view); } catch (e) {}
    }
    document.querySelectorAll('.view-btn').forEach(function (btn) {
      btn.addEventListener('click', function () { setView(this.dataset.value); });
    });

    // -- Search --
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
        var box = this.closest('.fdd__panel');
        box.querySelectorAll('.fdd__item').forEach(function (item) {
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
    function closeDropdowns() {
      document.querySelectorAll('.fdd').forEach(function (f) { f.classList.remove('fdd--open'); });
    }
    document.querySelectorAll('.fdd__btn').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var fdd = btn.closest('.fdd');
        var isOpen = fdd.classList.contains('fdd--open');
        closeDropdowns();
        if (!isOpen) {
          fdd.classList.add('fdd--open');
          var si = fdd.querySelector('.fdd__search');
          if (si) setTimeout(function() { si.focus(); }, 50);
        }
      });
    });
    document.querySelectorAll('.fdd__panel').forEach(function (p) {
      p.addEventListener('click', function (e) { e.stopPropagation(); });
    });
    document.addEventListener('click', closeDropdowns);

    // -- Keys: Escape closes; up and down walk the list while an idea is open --
    document.addEventListener('keydown', function (e) {
      var tag = (e.target.tagName || '').toLowerCase();
      if (e.key === 'Escape') {
        closeDropdowns();
        if (active && tag !== 'input') closeIdea();
        return;
      }
      if (!active || view === 'cards' || tag === 'input' || tag === 'textarea') return;
      if (e.key === 'ArrowDown') { e.preventDefault(); step(1); }
      if (e.key === 'ArrowUp')   { e.preventDefault(); step(-1); }
    });

    // -- Start --
    var saved = null;
    try { saved = localStorage.getItem('dp-catalog-view'); } catch (e) {}
    setView(saved);
    if (narrow.matches) groups.forEach(function (g) { g.el.open = false; });   // phones start folded
    var asked = '';
    try { asked = new URLSearchParams(location.search).get('q') || ''; } catch (e) {}
    if (asked && searchInput) { searchInput.value = asked; query = asked.toLowerCase().trim(); }   // catalog/?q=term
    applyFilters();
    var wanted = decodeURIComponent(location.hash.slice(1));
    if (wanted && view === 'list') {
      for (var k = 0; k < ideas.length; k++) {
        if (ideas[k].id === wanted) {
          openIdea(ideas[k]);
          var box = ideas[k].el.getBoundingClientRect();
          if (box.top < 80 || box.bottom > window.innerHeight) ideas[k].el.scrollIntoView({ block: 'center' });
          break;
        }
      }
    }
  })();
  </script>"""

    head = renderHead(
        title="Catalog of Market Ideas — Thin Markets Waiting to Be Built",
        description=f"{total} ideas for thin markets that could exist if the right matching infrastructure were built. None has been built. Each idea has a market analysis, sponsor revenue models and a short fictional story showing how a match would work.",
        css_path="../styles.css",
        root="../",
    )

    content = f"""
  <section class="section cat-header" id="catalog-index">
    <div class="container cat-wide">
      <h1 class="cat-title">Catalog of Market Ideas</h1>
      <p class="cat-lead">
        <span class="cat-lead__num">{total}</span>
        ideas for thin markets that nobody has built yet, across <strong>{len(sectors)} sectors</strong>
      </p>
      <p class="cat-desc">
        Each entry is an idea: a thin market that the right matching infrastructure could open up.
        Any single idea can be argued with. The point is how many plausible ones there are, across
        unrelated sectors, places and kinds of participant. Click a title to read its summary.
      </p>
      <p class="idea-note" style="max-width: 60rem; margin-left: auto; margin-right: auto; text-align: left;">
        <strong>These are ideas, not built markets.</strong> None of the marketplaces described here
        exists yet. The story attached to each idea is fiction: its people and firms are invented to
        show how a match could work, and the market figures are estimates.
      </p>
      <p class="idea-note" style="max-width: 60rem; margin-left: auto; margin-right: auto; text-align: left;">
        <strong>Why ideas, and so many of them?</strong> The best evidence for this approach would be a
        collection of working, commercial marketplaces built with it. Assembling that would be costly
        and would take years. Working the approach through hundreds of different markets on paper was
        the method we could afford now: a low-cost check that the same reasoning holds up across
        unrelated sectors, each idea set out in enough detail to be argued with.
      </p>

      <!-- Search -->
      <div class="cat-search-wrap">
        <span class="cat-search-icon">&#128269;</span>
        <input id="cat-search" class="cat-search" type="search"
               placeholder="Search titles, summaries, tags and sectors&hellip;" autocomplete="off">
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

        <!-- List or cards -->
        <div class="view-btns" role="group" aria-label="Show as a list of titles or as cards">
          <button class="view-btn active" type="button" data-value="list">Titles</button>
          <button class="view-btn" type="button" data-value="cards">Cards</button>
        </div>

        <!-- Clear all -->
        <button class="btn-clear" id="btn-clear" type="button">&#10005; Clear filters</button>
      </div>

      <!-- Active filter chips -->
      <div class="filter-chips" id="filter-chips"></div>

      <!-- Count -->
      <div class="cat-count">
        Showing <span id="visible-count">{total}</span> of {total} ideas
      </div>

      <!-- Titles by sector, with the reading panel beside them -->
      <div class="cat-layout" id="cat-layout">
        <div>
          <div class="idea-groups" id="idea-groups">{groups_html}
          </div>
          <div class="cat-empty" id="no-results">No ideas match your search or filters.</div>
        </div>
        <aside class="idea-panel" id="idea-panel" aria-live="polite">
          <p class="idea-panel__empty"><strong>Click any title</strong> to read its summary here.
          The list stays in place, so you can move from one idea to the next; the up and down arrow
          keys do the same.</p>
        </aside>
      </div>
      <div class="idea-backdrop" id="idea-backdrop"></div>
    </div>
  </section>
{filter_js}
"""
    return head + content + renderFooter(root="../")


# ---------------------------------------------------------------------------
# Detail Page
# ---------------------------------------------------------------------------


def loadBlogStory(blog_slug):
    """Return (title, summary) from a blog post's frontmatter, or None if there is no such post.

    Used when a catalog idea's story lives on the blog: the catalog then shows the
    blog story's own title and summary, since the two versions can differ in
    characters and setting.
    """
    path = BLOG_POSTS_DIR / f"{blog_slug}.md"
    if not path.exists():
        return None
    match = re.search(r"^---\s*\n(.*?)\n---\s*\n", path.read_text(encoding="utf-8"), flags=re.DOTALL | re.MULTILINE)
    if not match:
        return None
    meta = yaml.safe_load(match.group(1)) or {}
    title = re.sub(r"^(?:Market Scenario|Workshop Notes)\s*[:\-\u2013\u2014]\s*", "", str(meta.get("title", "")))
    return title, str(meta.get("summary", ""))


_CARDS = None


def challengesPanel(slugs):
    """The idea's challenge tags (the `challenges:` list in its YAML), each linked to its card,
    with the interventions the matrix rates against them. The interventions are read from
    cards/cards.json, never stored on the idea, so they cannot drift from the canon."""
    global _CARDS
    if not slugs:
        return ""
    if _CARDS is None:
        import json
        cards = json.loads((SITE_ROOT / "cards" / "cards.json").read_text(encoding="utf-8"))["cards"]
        _CARDS = {c["slug"]: c for c in cards}
    link = 'style="display:inline-block; margin:0 0.4rem 0.4rem 0; text-decoration:none;"'
    chips, answers = [], []
    for slug in slugs:
        c = _CARDS.get(slug)
        if not c:
            continue
        chips.append(f'<a class="blog-tag" {link} href="../cards/index.html#{slug}" '
                     f'title="{escHtml(c["definition"])}">{escHtml(c["title"])}</a>')
        m = c.get("matrix", {})
        for name in m.get("strongest") or m.get("lowers") or []:
            if name not in answers:
                answers.append(name)
    if not chips:
        return ""
    return f"""
      <div class="panel-section">
        <div class="panel-section__label">Challenges That Bind It</div>
        <p style="margin-bottom:0.5rem;">{"".join(chips)}</p>
        <p style="font-size:0.875rem; color: var(--dp-silver);">Interventions the
        <a href="../intervention-matrix.html" style="color:#818cf8;">matrix</a> rates against them:
        {escHtml(", ".join(answers))}. Tagged by an AI model against the fifteen cards; most binding first.</p>
      </div>"""


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
    challenges_html = challengesPanel(s.get("challenges") or [])
    tab1 = f"""
      <div class="panel-section">
        <div class="panel-section__label">The Thin Market Problem</div>
        <p>{escHtml(me.get('problem', me.get('summary', '')))}</p>
      </div>
      <div class="panel-section">
        <div class="panel-section__label">Dominant Forces</div>
        <ul class="force-list">{forces_html}</ul>
      </div>{challenges_html}
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

    blog_story = loadBlogStory(story_blog_slug) if story_blog_slug else None
    if story_blog_slug and not blog_story:
        print(f"  WARNING {sid}: story.blog_slug '{story_blog_slug}' has no blog post; showing the inline story")
        story_blog_slug = ""

    if story_blog_slug:
        # The blog carries the full story, so the catalog does not repeat it
        # (owner's rule, 2026-11-21: blog stories take precedence over catalog stories).
        blog_url = f"../blog/{story_blog_slug}.html"
        blog_title, blog_summary = blog_story
        summary_html = f"<p>{escHtml(blog_summary)}</p>" if blog_summary else ""
        tab3 = f"""
      <div class="panel-section">
        <div class="panel-section__label">Narrative Story</div>
        <div class="panel-section__title">{escHtml(blog_title or story.get('title', ''))}</div>
        <p class="idea-note"><strong>This story is fiction.</strong> Its people and firms are invented to show how a match could work.</p>
        {summary_html}
        <p>The full story for this idea is told on the blog.</p>
        <p><a href="{blog_url}" class="story-blog-link">Read the full story on the blog &rarr;</a></p>
      </div>"""
    elif story_body_md:
        # Render inline markdown story
        story_html_body = markdownToHtml(story_body_md)
        blog_link = ""
        draft_banner = ""
        tab3 = f"""
      <div class="panel-section">
        <div class="panel-section__label">Narrative Story</div>
        <div class="panel-section__title">{escHtml(story.get('title', ''))}</div>
        <p class="idea-note"><strong>This story is fiction.</strong> Its people and firms are invented to show how a match could work.</p>
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
        <p>No story written yet for this idea.</p>
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
      <p class="idea-note"><strong>An idea, not a built market.</strong> This entry describes a marketplace that could exist; nobody has built it yet. The market figures are estimates and the story is fiction.</p>
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
# Redirect stubs for retired entries
# ---------------------------------------------------------------------------

REDIRECT_STUB = """<!-- Copyright (c) 2026 Mustafa Uzumeri. All rights reserved. -->
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Moved &mdash; DeeperPoint</title>
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="0; url=__TARGET__">
  <link rel="canonical" href="__CANONICAL__">
  <link rel="stylesheet" href="../styles.css">
</head>

<body data-pagefind-ignore>
  <section class="section" style="padding-top: calc(var(--space-4xl, 4rem) + 60px); text-align: center;">
    <div class="container container--narrow">
      <p style="color: var(--color-text-secondary, #cbd5e1); font-size: 1rem;">
        This catalog idea has been retired&hellip;
        <br><br>
        <a href="__TARGET__" style="color: #818cf8;">Click here if you are not redirected automatically.</a>
      </p>
    </div>
  </section>
  <script>window.location.replace("__TARGET__");</script>
</body>

</html>
"""


def buildRedirects(live_ids):
    """Write a redirect stub for every retired entry listed in catalog/redirects.yaml.

    The file maps an old entry id to a target path relative to catalog/. An id that
    is live again (its YAML is back in catalog/scenarios/) is skipped, so restoring
    an entry never fights its redirect.
    """
    if not REDIRECTS_FILE.exists():
        return 0
    mapping = yaml.safe_load(REDIRECTS_FILE.read_text(encoding="utf-8")) or {}
    written = 0
    for old_id, target in sorted(mapping.items()):
        if old_id in live_ids:
            print(f"  Redirect skipped (entry is live): {old_id}")
            continue
        target_path = (CATALOG_OUT / target).resolve()
        if not target_path.exists():
            print(f"  WARNING redirect {old_id}: target {target} does not exist")
        canonical = SITE_URL + "/" + target_path.relative_to(SITE_ROOT).as_posix()
        page = (
            REDIRECT_STUB
            .replace("__TARGET__", html.escape(target, quote=True))
            .replace("__CANONICAL__", canonical)
        )
        (CATALOG_OUT / f"{old_id}.html").write_text(page, encoding="utf-8")
        written += 1
    return written


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

    redirect_count = buildRedirects({s.get("id") for s in scenarios})
    if redirect_count:
        print(f"  Wrote: {redirect_count} redirect stubs from catalog/redirects.yaml")

    # The word index behind "What market should exist?" on the Home page.
    import build_idea_index
    build_idea_index.write_index(scenarios)

    print(f"Catalog build complete. {len(scenarios)} ideas published.")
    print(f"  Access at: {SITE_URL}/catalog/")


if __name__ == "__main__":
    main()
