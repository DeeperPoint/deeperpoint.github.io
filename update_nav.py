"""Rewrite the site navigation on every page that carries one.

Edit NAV (and CTA), then run `python update_nav.py` from the site root. Every HTML file under the
site whose nav holds a `<ul class="nav__links">` block gets the block replaced, with hrefs made
relative to the file's depth and the active item chosen from the file's path. The blog and catalog
builders carry the same nav in their own templates (scripts/build_blog.py, scripts/build_catalog.py):
change those too when NAV changes, or the next rebuild reverts their pages.

Since 2026-11-05 the nav is organised by the question a visitor arrives with. Who It's For and its
five guides are hidden from the nav and the search index since 2026-11-05 (owner: duplicative of the
catalog); the pages remain at their URLs. Who It's For and its
five guides are hidden from the nav and the search index since 2026-11-05 (owner: duplicative of the
catalog); the pages remain at their URLs. Each item is
(label, target, also-active): the pages on which the item shows as current besides its target,
given as exact paths or as a folder with a trailing slash. CTA is the one button at the end of the
nav, styled by `.nav__link--cta` in styles.css.
"""
import os
import re

NAV = [
    ("Why Markets Don&rsquo;t Form", "market-physics.html",
     ["intervention-matrix.html", "whitepaper.html", "cards/"]),
    ("What We&rsquo;re Building", "platform.html",
     ["how-it-works.html", "demo.html", "cosolvent.html", "marketforge.html", "mf-cosolvent.html",
      "mf-commoncontext.html", "mf-clientsynth.html", "architecture.html"]),
    ("Catalog", "catalog/index.html", ["catalog/"]),
    ("Library", "library.html",
     ["ebook.html", "precis.html", "pitch-deck.html", "search.html", "testbeds.html", "marketmaps.html",
      "market-diagnostic.html", "examples.html"]),
    ("Blog", "blog/index.html", ["blog/"]),
    ("About", "about.html", ["mission.html"]),
]
CTA = ("Contribute", "contribute.html", [])

NAV_RE = re.compile(r'^[ \t]*<ul class="nav__links">.*?</ul>', re.MULTILINE | re.DOTALL)


def is_active(current: str, target: str, also: list[str]) -> bool:
    for a in [target] + list(also):
        if a.endswith("/"):
            if current.startswith(a):
                return True
        elif current == a:
            return True
    return False


def build_nav(current: str) -> str:
    depth = current.count("/")
    prefix = "../" * depth
    lines = ['      <ul class="nav__links">']
    for label, target, also in NAV:
        active = " nav__link--active" if is_active(current, target, also) else ""
        lines.append(f'        <li><a href="{prefix}{target}" class="nav__link{active}">{label}</a></li>')
    label, target, also = CTA
    active = " nav__link--active" if is_active(current, target, also) else ""
    lines.append(f'        <li><a href="{prefix}{target}" class="nav__link nav__link--cta{active}">{label}</a></li>')
    lines.append("      </ul>")
    return "\n".join(lines)


def main() -> None:
    updated = 0
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(root, name).replace(os.sep, "/").removeprefix("./")
            with open(path, encoding="utf-8", newline="") as fh:
                content = fh.read()
            if 'class="nav__links"' not in content:
                continue
            nl = "\r\n" if "\r\n" in content else "\n"
            new_nav = build_nav(path).replace("\n", nl)
            new_content = NAV_RE.sub(lambda _m: new_nav, content)
            if new_content != content:
                with open(path, "w", encoding="utf-8", newline="") as fh:
                    fh.write(new_content)
                updated += 1
    print(f"Updated {updated} files.")


if __name__ == "__main__":
    main()
