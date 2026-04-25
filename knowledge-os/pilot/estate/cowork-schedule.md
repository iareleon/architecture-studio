# Cowork schedule — estate pilot

Minimum viable automation for a **single branch** (one desktop with Claude open during work hours).

| Task | Cadence | Source template |
|------|---------|-----------------|
| **KO · Inbox process** | Weekdays, once (morning) | [knowledge-os/cowork/task-inbox-process.txt](../../cowork/task-inbox-process.txt) |
| **KO · Super wiki refresh** | Daily, end of day (or merge with inbox) | [knowledge-os/cowork/task-super-wiki-refresh.txt](../../cowork/task-super-wiki-refresh.txt) |

**Working folders:** set Cowork’s working directory to `OBSIDIAN_META` for inbox, and `OBSIDIAN_ROOT` for super-wiki—exactly as in the linked templates (after substituting your paths).

**Pilot acceptance:** for one week, no hand-edits to `meta/_os/index.md` or auto-generated `meta/wiki/{vault}.md`; if something is wrong, fix source vault `_os/log.md` or re-run the op-skill, not the index.

**Merge:** If the team prefers a single run, use one Cowork task that concatenates both instruction blocks in order: inbox (with explicit approval) first, then super-wiki—only if no moves are pending, or after approval.

## Future (not in pilot)

- launchd + `classify.sh` for FSEvents (optional; macOS)
- `social-media` skill for social posts; `documenter` skill for SOP PDFs
- Multi-seat: second writer uses **git pull** on the vault or Obsidian Sync; resolve conflicts in `inbox` first
