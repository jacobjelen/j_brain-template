@AGENTS.md

## Claude Code specifics
- The skills are installed as `brain-recall`, `brain-remember`, `brain-digest` and `brain-onboard` (symlinked from `system/skills/` by `system/install.sh`).
- Global awareness: `system/pointer.md` is copied into `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` by `system/install.sh`. Edit the pointer here, then re-run the installer.
- Hooks: `system/hooks/session_start.sh` syncs with GitHub in the background and prints nothing. `system/hooks/session_end.sh` saves the transcript to `inbox/`.
- When working *inside* this repo on the system itself (rules, scripts), you may edit `system/` and top-level docs. Still never hand-edit `memory/` without John asking.
