---
name: brain-recall
description: Answer questions using John's second brain (j_brain). Use whenever a request touches John's life, work, people, projects, clients, preferences, taste, health or plans. Examples are meeting prep, "recommend a film", "plan a weekend with my wife", "what's the status of X", "who is Y". Use it silently. It is also the default way to get context before helping with any personal task.
---

# brain-recall

Brain root: `/Users/john/Library/CloudStorage/GoogleDrive-john@example.com/My Drive/j_brain`. In a cloud clone, use the repo root.

## Steps
1. **Search first.** Put every name and topic in one call; it's accent-insensitive, best match first:
   ```bash
   python3 ~/j_brain/system/scripts/recall.py maya acme-app
   ```
   It returns path, summary, TL;DR and matched lines per note, plus undigested `inbox/` items, which override the notes. `--list [folder]` lists every note in one line each. Use `INDEX.md` only when you don't know where a kind of fact lives.
2. **Open full notes only if needed.** Read Current when the search output isn't enough (e.g. a whole films log). Go to History or `raw/` only to check something or to find a quote.
3. **Obey `system/rules/lessons.md`.** It's short; read it once per conversation.
4. **Check freshness.** Look at the `(as of …)` dates and `updated:`. If a fast-changing fact is more than about 2 months old, say it may be out of date.
5. **Answer.** Use the facts naturally. Cite a note only when the source matters or John asks ("per your notes from 12 Oct").
6. **Learn.**
   - The brain lacked something you needed → write a `kind: gap` inbox item (see `brain-remember`).
   - John corrects you → write a `kind: correction` inbox item.
   - John tells you a new durable fact → write a `kind: remember` inbox item.

## Recipes
- **Meeting prep with X about project Y:**
  - Run `recall.py X Y`. That usually covers the person, project and client notes in one call.
  - Open the project note in full for its next steps and decisions.
  - Open the newest `raw/` source only if you need what was actually said.
  
  Output: who they are, where things stand, proposed agenda, open questions, risks, and what X likely cares about.
- **Recommend a film or series:**
  - Read `taste/films.md`: never recommend anything in the Log, respect Dislikes, lean on Likes and ratings ≥8.
  - If it's for watching together, also read the partner's person note.
  - Give 3–5 picks, each with a one-line "why you'd like it" tied to his taste.
- **Plan a weekend with the wife:**
  - Run `recall.py wife food travel weekend`.
  - Then open what's still missing: her person note, `taste/food.md`, `lifestyle/places.md`, `health/diet.md` (restrictions) and `now.md` (busy dates).
  - Propose things they *both* like, and say which notes each choice comes from.
