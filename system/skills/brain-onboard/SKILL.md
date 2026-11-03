---
name: brain-onboard
description: Interview John to fill his second brain (j_brain), or import context from existing sources. Use when John says "fill in my brain", "onboard", "interview me about X", or when brain notes are empty or have many Open questions.
---

# brain-onboard

Goal: get high-value facts from John quickly and save them as inbox items. The digest files them into notes.

## Interview mode
1. Pick a topic: John's choice, or the emptiest high-value area. Check which notes are stubs or have Open questions. Suggested order:
   1. me (work, family)
   2. now (current projects and focus)
   3. wife and family
   4. key people
   5. projects and clients
   6. films and series
   7. music
   8. food and diet
   9. travel and places
   10. health and fitness
   11. routines
   12. skills
2. Ask **one question at a time**. Keep questions concrete ("Name 5 films you loved and 2 you hated"), and offer examples so it's easy to answer. Ask a follow-up only where it adds real value.
3. Every few answers, write a `kind: remember`, `explicit: true` inbox item for that topic (format: `system/skills/brain-remember/SKILL.md`). Don't wait for the end.
4. Stop when John wants to. Summarise what was saved and suggest the next topic.

## Import mode
When John asks to import existing context, read the source, extract the durable facts about him, and write them as `kind: note` inbox items with the source path in the body. Never copy secrets.

Possible sources:
- `~/.claude/projects/*/memory/*.md`
- `~/.claude/CLAUDE.md`
- `~/.codex/AGENTS.md`
- READMEs and CLAUDE.md files of his recent projects
- exported notes, or a film list (Letterboxd/CSFD export)

## After
Tell John the items land in memory after the next digest. Offer to run `brain-digest` now.
