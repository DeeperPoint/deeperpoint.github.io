<!-- Copyright (c) 2026 Mustafa Uzumeri. All rights reserved. -->
# deeperpoint.github.io

The public website for [DeeperPoint](https://deeperpoint.com) — engineering markets that work.

## Structure

```
├── index.html              # Landing page
├── about.html              # About DeeperPoint
├── spoke-science.html      # The Science path
├── spoke-build.html        # Build Your Market path
├── spoke-matching.html     # Solve Matching path
├── marketforge.html        # MarketForge overview
├── mf-*.html               # MarketForge sub-pages
├── blog/
│   ├── posts/              # Markdown blog posts (source)
│   ├── index.html          # Blog listing (generated)
│   ├── feed.xml            # RSS feed (generated)
│   └── *.html              # Individual posts (generated)
├── scripts/
│   ├── build_blog.py       # Markdown → HTML build script
│   └── post_to_linkedin.py # LinkedIn cross-posting
├── styles.css              # Shared design system
├── reveal.js               # Scroll reveal animation
└── assets/                 # Images, icons
```

## Blog Workflow

1. Write a post in `blog/posts/your-post.md` with YAML frontmatter
2. Run `python scripts/build_blog.py` (or push to `main` to trigger GitHub Actions)
3. Optionally cross-post to LinkedIn: `python scripts/post_to_linkedin.py your-post-slug`

## Local Preview

Open any `.html` file directly in a browser, or use a local server:

```bash
python -m http.server 8000
```

## Deployment

Push to `main` → GitHub Actions builds blog → deploys to GitHub Pages → serves at `deeperpoint.com`.
