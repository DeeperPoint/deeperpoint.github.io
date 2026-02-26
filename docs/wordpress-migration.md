<!-- Copyright (c) 2026 Mustafa Uzumeri. All rights reserved. -->

# WordPress Migration Guide

How to rescue your existing WordPress blog posts and convert them to Markdown for the new blog.

## Step 1: Export from WordPress

1. Log into your WordPress admin panel at `deeperpoint.com/wp-admin`
2. Go to **Tools → Export**
3. Select **All content**
4. Click **Download Export File**
5. Save the `.xml` file somewhere accessible (e.g., `~/Downloads/deeperpoint-export.xml`)

## Step 2: Convert to Markdown

Install and run the open-source converter:

```bash
npx wordpress-export-to-markdown --input ~/Downloads/deeperpoint-export.xml --output ./blog/posts/
```

Options you may want:

- `--post-folders false` — flat file output (recommended for our structure)
- `--include-other-types false` — skip pages, only export posts
- `--save-attached-images true` — download images referenced in posts

## Step 3: Review and Clean Frontmatter

The converter generates frontmatter like:

```yaml
---
title: "Your Post Title"
date: 2024-03-15
---
```

You need to add the fields our build script expects:

```yaml
---
title: "Your Post Title"
date: 2024-03-15
tags: [thin-markets, trade]
summary: "A one-sentence summary for the blog index and Open Graph previews."
author: Mustafa Uzumeri
slug: your-post-title
---
```

**Tips:**

- `slug` should match the filename (without `.md`)
- `tags` should use lowercase, hyphenated terms
- `summary` appears on the blog index page and in LinkedIn/social previews — make it compelling

## Step 4: Handle Images

If your WordPress posts contain images:

1. The converter downloads them alongside the Markdown files
2. Move images to `assets/blog/` in the repo
3. Update image paths in the Markdown files from the converter's path to `../assets/blog/filename.png`

## Step 5: Build and Verify

```bash
python scripts/build_blog.py
```

Then open `blog/index.html` in a browser to verify all posts appear correctly.

## Step 6: Set Up URL Redirects (Optional)

If your WordPress posts had URLs like `deeperpoint.com/2024/03/my-post/`, you'll want redirects so existing links don't break.

Create redirect HTML files at the old paths:

```html
<!-- blog/2024/03/my-post/index.html -->
<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="refresh" content="0; url=/blog/my-post.html">
  <link rel="canonical" href="https://deeperpoint.com/blog/my-post.html">
</head>
<body>
  <p>Redirecting to <a href="/blog/my-post.html">the new location</a>...</p>
</body>
</html>
```

This preserves SEO and prevents broken links from search engines or external sites.

## Step 7: Cancel Lightsail

Once you've verified:

1. DNS has propagated to GitHub Pages
2. All old posts are migrated and accessible
3. Redirects work for any important old URLs

Then you can cancel the Lightsail instance.
