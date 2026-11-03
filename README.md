# j_brain

A second brain for AI agents: plain markdown that Claude Code, Codex and Cursor read before helping you, and that updates itself every day from your conversations.

> **This repo ships with example data.** Everything in `memory/`, `raw/`, `inbox/`, `log/` and `system/rules/lessons.md` describes **John Doe, a fictional person**, so you can see what a filled brain looks like. Delete it and replace "John" with your own name (see *Make it yours*).

```
conversation ──hook──▶ inbox/ ──daily digest (cloud)──▶ memory/ + INDEX.md + log/
                                          └──▶ raw/   (originals, linked as sources)
memory/short/ idle 180 days ──digest──▶ archive/
```

- **Agents read** `AGENTS.md` (the manual) → `INDEX.md` (the router) → notes. Search with `python3 system/scripts/recall.py <keywords>`.
- **Agents write** only to `inbox/`. The digest is the only writer of `memory/`.
- **Every day** a Claude Code routine runs `system/skills/brain-digest` (prompt in `system/routines/digest.md`). It digests the inbox, rewrites notes, moves sources to `raw/`, archives stale short-term notes, writes `log/YYYY-MM.md`, commits and pushes.

## Adding things by hand
Drop any file into `inbox/`. Markdown with frontmatter is best (see `system/templates/inbox-item.md`), but plain text, PDFs or meeting transcripts work too. For a non-markdown file, add a `<name>.meta.md` sidecar saying what it is.

Or just tell any agent "remember that…".

## Setup
```bash
git clone git@github.com:your-username/j_brain.git ~/path/to/j_brain
bash ~/path/to/j_brain/system/install.sh
```
`install.sh` links `~/j_brain` to the repo, symlinks the skills into `~/.claude/skills` and `~/.agents/skills`, adds a short pointer to `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`, and installs the capture/sync hooks.

If you keep the folder in Google Drive or iCloud, put the git database outside it (`git clone --separate-git-dir ~/.j_brain.git …`): cloud sync corrupts `.git` folders.

## Make it yours
1. Delete the example data: `memory/**/*.md`, `raw/2026/`, `inbox/*.md`, `log/*.md`, and the rules in `system/rules/lessons.md`.
2. Replace "John" with your name across `AGENTS.md`, `INDEX.md`, `CLAUDE.md`, `system/` (one find-and-replace).
3. Replace the example paths (`/Users/john/...`) in `AGENTS.md` and `system/skills/*/SKILL.md` with your own.
4. Run `install.sh`, then ask an agent to "fill in my brain" (skill `brain-onboard`).
5. Create a daily Claude Code routine with the prompt in `system/routines/digest.md`.

## Tests
```bash
python3 system/scripts/test_scripts.py   # scripts
python3 system/scripts/lint.py           # brain integrity
```
