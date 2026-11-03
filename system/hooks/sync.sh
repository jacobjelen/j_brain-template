#!/bin/bash
# Flush transcript chunks into inbox/, commit inbox/ (+ Obsidian settings), pull, push. Fails open: never blocks a session.
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT" || exit 0
t() { perl -e 'alarm shift; exec @ARGV' "$@"; }   # timeout without coreutils
touch "$HOME/.j_brain-last-sync"
python3 system/scripts/transcript_to_inbox.py flush --root "$ROOT" >/dev/null 2>&1
git add inbox .obsidian >/dev/null 2>&1
git diff --cached --quiet -- inbox .obsidian || git commit -q -m "inbox: $(date "+%F %H:%M") $(hostname -s)" -- inbox .obsidian >/dev/null 2>&1
t 15 git pull -q --rebase --autostash >/dev/null 2>&1 || git rebase --abort >/dev/null 2>&1
t 15 git push -q >/dev/null 2>&1
exit 0
