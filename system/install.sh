#!/bin/bash
# Wire j_brain into Claude Code, Codex (and print the Cursor rule). Idempotent: safe to re-run.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LINK="$HOME/j_brain"   # space-free path used by hooks and imports

[ -L "$LINK" ] || [ -e "$LINK" ] || ln -s "$ROOT" "$LINK"
echo "✓ $LINK → $ROOT"

backup() { [ -f "$1" ] && cp "$1" "$1.bak-$(date +%Y%m%d%H%M%S)" || true; }

# --- skills (Claude Code + Codex/agents) ---
for dir in "$HOME/.claude/skills" "$HOME/.agents/skills"; do
  mkdir -p "$dir"
  for s in "$ROOT"/system/skills/*/; do
    n=$(basename "$s"); [ -e "$dir/$n" ] || ln -s "$LINK/system/skills/$n" "$dir/$n"
  done
  echo "✓ skills linked in $dir"
done

put_pointer() {  # replace the marked j_brain block in $1 with system/pointer.md (or append it)
  backup "$1"
  python3 - "$1" "$ROOT/system/pointer.md" <<'PY'
import os, re, sys
path, pointer = sys.argv[1], open(sys.argv[2]).read().strip()
block = f"<!-- j_brain:start -->\n{pointer}\n<!-- j_brain:end -->"
text = open(path).read() if os.path.exists(path) else ""
# also drops the pre-marker versions ("# Second brain" + import/pointer line) from earlier installs
text = re.sub(r"\n*# Second brain\n(@~/j_brain/AGENTS\.md|John keeps a second brain[^\n]*)\n?", "\n", text)
if "<!-- j_brain:start -->" in text:
    text = re.sub(r"<!-- j_brain:start -->.*?<!-- j_brain:end -->", lambda _: block, text, flags=re.S)
else:
    text = text.rstrip("\n") + "\n\n" + block + "\n"
open(path, "w").write(text.lstrip("\n"))
PY
  echo "✓ brain pointer in $1"
}

# --- Claude Code: global CLAUDE.md pointer + hooks ---
put_pointer "$HOME/.claude/CLAUDE.md"

add_hooks() {  # <settings/hooks json file> <source>
  backup "$1"
  python3 - "$1" "$2" <<'PY'
import json, os, sys
path, source = sys.argv[1], sys.argv[2]
cfg = json.load(open(path)) if os.path.exists(path) else {}
hooks = cfg.setdefault("hooks", {})
want = {
    "SessionStart": {"type": "command", "command": "bash ~/j_brain/system/hooks/session_start.sh", "timeout": 30},
    "Stop": {"type": "command", "command": f"bash ~/j_brain/system/hooks/session_end.sh {source}", "timeout": 10},
}
for event, hook in want.items():
    groups = hooks.setdefault(event, [])
    if not any("j_brain/system/hooks" in h.get("command", "") for g in groups for h in g.get("hooks", [])):
        groups.append({"hooks": [hook]})
json.dump(cfg, open(path, "w"), indent=2)
PY
  echo "✓ hooks in $1"
}
add_hooks "$HOME/.claude/settings.json" claude-code

# --- Claude Code mods (system/mods is a local marketplace, read in place: edit + /reload-plugins) ---
if command -v claude >/dev/null; then
  claude plugin marketplace add "$LINK/system/mods" >/dev/null 2>&1 || true
  for m in "$ROOT"/system/mods/*/.claude-plugin/plugin.json; do
    n=$(basename "$(dirname "$(dirname "$m")")")
    claude plugin install "$n@j-brain-mods" --scope user >/dev/null 2>&1 || true
    echo "✓ mod $n installed"
  done
fi

# --- Codex: AGENTS.md pointer + hooks ---
if [ -d "$HOME/.codex" ]; then
  put_pointer "$HOME/.codex/AGENTS.md"
  add_hooks "$HOME/.codex/hooks.json" codex
  echo "  → In Codex, run /hooks once to trust the two new j_brain hooks."
fi

printf '\nCursor: paste this into Settings → Rules → User Rules (use source: cursor for inbox items):\n---\n'
cat "$ROOT/system/pointer.md"
echo "---"
