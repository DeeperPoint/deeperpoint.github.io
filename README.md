<!-- Copyright (c) 2026 Mustafa Uzumeri. All rights reserved. -->
# deeperpoint.github.io

The public website for [DeeperPoint](https://deeperpoint.com) — engineering markets that work.

DeeperPoint is a self-funded, open research and engineering project exploring how AI can make thin markets thicker and more functional. The site follows a **Problem → Project → Evidence → About** narrative flow.

## Site Map

```
├── index.html                  # Landing page (hero + overview narrative)
├── thin-markets.html           # The Problem — thin market theory explained
├── marketforge.html            # The Project — MarketForge integration overview
│   ├── mf-cosolvent.html       # Cosolvent — marketplace scaffolding framework (MIT)
│   ├── mf-clientsynth.html     # ClientSynth — synthetic user populations for testing
│   └── mf-curation.html        # KnowledgeSlot — AI-curated domain knowledge
├── whitepaper.html             # Full whitepaper on thin market theory
├── testbeds.html               # Thin market example summaries
├── testbeds-detail.html        # 20 detailed thin market analyses
├── market-diagnostic.html      # Interactive Market Engineer's Diagnostic Checklist
├── blog/
│   ├── posts/                  # Markdown blog posts (source)
│   ├── index.html              # Blog listing (generated)
│   ├── feed.xml                # RSS feed (generated)
│   └── *.html                  # Individual posts (generated)
├── about.html                  # About DeeperPoint & author
├── docs/                       # Internal design notes & migration reference
├── scripts/
│   ├── build_blog.py           # Markdown → HTML blog build script
│   └── post_to_linkedin.py     # LinkedIn cross-posting utility
├── styles.css                  # Shared design system
├── reveal.js                   # Scroll-reveal animation
├── assets/
│   ├── images/                 # General site images
│   └── myimages/               # Project-specific diagrams (e.g. MarketForge workflow)
├── requirements.txt            # Python dependencies (markdown, pyyaml, requests)
└── .github/workflows/
    └── deploy.yml              # GitHub Actions — build blog + deploy to Pages
```

## Navigation

The top-level navigation follows a guided narrative:

| Link | Page | Purpose |
|------|------|---------|
| **The Problem** | `thin-markets.html` | Explain thin market theory and the forces that prevent markets from working |
| **The Project** | `marketforge.html` | Introduce MarketForge and its component tools (Cosolvent, ClientSynth, KnowledgeSlot) |
| **Blog** | `blog/index.html` | Updates and articles |
| **About** | `about.html` | About DeeperPoint and the author |

## Blog Workflow

1. Write a post in `blog/posts/your-post.md` with YAML frontmatter
2. Run `python scripts/build_blog.py` (or push to `master` to trigger GitHub Actions)
3. Optionally cross-post to LinkedIn: `python scripts/post_to_linkedin.py your-post-slug`

## Local Preview

Open any `.html` file directly in a browser, or use a local server:

```bash
python -m http.server 8000
```

## Deployment

Push to `master` → GitHub Actions builds blog → deploys to GitHub Pages → serves at `deeperpoint.com`.

The CI pipeline (`.github/workflows/deploy.yml`) runs on Python 3.11 and:

1. Installs dependencies from `requirements.txt`
2. Runs `build_blog.py` to generate blog HTML from Markdown sources
3. Deploys the entire repo root to GitHub Pages
