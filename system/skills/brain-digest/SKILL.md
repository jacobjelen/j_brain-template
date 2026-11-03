---
name: brain-digest
description: Run the daily digest of John's second brain (j_brain). It processes inbox/ into memory/, moves sources to raw/, archives stale short-term notes, updates INDEX and log, then commits and pushes. Use when the scheduled routine fires, or when John says "digest my brain" / "process the inbox".
---

# brain-digest

Run from the repo root. You are the **only** writer of `memory/`. Work carefully: this is John's long-term memory. Git history is the undo.

## 0. Gate (before reading anything else)
```bash
git pull --rebase
python3 system/scripts/precheck.py
```
If it prints `NOTHING TO DO`, stop here: no log entry, no commit. Otherwise it lists what's waiting (inbox items, stale notes, lint problems). Do only the steps those need.

Then read: `INDEX.md`, `system/rules/note-format.md`, `system/rules/digest.md`, `system/rules/privacy.md`, `system/rules/lessons.md`, and `system/rules/archive.md` (only if notes are stale). Use the notes in `system/templates/` when creating new ones. To find existing notes, use `python3 system/scripts/recall.py <names>` rather than opening files one by one.

`TODAY` = today's date (YYYY-MM-DD). Keep a running list of everything you do; you'll need it for the log.

## 1. Sync
Already pulled in step 0. If the inbox is empty, jump to step 5.

## 2. Record usage
```bash
python3 system/scripts/archive_stale.py bump
```
This sets `last_used` on notes listed in inbox items' `brain_files_read`.

## 3. Process each inbox item, oldest first
For each file (plus its `.meta.md` sidecar, if any):
1. **Archive the source first.** Run `git mv inbox/<f> raw/<YYYY>/<MM>/<f>`, taking YYYY/MM from `captured`, or from the file name if `captured` is missing. Create the folder if needed. From now on, `raw/<YYYY>/<MM>/<f>` is the source path you cite.
2. **Redact** secrets in the raw copy (`privacy.md`). This is the only edit ever allowed in `raw/`.
3. **Extract durable facts.** Look for people, relationships, projects (state, next steps, decisions), clients, preferences and taste, health, lifestyle, plans with dates, skills used, lessons learned, and corrections.
   - Transcripts are mostly noise. Skip coding mechanics unless they reveal a project's state, a decision, a skill or a preference.
   - `explicit: true` beats inferred.
   - Most transcripts yield 0–5 facts. Yielding none is fine.
4. **Route** each fact using the INDEX **Save** table. Find existing notes by slug, by `aliases:`, and with grep.
5. **Rewrite** the target notes following `note-format.md`:
   - Update TL;DR and Current so they are true today.
   - Move superseded facts to History with a date.
   - Date each fact, and link it to the raw source with a relative link.
   - Add the raw path to `sources:` and set `updated: TODAY`.
   - Add `links:` between related notes, both ways (person ↔ project ↔ client).
6. **New entity** (a person, project, client or topic) → create it from a template.
7. **No home for the fact** → extend the structure: a new note or folder in the most sensible place. Add rows to **both** INDEX tables, and log it as `STRUCTURE`.
8. **Special kinds:**
   - `gap`: if the info exists somewhere, improve the INDEX Lookup row or the note's aliases or summary so it's found next time. If it doesn't exist, add it to that note's Open questions and to `now.md` → Needs John.
   - `correction`: fix the note. If it's about agent behaviour, add a dated one-line rule to `system/rules/lessons.md` with a source link.
9. Keep `memory/short/now.md` current: focus, open loops, upcoming dates (next ~30 days) from `plans/` and projects, and Needs John.

## 4. Conflicts
When a new fact contradicts a note:
- Newer and explicit wins. Put the old fact in History.
- If it's genuinely unclear which is right, keep both in Current marked `⚠ conflicting`, and add a question to `now.md` → Needs John.

## 5. Archive pass
```bash
python3 system/scripts/archive_stale.py list
```
For each stale note in `memory/short/`:
1. Promote durable knowledge to `memory/long/` (`archive.md`).
2. `git mv memory/short/<p> archive/<p>`.
3. Repoint links to it.
4. Log `ARCHIVE`.

If an inbox item reactivated an archived topic, move it back and log `RESTORE`.

## 6. Self-maintenance
```bash
python3 system/scripts/lint.py
```
- Keep each note's `summary:` one sharp line, and give people and projects `aliases:` for every name they go by. `recall.py` ranks on these, so they are how notes get found.
- Fix every reported problem (broken links, missing frontmatter, notes with no sources and undated facts) until lint exits 0.
- While touching notes, also look for:
  - duplicates: merge them, keeping a redirect line in the retired note's place in History
  - notes over 300 lines: split them
  - Open questions answered by now
  - empty notes that are routed often (from `gap`s)

  Fix what you can.
- If you think a **rule or system file** should change (anything in `system/` except `lessons.md`, or `AGENTS.md`), don't edit it. Write a `PROPOSAL` in the log and a line in `now.md` → Needs John.

## 7. Log
Append to `log/<YYYY-MM>.md`. Create it with a `# Log YYYY-MM` heading if missing.
```markdown
## TODAY
- Processed: 4 items (2 transcripts, 1 remember, 1 meeting)
- UPDATED [[memory/short/projects/acme-app]]: status → beta; next steps (src: raw/2026/10/…)
- CREATED [[memory/long/people/maya-novak]]
- STRUCTURE: added memory/long/taste/games.md + INDEX rows (no home for video-game preferences)
- ARCHIVE: memory/short/threads/old-idea.md (idle since 2026-03-01; lesson promoted to knowledge/…)
- LESSON: "Don't suggest horror films" → lessons.md
- PROPOSAL: …
- Issues: …
```
Keep it short: one line per action.

## 8. Commit and push
```bash
git add -A
git commit -m "digest: TODAY — N items, M notes, K structure changes"
git push
```
If the push is rejected, run `git pull --rebase` and push again. If a conflict hits `inbox/`, keep both sides. Never force-push.

## 9. Report
Reply with the log entry, and with any Needs John items.
