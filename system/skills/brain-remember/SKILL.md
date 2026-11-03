---
name: brain-remember
description: Save something to John's second brain (j_brain) inbox. Use when John says "remember", "note that", "save this", "add to my brain", or shares a durable fact (a preference, person, decision, project update, film watched, health info). Also use when the brain lacked info you needed (gap) or when John corrects you (correction). Writes only to inbox/; the daily digest does the rest.
---

# brain-remember

Brain root: `/Users/john/Library/CloudStorage/GoogleDrive-john@example.com/My Drive/j_brain`.

Write **one new file** to `inbox/`. Never edit `memory/` directly. The daily digest absorbs inbox items.

## Steps
1. Choose the `kind`:
   - `remember`: a fact or preference
   - `meeting`: meeting notes or a transcript
   - `note`: a document or idea to keep
   - `gap`: the brain lacked something
   - `correction`: John corrected you, or a note was wrong
2. File name: `inbox/<YYYY-MM-DD-HHMM>-<source>-<short-slug>.md`. Get the time with `date +%Y-%m-%d-%H%M`. `source` is `claude-code`, `codex` or `cursor`.
3. Content:
   ```markdown
   ---
   captured: 2026-10-26T14:12
   source: claude-code
   kind: remember
   about: [memory/long/taste/films.md]      # best guess of related notes; [] if unsure
   cwd: <current working directory>
   explicit: true                           # true if John stated/asked it directly
   ---
   John watched "Dune: Part Two" on 2026-10-25 with his wife. Rated 9/10; loved the score and visuals.
   ```
   Write facts as dated statements in plain words. Include who, what and when. Skip the conversation fluff.
4. Never include passwords, keys, card or bank numbers, or ID numbers (`system/rules/privacy.md`).
5. Confirm in one short line ("Saved, it'll be in your brain after tonight's digest"). Don't commit; the hooks commit and push the inbox.

## Examples
- "Remember that Maya from Acme prefers calls over email": `kind: remember`, about `[memory/long/people/]`.
- John: "No, my wife is vegetarian, not vegan": `kind: correction`. Body: what was wrong, what is right.
- You needed his dentist's name and it wasn't there: `kind: gap`. Body: "Needed John's dentist for X; looked in health/health.md; not present."
- John pastes meeting notes: `kind: meeting`, about the project and people. Body: the notes verbatim.
