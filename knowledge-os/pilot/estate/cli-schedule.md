# CLI schedule — estate pilot

Minimum viable manual terminal cadence for a **single branch** (one desktop with Claude CLI during work hours).

| Task | Cadence | Source template |
|------|---------|-----------------|
| **KO · Inbox process** | Weekdays, once (morning) | Use the Knowledge OS terminal inbox workflow prompt |
| **KO · Super wiki refresh** | Daily, end of day (or merge with inbox) | Use the Knowledge OS terminal super-wiki refresh prompt |

**Working folders:** run from `OBSIDIAN_META` for inbox and `OBSIDIAN_ROOT` for super-wiki exactly as in the linked templates (after substituting your paths).

**Pilot acceptance:** for one week, no hand-edits to `meta/_os/index.md` or auto-generated `meta/wiki/{vault}.md`; if something is wrong, fix source vault `_os/log.md` or re-run the op-skill, not the index.

**Merge:** If the team prefers a single run, use one terminal session that executes both instruction blocks in order: inbox (with explicit approval) first, then super-wiki only if no moves are pending, or after approval.

## Future (not in pilot)

- launchd + `classify.sh` for FSEvents (optional; macOS)
- `social-media` skill for social posts; `documenter` skill for SOP PDFs
- Multi-seat: second writer uses **git pull** on the vault or Obsidian Sync; resolve conflicts in `inbox` first
