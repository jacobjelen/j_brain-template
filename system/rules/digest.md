# Digest procedure (summary)

The full step-by-step procedure is in `system/skills/brain-digest/SKILL.md`. This file states the invariants the digest must keep:

1. Every inbox item is moved to `raw/YYYY/MM/` (by its `captured` date) **before** facts are extracted, so source links are stable. `raw/` is never edited after that.
2. Every fact written to `memory/` links to at least one `raw/` source, or is dated.
3. Notes are rewritten (Current/History), not appended to. See `note-format.md`.
4. New folders or note types → add a row to both INDEX tables and log the change as `STRUCTURE`.
5. The digest may edit `memory/`, `INDEX.md`, `log/` and `system/rules/lessons.md`. It must **not** edit the other files in `system/` or `AGENTS.md`. Changes it wants there go into the log as `PROPOSAL` and into `now.md` under **Needs John**.
6. The digest ends with `lint.py` passing, a log entry, and one commit pushed to `main`.
7. Transcripts are mostly noise. Extract only durable facts about John, his people, projects, clients, preferences, decisions and lessons. Skip the mechanics of coding sessions unless they reveal a project's state, a decision or a skill.
