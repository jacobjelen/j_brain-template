# j_brain: operating manual for AI agents

This repo is John's second brain. It holds the context an AI agent needs about him: who he is, the people in his life, projects, clients, skills, knowledge, taste, lifestyle and health. It is written **for agents first**. John may browse it in Obsidian, but you are the main reader.

Absolute path on John's Mac:
`/Users/john/Library/CloudStorage/GoogleDrive-john@example.com/My Drive/j_brain`
In a cloud clone, the path is the repo root.

## How to use it
The brain is read **on demand**, not at session start. Agents only know it exists (from a short pointer in their global instructions). Use it when a task would benefit from context about John, his people, work, taste or plans, or when he mentions something you don't know. Don't use it for generic tasks (plain coding questions, general facts).

1. **Search, don't browse.** Run `python3 ~/j_brain/system/scripts/recall.py <names or keywords>`.
   - It returns each matching note's summary, TL;DR and matched lines, accent-insensitive, best match first.
   - It also covers undigested `inbox/` items, which are newer than the notes and beat them.
   - `--list [folder]` shows every note in one line each.
   - Open a full note only when the search output isn't enough. Use `INDEX.md` when you need to know where a kind of fact lives.
2. **Obey `system/rules/lessons.md`**: the corrections John has given. Open `memory/long/me.md` or `memory/short/now.md` only when the task needs who he is or what he's doing right now.
3. **Use it silently.** Don't announce "checking my brain"; just be informed. Mention a source only when it matters ("your notes from 12 Oct say…").
4. **Capture.** Follow `system/skills/brain-remember/SKILL.md`.
   - When John says "remember…", or shares a durable fact (a preference, a person, a decision, a project change, a film he watched), write an inbox item.
   - Full conversation transcripts are captured automatically by hooks in Claude Code and Codex. Elsewhere (Cursor), capture only when asked, or when the conversation produced clearly durable facts.
5. **Report gaps.** When you needed something and the brain didn't have it (or had it wrong), write an inbox item with `kind: gap` or `kind: correction`. This is how the brain learns where it is weak.

## Hard rules
- **Never edit `memory/`, `INDEX.md` or `log/` in a normal session.** Only the daily digest (`system/skills/brain-digest`) writes there. You write only to `inbox/`. If John explicitly asks you to fix a note right now, do it, and also leave an inbox item so the log records it.
- **Never edit `system/` unless John asks.**
- **Never read `archive/`** unless John explicitly tells you to. It holds stale short-term memory.
- **`raw/` is immutable.** Read it to verify a fact. Never modify it.
- **Privacy:** follow `system/rules/privacy.md`. Never store passwords, keys, card or bank numbers, or ID numbers. Never send brain content to third-party services unless John asks.
- **Facts are dated or sourced.** If a note says "as of 2025-03" and the topic changes fast, treat it as possibly stale and say so.

## Layout (details in INDEX.md)
| Path | What |
|---|---|
| `inbox/` | Unprocessed captures. Agents write here. |
| `raw/YYYY/MM/` | Original sources after digestion. Notes link here. |
| `memory/long/` | Long-term: me, people, taste, health, lifestyle, skills, knowledge. Never auto-archived. |
| `memory/short/` | Short-term: now, projects, clients, plans, threads. Archived after 180 days without update or use. |
| `log/YYYY-MM.md` | What each digest did. |
| `archive/` | Stale short-term notes. Do not read. |
| `system/` | Rules, templates, skills, hooks, scripts. |

## Skills
| Skill | Use when |
|---|---|
| `system/skills/brain-recall` | Answering anything about John, his people, work or taste |
| `system/skills/brain-remember` | Saving something to the inbox |
| `system/skills/brain-digest` | The daily digest (cloud routine, or manually on request) |
| `system/skills/brain-onboard` | Interviewing John to fill gaps ("let's fill in my brain") |
