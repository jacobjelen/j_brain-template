# INDEX: where to find and where to save

Agents: find notes with the search script. Don't read whole files to look for things:
```bash
python3 ~/j_brain/system/scripts/recall.py <names or keywords>   # summary + TL;DR + matched lines
python3 ~/j_brain/system/scripts/recall.py --list [folder]        # every note, one line each
```
Open a full note only when the search output isn't enough. The tables below say where things live. The digest maintains them and adds rows when it extends the structure.

## Lookup: question → where to look
| If you need… | Look in |
|---|---|
| Who John is, basics, values, how he likes to work | `memory/long/me.md` |
| What he's focused on right now, open loops, "needs John" | `memory/short/now.md` |
| Corrections and do/don't for agents | `system/rules/lessons.md` |
| A person: who they are, relationship, history, preferences | `memory/long/people/<slug>.md` (grep `aliases:` for nicknames) |
| Wife, family, partner's preferences | `memory/long/people/` (see `me.md` → Family for slugs) |
| A project's state, next steps, people, decisions | `memory/short/projects/<slug>.md` |
| A client or company: contacts, engagements, terms | `memory/short/clients/<slug>.md` → contacts in `people/` |
| Meeting prep with X about Y | person note + project note + client note + newest `raw/` sources they cite |
| Films, series | `memory/long/taste/films.md` |
| Music | `memory/long/taste/music.md` |
| Books, podcasts | `memory/long/taste/books.md` |
| Food, restaurants, cooking | `memory/long/taste/food.md` + `memory/long/health/diet.md` |
| Travel, places liked or visited | `memory/long/taste/travel.md` + `memory/long/lifestyle/places.md` |
| Weekend or date planning | `taste/*` + wife's person note + `lifestyle/places.md` + `short/plans/` |
| Health, conditions, medication, doctors | `memory/long/health/health.md` |
| Diet, allergies, what he eats | `memory/long/health/diet.md` |
| Exercise, sport | `memory/long/health/fitness.md` |
| Home, routines, schedule, where he lives | `memory/long/lifestyle/` |
| What he knows or can do (tech, tools, domains) | `memory/long/skills/` |
| Things he has learned, frameworks, lessons from past projects | `memory/long/knowledge/` |
| Trips, events, purchases being planned | `memory/short/plans/` |
| Ideas and open questions in progress | `memory/short/threads/` |
| What happened when, and why a note changed | `log/YYYY-MM.md` → `raw/` |
| Old, finished, inactive stuff | `archive/`, **only if John explicitly asks** |

## Save: kind of info → where it goes (used by the digest)
| New information about… | Goes to |
|---|---|
| John himself (identity, values, work style, background) | `memory/long/me.md` |
| Current priorities, this week, things waiting on John | `memory/short/now.md` |
| A person | `memory/long/people/<firstname-lastname>.md` (template: person) |
| A project | `memory/short/projects/<slug>.md` (template: project) |
| A client or company | `memory/short/clients/<slug>.md` (template: client) |
| A film, series, music, book, food or travel preference | the matching `memory/long/taste/*.md` |
| Health, diet, fitness | `memory/long/health/*.md` |
| Home, routines, places | `memory/long/lifestyle/*.md` |
| A skill or tool John uses or learned | `memory/long/skills/<slug>.md` (template: topic) |
| A durable insight or lesson | `memory/long/knowledge/<slug>.md` (template: topic) |
| A plan with a date (trip, event) | `memory/short/plans/<slug>.md` |
| An idea or open question being worked on | `memory/short/threads/<slug>.md` |
| A correction to how agents behave | `system/rules/lessons.md` |
| Doesn't fit anywhere | create a new note or folder from the closest template, add a row to both tables, and log it as STRUCTURE |

