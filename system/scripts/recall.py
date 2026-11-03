"""Search the brain cheaply: matching notes' summary + TL;DR + matched lines, not whole files.

  recall.py maya acme-app        notes matching any term, best first (all terms matched ranks top)
  recall.py --list                 one line per note: path — summary (the catalogue, on demand)
  recall.py --list people          the same, only paths containing "people"

Searches memory/ and inbox/ (undigested, newer than the notes). Never archive/ or raw/.
Case- and accent-insensitive: "novak" finds "Novák".
"""
import argparse
import glob
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(__file__))
import fm  # noqa: E402

MAX_NOTES = 6
MAX_LINES = 4      # matched lines shown per note
TLDR_LINES = 5
SRC = re.compile(r"\[src\]\([^)]*\)")   # source paths: in the note when needed, noise in a search


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))


def tldr(text):
    out, on = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            if on:
                break
            on = line.strip() == "## TL;DR"
            continue
        if on and line.strip():
            out.append(line.strip())
    return out[:TLDR_LINES]


def load(root, folder):
    for p in sorted(glob.glob(os.path.join(root, folder, "**", "*.md"), recursive=True)):
        with open(p, encoding="utf-8") as f:
            yield os.path.relpath(p, root), f.read()


def score(rel, text, terms):
    meta = fm.parse(text) or {}
    aliases = meta.get("aliases") or []
    head = norm(" ".join([rel, str(meta.get("summary", "")), " ".join(aliases) if isinstance(aliases, list) else str(aliases)]))
    body = norm(text)
    hit = [t for t in terms if t in body or t in head]
    if not hit:
        return None
    # all terms beat some terms; a hit in path/summary/aliases beats a mention in the body
    return (len(hit), sum(t in head for t in hit), sum(body.count(t) for t in hit))


def matched_lines(text, terms):
    out, seen = [], set(tldr(text))
    fm_end = text.find("\n---\n", 4) + 5 if text.startswith("---\n") else 0
    for i, line in enumerate(text[fm_end:].splitlines(), 1 + text[:fm_end].count("\n")):
        s = line.strip()
        if s and not s.startswith("#") and s not in seen and any(t in norm(s) for t in terms):
            out.append(f"  L{i}: {SRC.sub('[src]', s)[:200]}")
    return out[:MAX_LINES]


def search(root, terms, limit=MAX_NOTES):
    terms = [norm(t) for t in terms if t.strip()]
    hits = []
    for folder in ("memory", "inbox"):
        for rel, text in load(root, folder):
            s = score(rel, text, terms)
            if s:
                hits.append((s, rel, text))
    hits.sort(key=lambda h: h[0], reverse=True)
    out = []
    for (n, _, _), rel, text in hits[:limit]:
        meta = fm.parse(text) or {}
        if rel.startswith("inbox/"):
            out.append(f"{rel}  [UNDIGESTED, newer than notes]  ({n}/{len(terms)} terms)")
        else:
            out.append(f"{rel} — {meta.get('summary', '')}  (updated {meta.get('updated', '?')}, {n}/{len(terms)} terms)")
            out += [f"  | {l}" for l in tldr(text)]
        out += matched_lines(text, terms)
    if len(hits) > limit:
        out.append(f"(+{len(hits) - limit} more matches: narrow the terms or raise --limit)")
    return "\n".join(out) or "no matches (try other spellings/aliases; then write a kind: gap inbox item)"


def catalogue(root, filt=""):
    lines = []
    for rel, text in load(root, "memory"):
        if norm(filt) in norm(rel):
            lines.append(f"{rel} — {(fm.parse(text) or {}).get('summary', '')}")
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--limit", type=int, default=MAX_NOTES)
    ap.add_argument("--root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    if a.list:
        print(catalogue(root, " ".join(a.terms)))
    elif a.terms:
        print(search(root, a.terms, a.limit))
    else:
        ap.print_help()
