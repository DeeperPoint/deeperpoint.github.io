# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.

"""
LinkedIn Cross-Post Script for DeeperPoint Blog

Posts a blog article to LinkedIn via the Posts API.

Setup:
    1. Create a LinkedIn Developer App at https://developer.linkedin.com/
    2. Request 'w_member_social' permission (for personal profile posting)
       or 'w_organization_social' (for company page posting)
    3. Generate an OAuth 2.0 access token
    4. Create a .env file in the repo root with:
         LINKEDIN_ACCESS_TOKEN=your_token_here
         LINKEDIN_PERSON_ID=your_person_urn  (e.g., "urn:li:person:ABC123")

Usage:
    python scripts/post_to_linkedin.py why-thin-markets-fail

Notes:
    - LinkedIn access tokens expire (typically 60 days).
    - The script will detect expiry and print renewal instructions.
    - For company page posting, use LINKEDIN_ORG_ID instead of PERSON_ID.
"""

import re
import sys
from pathlib import Path

import requests
import yaml

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SITE_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = SITE_ROOT / "blog" / "posts"
ENV_FILE = SITE_ROOT / ".env"
SITE_URL = "https://deeperpoint.com"
API_URL = "https://api.linkedin.com/v2/posts"


def loadEnv():
    """Load environment variables from .env file."""
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip()
    return env


def parsePost(slug):
    """Read and parse a blog post Markdown file."""
    filepath = POSTS_DIR / f"{slug}.md"
    if not filepath.exists():
        print(f"Error: Post not found: {filepath}")
        sys.exit(1)

    text = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not match:
        print("Error: No YAML frontmatter found.")
        sys.exit(1)

    meta = yaml.safe_load(match.group(1))
    return meta


def postToLinkedIn(meta, env):
    """Create a LinkedIn post with article link."""
    token = env.get("LINKEDIN_ACCESS_TOKEN")
    author = env.get("LINKEDIN_PERSON_ID")

    if not token:
        print("Error: LINKEDIN_ACCESS_TOKEN not found in .env")
        print("See the docstring in this script for setup instructions.")
        sys.exit(1)

    if not author:
        print("Error: LINKEDIN_PERSON_ID not found in .env")
        sys.exit(1)

    postUrl = f"{SITE_URL}/blog/{meta['slug']}.html"

    # Build the post payload
    payload = {
        "author": author,
        "commentary": (
            f"{meta['title']}\n\n"
            f"{meta['summary']}\n\n"
            f"Read the full post: {postUrl}\n\n"
            + " ".join(f"#{tag.replace('-', '')}" for tag in meta["tags"])
        ),
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "content": {
            "article": {
                "source": postUrl,
                "title": meta["title"],
                "description": meta["summary"],
            }
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202402",
    }

    print(f"Posting to LinkedIn: {meta['title']}")
    print(f"  URL: {postUrl}")

    response = requests.post(API_URL, json=payload, headers=headers, timeout=30)

    if response.status_code == 201:
        print("  Success! Post published to LinkedIn.")
        postId = response.headers.get("x-restli-id", "unknown")
        print(f"  Post ID: {postId}")
    elif response.status_code == 401:
        print("  Error 401: Access token expired or invalid.")
        print("  Regenerate your token at https://developer.linkedin.com/")
        print("  Then update LINKEDIN_ACCESS_TOKEN in .env")
    else:
        print(f"  Error {response.status_code}: {response.text}")

    return response.status_code


def main():
    """Cross-post a blog article to LinkedIn."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/post_to_linkedin.py <slug>")
        print("Example: python scripts/post_to_linkedin.py why-thin-markets-fail")
        sys.exit(1)

    slug = sys.argv[1]
    env = loadEnv()
    meta = parsePost(slug)
    postToLinkedIn(meta, env)


if __name__ == "__main__":
    main()
