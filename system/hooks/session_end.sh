#!/bin/bash
# Stop hook (Claude Code, Codex): remember this session's transcript; sync at most every 30 min.
# Usage: session_end.sh <claude-code|codex>   (hook JSON on stdin)
[ -n "$BRAIN_NO_CAPTURE" ] && exit 0
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
python3 "$ROOT/system/scripts/transcript_to_inbox.py" note --source "${1:-claude-code}" >/dev/null 2>&1
stamp="$HOME/.j_brain-last-sync"
if [ ! -e "$stamp" ] || [ -n "$(find "$stamp" -mmin +30)" ]; then
  nohup bash "$ROOT/system/hooks/sync.sh" >/dev/null 2>&1 &
fi
exit 0
