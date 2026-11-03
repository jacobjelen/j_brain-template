"""Check the brain's integrity. Reports problems, exits 1 if any."""
import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import fm  # noqa: E402

REQUIRED = ("type", "summary", "updated", "last_used")
WIKILINK = re.compile(r"\[\[([^\]|#]+)")
MDLINK = re.compile(r"\]\(((?:\.\./)*raw/[^)\s]+)\)")


def notes(root):
    return sorted(os.path.relpath(p, root)
                  for p in glob.glob(os.path.join(root, "memory", "**", "*.md"), recursive=True))


def check(root):
    problems = []
    for rel in notes(root):
        path = os.path.join(root, rel)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        meta = fm.parse(text)
        if meta is None:
            problems.append(f"{rel}: missing frontmatter")
            continue
        for k in REQUIRED:
            if not meta.get(k):
                problems.append(f"{rel}: frontmatter missing '{k}'")
        for src in meta.get("sources") or []:
            if not os.path.exists(os.path.join(root, src)):
                problems.append(f"{rel}: source not found: {src}")
        for target in WIKILINK.findall(text):
            t = target.strip()
            if not any(os.path.exists(os.path.join(root, t + ext)) for ext in ("", ".md", "/README.md")):
                problems.append(f"{rel}: broken link [[{t}]]")
        for link in MDLINK.findall(text):
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), link))):
                problems.append(f"{rel}: broken source link {link}")
    return problems


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    problems = check(root)
    print("\n".join(problems) or "ok")
    sys.exit(1 if problems else 0)
