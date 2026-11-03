# Note format

Every note in `memory/` follows this format. Notes are written for agents first: they put the answer near the top, date every fact, and link every fact to its source.

## Frontmatter
```yaml
---
type: person        # profile|person|project|client|taste|health|lifestyle|skill|topic|plan|thread|now
summary: One line an agent can route on. recall.py shows it and ranks on it.
aliases: [Sam, wife]          # other names to grep for (people, projects)
updated: 2026-10-26            # last content change. Set by the digest.
last_used: 2026-10-25          # last time an agent read it. Set by the digest from transcripts.
sources: [raw/2026/10/2026-10-24-1830-claude-weekend.md]   # every raw file this note draws on
links: ["[[memory/short/projects/acme-app]]"]           # related notes
---
```

## Body
```markdown
## TL;DR
≤5 lines. The most useful current facts. An agent should be able to stop reading here.

## Current
- Fact. (as of 2026-10) [src](../../../raw/2026/10/file.md)
- Group with ### subheadings when the note grows.

## History
- 2026-10-24: Changed from X to Y. Previously: "…" [src](…)

## Open questions
- Things we don't know yet that would be useful. The digest and onboarding try to fill these.
```

## Rules
1. **Rewrite, don't append.** Update **Current** so it is true *today*. When a fact is superseded, move the old version to **History** with a date. Never leave contradictory facts side by side in Current.
2. **Every fact is timeless, dated or sourced.** Timeless: "born in Manchester". Dated: "(as of 2026-10)". Sourced: a link to `raw/`. Fast-changing facts (statuses, numbers, next steps) must be dated.
3. **Explicit beats inferred.** Something John said with "remember" (`explicit: true`) overrides something an agent inferred.
4. **Links.**
   - Between notes: path-qualified wikilinks, `[[memory/long/people/sam-doe]]`. They work in Obsidian and can be grepped.
   - To sources: relative markdown links to `raw/`, so they also work on GitHub.
5. **Slugs.** Lowercase and hyphenated. People: `firstname-lastname`. If only the first name is known, use `firstname` plus context (`maya-from-acme`) and rename later.
6. **Size.** Keep notes under ~300 lines. When a note grows past that, split it into a folder: `projects/foo/README.md` + `projects/foo/decisions.md`.
7. **No secrets.** See `privacy.md`.

## Special notes
- `memory/long/me.md`: always loaded. ≤100 lines. Identity, family slugs, work, values, how John likes agents to behave.
- `memory/short/now.md`: always loaded. ≤60 lines. Current focus, open loops, upcoming dates, and a **Needs John** section (digest proposals, questions).
- `memory/long/taste/*.md`: use tables, e.g. films: `| Title | Year | Seen | Rating /10 | Note |`, plus Likes / Dislikes / Want to see lists.
