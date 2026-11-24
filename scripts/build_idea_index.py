# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.
"""
build_idea_index.py — the word index behind "What market should exist?" on the Home page.

The Home page box (your-market.js) matches a visitor's sentence against the catalog ideas
entirely in the browser: no model, no server, nothing sent. This script writes the file it
loads, catalog/idea-index.json:

  docs       one row per published idea: id, title, sector, a short summary, and the three
             frictions its write-up leans on most (indexes into `frictions`)
  postings   term -> [doc, weight, doc, weight, ...]; the weight is the finished BM25 score
             of that term in that idea, so the browser only adds numbers up
  frictions  the fifteen cards (slug, title, definition) with the word list that marks each

Two things here are rules of thumb, and the page says so:

  * The match is on words, after a crude stemmer. stem() below and stem() in your-market.js
    must stay identical; `python scripts/build_idea_index.py --stems` prints a sample the
    JavaScript can be checked against.
  * An idea's frictions are its `challenges:` tags (added 2026-11-24, by Claude Opus 5.5
    against the fifteen cards). An idea without tags falls back to a count of its own text
    against the LEXICON below. The LEXICON also catches a friction the visitor names outright.

Run by scripts/build_catalog.py at the end of every catalog build, and on its own:
    python scripts/build_idea_index.py
"""
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
SCENARIOS_DIR = ROOT / "catalog" / "scenarios"
CARDS_JSON = ROOT / "cards" / "cards.json"
OUT = ROOT / "catalog" / "idea-index.json"

# How much a word counts by where it appears in the idea.
FIELD_WEIGHT = {"title": 3.0, "tags": 3.0, "sub_sector": 2.0, "sector": 2.0, "summary": 2.0,
                "problem": 1.0, "forces": 1.0}
K1, B = 1.2, 0.75
MAX_DF = 0.5            # a word in more than half the ideas tells them apart too little to keep

STOP = set("""
a about above after again against all also am an and any are aren as at be because been before
being below between both but by can cannot could did do does doing don down during each few for
from further had has have having he her here hers him his how i if in into is it its itself just
me more most my no nor not now of off on once only or other our ours out over own same she should
so some such than that the their theirs them then there these they this those through to too
under until up very was we were what when where which while who whom why will with would you your
yours need needs want wants like get one two may might must new use used using make makes made
market markets marketplace platform match matching matches connect connecting connects find
finding people someone something thing things way ways help helps via per etc
""".split())


def stem(w):
    """A crude stemmer. Keep it identical to stem() in your-market.js."""
    if len(w) > 4 and w.endswith("ies"):
        return w[:-3] + "y"
    if len(w) > 5 and w.endswith("sses"):
        return w[:-2]
    if len(w) > 6 and w.endswith("ing"):
        return w[:-3]
    if len(w) > 5 and w.endswith("ed"):
        return w[:-2]
    if len(w) > 5 and w.endswith("ers"):
        return w[:-1]
    if len(w) > 4 and w.endswith("es") and not w.endswith("ses"):
        return w[:-2]
    if len(w) > 3 and w.endswith("s") and not w.endswith("ss") and not w.endswith("us"):
        return w[:-1]
    return w


def tokens(text):
    """Lower-case words of three letters or more, stop words out, stemmed."""
    out = []
    for w in re.findall(r"[a-z][a-z0-9]+", str(text or "").lower().replace("’", "'")):
        if len(w) < 3 or w in STOP:
            continue
        out.append(stem(w))
    return out


# The words that mark each friction. Single words only; they are stemmed like everything else.
LEXICON = {
    "trust": "trust trusted credibility credible reputation verify verification vetting vetted "
             "fraud stranger strangers confidence counterparty unknown unproven references",
    "risk": "risk risks risky liability failure fail insurance uninsured exposure guarantee "
            "warranty untested downside",
    "regulatory-friction": "regulatory regulation regulations regulator regulators certification "
                           "certified licence license licensing licensed compliance permit permits "
                           "approval accreditation accredited jurisdiction statute bylaw audit",
    "geopolitical-trade-volatility": "tariff tariffs sanction sanctions geopolitical embargo border "
                                     "customs export exports exporter import imports importer "
                                     "corridor war bilateral",
    "macro-fx-exposure": "currency inflation volatility volatile hedge hedging recession repriced "
                         "devaluation",
    "opacity": "invisible hidden visibility discover discovery directory unlisted opaque opacity "
               "undocumented unadvertised referral referrals network networks unaware unseen",
    "decision-process-opacity": "procurement committee board stakeholder stakeholders signoff "
                                "budget consensus approvals bureaucracy tender rfp purchasing",
    "geographic-distance": "remote rural distance distant kilometre kilometres northern region "
                           "regional travel dispersed isolated province provinces interprovincial",
    "temporal-distance": "seasonal season timing window windows schedule scheduling perishable "
                         "deadline idle availability urgent backlog queue waitlist short-notice",
    "offering-complexity": "specialized specialised specialist specialists bespoke custom complex "
                           "niche expertise combination multidisciplinary unique specification "
                           "technical rare",
    "cold-start": "bootstrap liquidity adoption adopters chicken traction",
    "cognitive-bandwidth": "overwhelmed overwhelm overload navigate navigation choices options "
                           "paperwork sift confusing eligibility "
                           "intake",
    "fulfillment": "logistics shipping shipment delivery deliver freight transport warehouse "
                   "storage minimum carrier haul trucking cold-chain refrigerated packaging",
    "participant-fragmentation": "small smallholder smallholders fragmented fragmentation scattered "
                                 "cooperative consortium aggregate aggregation pooled pool scale "
                                 "independent micro volume",
    "technological-obsolescence": "obsolete obsolescence legacy outdated upgrade payback "
                                  "depreciation discontinued",
}


def load_ideas():
    ideas = []
    for f in sorted(SCENARIOS_DIR.glob("*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        if d.get("hidden") is True or d.get("status") != "published":
            continue
        ideas.append(d)
    return ideas


def first_sentence(text, limit=210):
    text = " ".join(str(text or "").split())
    m = re.match(r"(.{40,}?[.!?])(\s|$)", text)
    s = m.group(1) if m else text
    if len(s) > limit:
        s = s[:limit].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"
    return s


def build(ideas):
    cards = json.loads(CARDS_JSON.read_text(encoding="utf-8"))["cards"]
    frictions = [{"slug": c["slug"], "title": c["title"], "definition": c["definition"],
                  "terms": sorted({stem(w.replace("-", "")) for w in LEXICON[c["slug"]].split()})}
                 for c in cards]
    term_to_friction = defaultdict(set)
    for i, f in enumerate(frictions):
        for t in f["terms"]:
            term_to_friction[t].add(i)

    docs, tfs, lens, friction_raw = [], [], [], []
    for d in ideas:
        me = d.get("market_example") or {}
        fields = {
            "title": f"{d.get('title', '')} {d.get('card_title', '')}",
            "tags": " ".join(d.get("tags") or []),
            "sub_sector": d.get("sub_sector", ""),
            "sector": str(d.get("sector", "")).replace("-", " "),
            "summary": me.get("summary", ""),
            "problem": me.get("problem", ""),
            "forces": " ".join(me.get("dominant_forces") or []),
        }
        tf = Counter()
        for name, text in fields.items():
            for t in tokens(text):
                tf[t] += FIELD_WEIGHT[name]
        tfs.append(tf)
        lens.append(sum(tf.values()))

        body = tokens(" ".join([fields["summary"], fields["problem"], fields["forces"]]))
        hits = Counter()
        for t in body:
            for i in term_to_friction.get(t, ()):
                hits[i] += 1
        friction_raw.append([hits[i] / max(len(body), 1) for i in range(len(frictions))])

        docs.append({
            "id": d["id"],
            "title": d.get("card_title") or d.get("title"),
            "sector": str(d.get("sector", "")).replace("-", " ").title(),
            "summary": first_sentence(me.get("summary")),
        })

    # An idea's frictions: the ones its text leans on more than the catalog as a whole does.
    n = len(docs)
    for i in range(len(frictions)):
        col = [row[i] for row in friction_raw]
        mean = sum(col) / n
        sd = math.sqrt(sum((x - mean) ** 2 for x in col) / n) or 1.0
        for row in friction_raw:
            row[i] = (row[i] - mean) / sd
    slug_index = {f["slug"]: i for i, f in enumerate(frictions)}
    for d, doc, row in zip(ideas, docs, friction_raw):
        tagged = [slug_index[s] for s in (d.get("challenges") or []) if s in slug_index]
        if tagged:                       # the idea's own tags win over the word count
            doc["frictions"] = tagged[:3]
            continue
        ranked = sorted(range(len(row)), key=lambda i: -row[i])
        doc["frictions"] = [i for i in ranked[:3] if row[i] > 0.5]

    # How common each friction is across the catalog, and so how much it tells one idea from
    # another. Opacity binds nearly every idea; the page says so once instead of listing it
    # every time, and ranks the rest by `weight`.
    held = Counter(i for doc in docs for i in doc["frictions"])
    for i, f in enumerate(frictions):
        f["share"] = round(held[i] / n, 2)
        f["weight"] = round(min(math.log(n / held[i]), 2.5), 2) if held[i] else 0.0   # capped: one rare tag must not swamp the rest

    df = Counter()
    for tf in tfs:
        df.update(tf.keys())
    avg = sum(lens) / n
    postings = defaultdict(list)
    for di, tf in enumerate(tfs):
        for t, f in tf.items():
            if df[t] > MAX_DF * n:
                continue
            idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
            w = idf * f * (K1 + 1) / (f + K1 * (1 - B + B * lens[di] / avg))
            postings[t] += [di, round(w, 2)]

    return {"count": n, "docs": docs, "frictions": frictions,
            "postings": dict(sorted(postings.items()))}


def write_index(ideas=None):
    # Sorted, so the file is the same whether this runs alone or from the catalog build.
    index = build(sorted(ideas if ideas is not None else load_ideas(), key=lambda d: d["id"]))
    OUT.write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"  Wrote: catalog/idea-index.json ({index['count']} ideas, "
          f"{len(index['postings'])} terms, {OUT.stat().st_size // 1024} KB)")
    return index


if __name__ == "__main__":
    if "--stems" in sys.argv:
        words = sorted({w for d in load_ideas() for w in re.findall(r"[a-z][a-z0-9]+", json.dumps(d).lower())})
        print(json.dumps({w: stem(w) for w in words}))
    else:
        write_index()
