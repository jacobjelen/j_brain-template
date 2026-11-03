# Archive rule

- Applies **only** to `memory/short/` (projects, clients, plans, threads). Never to `memory/long/`, `now.md`, `raw/` or `system/`.
- A note is stale when `max(updated, last_used)` is more than **180 days** before the digest date. `system/scripts/archive_stale.py` lists the candidates.
- **Promote before archiving.** Before moving a stale note, copy anything still useful long-term into `memory/long/`:
  - lessons and what worked → `knowledge/`
  - skills used → `skills/`
  - people's roles → `people/`
  
  Link the archived path as the source.
- Move with `git mv memory/short/X archive/X` (same relative path). Update any links pointing to it to the archive path, and log an `ARCHIVE` line.
- Agents never read `archive/` unless John explicitly asks. If an archived topic becomes active again, the digest moves it back to `memory/short/` and logs `RESTORE`.
