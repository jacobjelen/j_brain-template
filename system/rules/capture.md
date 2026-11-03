# Capture: how agents write to the inbox

Agents in normal sessions write **only** to `inbox/`. The daily digest turns inbox items into memory.

## File name
`inbox/YYYY-MM-DD-HHMM-<source>-<slug>.md`, for example `inbox/2026-10-26-1412-claude-film-dune.md`.

## Format
```markdown
---
captured: 2026-10-26T14:12
source: claude-code        # claude-code | codex | cursor | manual | meeting | email
kind: remember             # transcript | remember | meeting | note | gap | correction
about: [memory/long/taste/films.md]   # optional hints: notes this relates to
cwd: ~/Projects/AcmeApp            # optional: where the conversation happened
explicit: true             # true when John directly said "remember"/stated it
---
John watched Dune Part Two on 2026-10-25 with his wife, loved it (9/10), especially the score.
```

## Kinds
| Kind | When | Body |
|---|---|---|
| `transcript` | Written automatically by the session-end hook | The conversation as markdown |
| `remember` | John asks to remember something, or states a durable fact | 1–10 lines in John's terms: who, what, when |
| `meeting` | A meeting transcript or notes | Raw transcript; put attendees and project in `about` |
| `note` | A document, article or idea John wants kept | Content or a summary plus a link |
| `gap` | You needed info the brain didn't have | "Needed X to answer Y; looked in Z." |
| `correction` | John corrected you, or the brain was wrong | What was wrong, what is right, the rule to follow |

## Rules
- One topic per `remember` item. Several facts are fine if they are about the same thing.
- Write facts as statements with dates. Don't write "he likes this", write "John said on 2026-10-26 that he likes…".
- Non-markdown files (PDF, audio, images): drop the file in `inbox/` with a `<filename>.meta.md` sidecar using the frontmatter above.
- Never put secrets in the inbox (`privacy.md`).
- After writing, don't commit. The hooks commit and push the inbox.
