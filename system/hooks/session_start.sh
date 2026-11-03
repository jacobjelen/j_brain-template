#!/bin/bash
# SessionStart hook (Claude Code, Codex): sync the brain with GitHub. Prints nothing: agents learn the
# brain exists from system/pointer.md (in ~/.claude/CLAUDE.md, ~/.codex/AGENTS.md) and read it on demand.
[ -n "$BRAIN_NO_CAPTURE" ] && exit 0
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
nohup perl -e 'alarm shift; exec @ARGV' 60 bash "$ROOT/system/hooks/sync.sh" >/dev/null 2>&1 &
exit 0
