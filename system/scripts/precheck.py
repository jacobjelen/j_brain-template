"""Cheap gate before the digest: is there anything to do today?

Prints NOTHING TO DO (exit 0) when the inbox is empty, no short-term note is stale and lint passes,
so the routine can stop before reading any rules. Otherwise prints what is waiting.
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import archive_stale  # noqa: E402
import lint  # noqa: E402


def pending(root):
    inbox = [p for p in glob.glob(os.path.join(root, "inbox", "*")) if not p.endswith(".gitkeep")]
    stale = archive_stale.stale(root)
    problems = lint.check(root)
    out = []
    if inbox:
        out.append(f"inbox: {len(inbox)} item(s)")
    if stale:
        out.append(f"stale: {len(stale)} note(s) to archive")
    if problems:
        out.append(f"lint: {len(problems)} problem(s)")
    return out


if __name__ == "__main__":
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    print("\n".join(pending(root)) or "NOTHING TO DO")
