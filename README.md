<!-- Copyright (c) 2026 Mustafa Uzumeri. All rights reserved. -->
# deeperpoint.github.io

The public website for [DeeperPoint](https://deeperpoint.com) — engineering markets that work.

DeeperPoint is a self-funded, open research and engineering project exploring how AI can make thin markets thicker and more functional. The site is organised by the question a visitor arrives with: why markets stay thin, what we built, examples, who it's for, the library, the blog, about.

## Site Map

```
├── index.html                  # Landing page (hero + overview narrative)
├── market-physics.html         # Why Markets Stay Thin — thin market theory, a strip of the cards, the AI interventions
├── cards/                      # The fifteen resistance cards: synced from DeeperPointComms/library/resistance-cards, never edited here
├── platform.html               # Platform — the open-source engine, deal pipeline, Deal Brief
├── marketforge.html            # The Project — MarketForge integration overview
│   ├── mf-cosolvent.html       # Cosolvent — headless marketplace engine (MIT)
│   ├── mf-clientsynth.html     # ClientSynth — synthetic user populations for testing
│   └── mf-commoncontext.html        # CommonContext — AI-curated domain knowledge
├── whitepaper.html             # Full whitepaper on thin market theory
├── testbeds.html               # Thin market example summaries
├── examples.html               # Redirect to library.html#examples (the Examples hub merged into the Library, 2026-11-05)
├── library.html                # Library: the documents (whitepaper, cards and deck, matrix, ebook with its précis and pitch deck, mission) and the worked examples (catalog, test beds, MarketMaps, scenarios, diagnostic, demo)
├── contribute.html             # Contribute: the open door (nav button and footer link on every page)
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

Since 2026-11-05 the top-level navigation is organised by the question a visitor arrives with. The
logo is the link home. `update_nav.py` holds the list and rewrites the nav on every page (run it from
the site root after editing the list); `scripts/build_blog.py` and `scripts/build_catalog.py` carry
the same list in their templates and must be changed with it.

| Link | Page | Answers |
|------|------|---------|
| **Why Markets Don't Form** | `market-physics.html` | What a thin market is and why it stays thin: the theory, the fifteen cards (`cards/`), the intervention matrix, the whitepaper |
| **What We're Building** | `platform.html` | The open-source engine and everything under it: how it works, the demo, Cosolvent, CommonContext, MarketForge, ClientSynth, architecture |
| **Catalog** | `catalog/index.html` | The opportunity catalog, restored to the nav on 2026-11-05 at the owner's request |
| **Library** | `library.html` | The documents (whitepaper, cards and deck, matrix, ebook with its précis and pitch deck beneath it, mission essay, search) and the worked examples (test beds, MarketMaps, scenario stories, diagnostic, demo); Examples merged in on 2026-11-05 |
| **Blog** | `blog/index.html` | Updates and articles |
| **About** | `about.html` | About DeeperPoint and the author |
| *(hidden)* | `who-should-care.html`, `guide-*.html` | Who It's For and its five guides: out of the nav and the search index since 2026-11-05 as duplicative of the catalog; the pages remain |
| **Contribute** (button) | `contribute.html` | The open door: the public repos, the help that is not code, how to start. Also linked from every footer |

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

**To publish any change:** edit a file (an existing `.html` page, `styles.css`, a blog post, a catalog entry — anything), commit, and push to `master`:

```bash
git add <file>
git commit -m "Describe the change"
git push origin master
```

The push triggers GitHub Actions, which rebuilds and deploys the site to GitHub Pages at `deeperpoint.com`. No manual build is required before pushing — the Action runs the build steps for you.

Watch the run under the repo's **Actions** tab on GitHub. A deploy typically takes a minute or two; if a build step fails (e.g. malformed blog frontmatter or catalog YAML), the run goes red and the site is **not** updated. Concurrent pushes queue rather than cancel each other, so a new push waits for the in-progress deploy to finish.

You can also trigger a deploy manually from the Actions tab (the workflow allows `workflow_dispatch`) without pushing a commit.

### What the CI pipeline does

The pipeline (`.github/workflows/deploy.yml`) runs on push to `master` (Python 3.11) and:

1. Installs dependencies from `requirements.txt`
2. Runs `build_blog.py` — generates blog HTML + RSS from Markdown sources
3. Runs `build_catalog.py` — generates catalog pages from the scenario YAML files
4. Builds the full-text search index with Pagefind (`npx pagefind --site .`)
5. Deploys the entire repo root to GitHub Pages
