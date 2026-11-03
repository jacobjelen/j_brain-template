"""Capture Claude Code / Codex session transcripts (JSONL) into inbox/ as immutable chunks.

  transcript_to_inbox.py note  --source codex   < hook-json   remember this session's transcript path
  transcript_to_inbox.py flush --root <brain>                  write new messages of every known session

Chunks are never rewritten: each flush writes only messages since the previous flush as a new file
(inbox/<when>-<source>-<session>-m<start>.md). The cloud digest moves inbox files into raw/, so
rewriting a file it already took would cause git conflicts; immutable chunks avoid that entirely.
Local progress per session lives outside the repo in ~/.j_brain-capture.json.
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import datetime

MIN_USER_TURNS = 3          # sessions shorter than this are never captured
MAX_ASSISTANT_CHARS = 300   # agent replies are trimmed hard (most tokens, few facts); John's words are kept whole
FORGET_AFTER = 7 * 86400    # drop sessions from state after a week without changes
STATE = os.environ.get("BRAIN_CAPTURE_STATE", os.path.expanduser("~/.j_brain-capture.json"))
BRAIN_PATH = re.compile(r"j_brain/((?:memory|system/rules)/[^\s\"'\\)]+?\.md)")


INJECTED = re.compile(r"<(system-reminder|environment_context|command-[\w-]+)>.*?</\1>", re.S)


def _text(content):
    """Message text minus harness injections (system reminders etc.), which ride along in user turns."""
    if not isinstance(content, str):
        content = "\n".join(c.get("text", "") for c in content or []
                            if isinstance(c, dict) and c.get("type") in ("text", "input_text", "output_text"))
    return INJECTED.sub("", content)


def parse_transcript(lines):
    """Return (messages [(role, text)], brain files read)."""
    msgs, read = [], set()
    for raw in lines:
        try:
            e = json.loads(raw)
        except ValueError:
            continue
        read.update(BRAIN_PATH.findall(raw))
        if e.get("type") in ("user", "assistant") and isinstance(e.get("message"), dict):  # Claude Code
            if e.get("isMeta") or e.get("isSidechain"):
                continue
            role, content = e["type"], e["message"].get("content")
        elif e.get("type") == "response_item" and (e.get("payload") or {}).get("type") == "message":  # Codex
            role, content = e["payload"].get("role"), e["payload"].get("content")
        else:
            continue
        text = _text(content).strip()
        # Skip tool results, hook/system injections and empty turns.
        if role not in ("user", "assistant") or not text or text.startswith(("<", "Caveat:", "# AGENTS.md")):
            continue
        if role == "assistant" and len(text) > MAX_ASSISTANT_CHARS:
            text = text[:MAX_ASSISTANT_CHARS] + " …[trimmed]"
        msgs.append((role, text))
    return msgs, read


def load_state():
    try:
        with open(STATE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_state(state):
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=1)
    os.replace(tmp, STATE)


def note(source, hook):
    path, sid = hook.get("transcript_path"), hook.get("session_id")
    if not path or not sid:
        return
    state = load_state()
    s = state.setdefault(sid, {"done": 0})
    s.update(path=path, source=source, cwd=hook.get("cwd", ""))
    save_state(state)


def write_chunk(root, sid, s, msgs, read, now):
    start = s["done"]
    new = msgs[start:]
    first_user = next((t for r, t in new if r == "user"), "")
    title = re.sub(r"\s+", " ", first_user)[:80] or "(continued)"
    head = [
        "---",
        f"captured: {now:%Y-%m-%dT%H:%M}",
        f"source: {s['source']}",
        "kind: transcript",
        f"session: {sid[:8]}",
        f"cwd: {s.get('cwd', '')}",
        f"msg_start: {start}",
        f"msg_end: {len(msgs)}",
        f"brain_files_read: [{', '.join(sorted(read))}]",
        "explicit: false",
        "---",
        f"# {title}",
        "",
    ]
    body = [f"**{'John' if r == 'user' else 'Agent'}:** {t}\n" for r, t in new]
    out = os.path.join(root, "inbox", f"{now:%Y-%m-%d-%H%M}-{s['source']}-{sid[:8]}-m{start}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(head) + "\n".join(body))
    return out


def flush(root, now=None):
    now = now or datetime.now()
    state, written = load_state(), []
    for sid, s in list(state.items()):
        path = s.get("path", "")
        if not os.path.exists(path):
            del state[sid]
            continue
        if time.time() - os.path.getmtime(path) > FORGET_AFTER:
            del state[sid]
            continue
        with open(path, encoding="utf-8") as f:
            msgs, read = parse_transcript(f)
        if sum(r == "user" for r, _ in msgs) < MIN_USER_TURNS:
            continue
        if not any(r == "user" for r, _ in msgs[s["done"]:]):
            continue
        written.append(write_chunk(root, sid, s, msgs, read, now))
        s["done"] = len(msgs)
    save_state(state)
    return written


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["note", "flush"])
    ap.add_argument("--source", default="claude-code")
    ap.add_argument("--root")
    a = ap.parse_args()
    if a.cmd == "note":
        try:
            note(a.source, json.load(sys.stdin))
        except ValueError:
            pass
    else:
        for p in flush(a.root):
            print(p)
