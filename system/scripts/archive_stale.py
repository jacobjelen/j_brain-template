"""Staleness helpers for the digest.

  archive_stale.py bump   set last_used on notes listed in inbox items' brain_files_read
  archive_stale.py list   print memory/short notes idle > 180 days (archive candidates)
"""
import argparse
import glob
import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(__file__))
import fm  # noqa: E402

DAYS = 180


def _d(s):
    try:
        return date.fromisoformat(str(s)[:10])
    except ValueError:
        return None


def bump(root):
    changed = []
    for item in glob.glob(os.path.join(root, "inbox", "*.md")):
        with open(item, encoding="utf-8") as f:
            meta = fm.parse(f.read()) or {}
        when = _d(meta.get("captured", ""))
        files = meta.get("brain_files_read") or []
        if not when or not isinstance(files, list):
            continue
        for rel in files:
            p = os.path.join(root, rel)
            if not os.path.isfile(p):
                continue
            with open(p, encoding="utf-8") as f:
                text = f.read()
            note = fm.parse(text)
            if note is None:
                continue
            last = _d(note.get("last_used", ""))
            if last is None or when > last:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(fm.set_field(text, "last_used", when.isoformat()))
                changed.append(rel)
    return changed


def stale(root, today=None):
    today = today or date.today()
    cutoff = today - timedelta(days=DAYS)
    out = []
    for p in sorted(glob.glob(os.path.join(root, "memory", "short", "**", "*.md"), recursive=True)):
        rel = os.path.relpath(p, root)
        if rel == os.path.join("memory", "short", "now.md"):
            continue
        with open(p, encoding="utf-8") as f:
            meta = fm.parse(f.read()) or {}
        dates = [d for d in (_d(meta.get("updated", "")), _d(meta.get("last_used", ""))) if d]
        if dates and max(dates) < cutoff:
            out.append(rel)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["bump", "list"])
    ap.add_argument("--root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    for line in (bump(root) if a.cmd == "bump" else stale(root)):
        print(line)
