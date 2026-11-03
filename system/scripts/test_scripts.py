"""Self-check for the brain scripts. Run: python3 system/scripts/test_scripts.py"""
import glob
import json
import os
import sys
import tempfile
from datetime import date, datetime

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
tmp = tempfile.mkdtemp()
os.environ["BRAIN_CAPTURE_STATE"] = os.path.join(tmp, "state.json")

import archive_stale  # noqa: E402
import fm  # noqa: E402
import lint  # noqa: E402
import precheck  # noqa: E402
import recall  # noqa: E402
import transcript_to_inbox as tti  # noqa: E402


def w(rel, text):
    p = os.path.join(tmp, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    return p


def r(rel):
    with open(os.path.join(tmp, rel), encoding="utf-8") as f:
        return f.read()


# fm
t = "---\ntype: person\nsources: [raw/a.md, raw/b.md]   # c\nlast_used: 2026-01-01\n---\nbody"
assert fm.parse(t)["sources"] == ["raw/a.md", "raw/b.md"]
assert "last_used: 2026-05-05" in fm.set_field(t, "last_used", "2026-05-05")
assert fm.set_field(t, "last_used", "x").endswith("---\nbody")

# transcript capture: immutable chunks, only new messages each flush
os.makedirs(os.path.join(tmp, "inbox"))
lines = [
    {"type": "user", "message": {"role": "user", "content": [
        {"type": "text", "text": "<system-reminder>ctx</system-reminder>"},
        {"type": "text", "text": "plan a weekend with my wife"}]}},
    {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Read", "input": {"file_path": "/x/j_brain/memory/long/me.md"}},
        {"type": "text", "text": "Sure."}]}},
    {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "content": "..."}]}},
    {"type": "user", "message": {"role": "user", "content": "<system-reminder>x</system-reminder>"}},
    {"type": "user", "message": {"role": "user", "content": "she likes hiking"}},
    {"type": "response_item", "payload": {"type": "message", "role": "user",
                                          "content": [{"type": "input_text", "text": "and Italian food"}]}},
]
tp = w("t.jsonl", "\n".join(json.dumps(x) for x in lines[:2]) + "\n")
tti.note("claude-code", {"transcript_path": tp, "session_id": "abcdef1234", "cwd": "/c"})
assert tti.flush(tmp) == []                              # < 3 user turns: nothing yet
with open(tp, "a") as f:
    f.write("\n".join(json.dumps(x) for x in lines[2:]) + "\n")
out = tti.flush(tmp, datetime(2026, 10, 26, 14, 5))
assert len(out) == 1 and out[0].endswith("2026-10-26-1405-claude-code-abcdef12-m0.md"), out
chunk = open(out[0]).read()
meta = fm.parse(chunk)
assert meta["msg_end"] == "4" and meta["brain_files_read"] == ["memory/long/me.md"], meta
assert "tool_result" not in chunk and "system-reminder" not in chunk and "Italian" in chunk
assert "# plan a weekend with my wife" in chunk, chunk     # reminder stripped, message kept
assert tti.flush(tmp) == []                              # nothing new: no new file
with open(tp, "a") as f:
    f.write(json.dumps({"type": "user", "message": {"role": "user", "content": "budget 200 eur"}}) + "\n")
out2 = tti.flush(tmp, datetime(2026, 10, 26, 15, 0))
assert out2[0].endswith("-m4.md") and "budget" in open(out2[0]).read() and "hiking" not in open(out2[0]).read()

# archive_stale: bump last_used from inbox, list stale short notes
w("memory/long/me.md", "---\ntype: profile\nsummary: me\nupdated: 2026-01-01\nlast_used: 2026-01-01\n---\n")
w("memory/short/now.md", "---\ntype: now\nsummary: now\nupdated: 2020-01-01\nlast_used: 2020-01-01\n---\n")
w("memory/short/projects/old.md", "---\ntype: project\nsummary: old\nupdated: 2026-01-01\nlast_used: 2026-02-01\n---\n")
w("memory/short/projects/fresh.md", "---\ntype: project\nsummary: f\nupdated: 2026-09-01\nlast_used: 2026-09-01\n---\n")
assert archive_stale.bump(tmp) == ["memory/long/me.md"]
assert "last_used: 2026-10-26" in r("memory/long/me.md")
assert archive_stale.stale(tmp, date(2026, 10, 26)) == ["memory/short/projects/old.md"]

# lint: catches broken links, passes once fixed
w("raw/2026/10/s.md", "src")
w("memory/long/people/sam.md", "---\ntype: person\nsummary: John's wife\naliases: [Sam]\nupdated: 2026-10-26\nlast_used: 2026-10-26\n"
  "sources: [raw/2026/10/s.md]\n---\n## TL;DR\nWife. Loves hiking.\n\n## Current\n- Likes Novák's bakery [src](../../../raw/2026/10/s.md)\n"
  "- See [[memory/short/projects/gone]]\n")
probs = lint.check(tmp)
assert any("broken link [[memory/short/projects/gone]]" in p for p in probs), probs
w("memory/long/people/sam.md", r("memory/long/people/sam.md").replace("projects/gone", "projects/fresh"))
assert lint.check(tmp) == [], lint.check(tmp)

# recall: accent-insensitive, TL;DR not repeated, source paths shortened, inbox flagged, misses explained
out = recall.search(tmp, ["novak"])
assert out.startswith("memory/long/people/sam.md — John's wife"), out
assert "| Wife. Loves hiking." in out and out.count("Loves hiking") == 1 and "[src]" in out and "raw/2026" not in out, out
assert "UNDIGESTED" in recall.search(tmp, ["budget"])           # the transcript chunk still in inbox/
assert recall.search(tmp, ["zzz"]).startswith("no matches")
assert recall.catalogue(tmp, "people") == "memory/long/people/sam.md — John's wife"

# precheck: work while inbox/stale/lint have something, NOTHING TO DO once clear
assert precheck.pending(tmp)[0].startswith("inbox: ")
for p in glob.glob(os.path.join(tmp, "inbox", "*")):
    os.remove(p)
os.remove(os.path.join(tmp, "memory/short/projects/old.md"))
assert precheck.pending(tmp) == [], precheck.pending(tmp)

print("ok")
