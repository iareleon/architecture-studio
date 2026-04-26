<!-- system-skills: always-on -->
## System Capabilities (Always Active)

> To switch to manual mode: invoke `/brain-manager` → "toggle system skills to manual"

### Skill Detection

Propose a new skill when any of these occur:
- Same ad-hoc pattern appears 2+ times in a session with no matching active skill
- User describes a multi-step process with no matching active skill
- User references a tool or technology not covered by any active skill
- User asks "is there a skill for X?"

Before proposing: run `skillmanager ls` to confirm no skill with that name already exists.

Proposal format:
```
Potential new skill: <name> (<type>) — <one-line description>.
Create now / Defer / Decline?
```
- **Create now** → reply: "Activate `skill-manager` to create this skill."
- **Defer** → write stub to `${SKILLSLOOM_DIR}/skills/skill-manager/references/deferred-skill-plans/<name>-YYYY-MM-DD.md`, confirm path
- **Decline** → suppress for this session only; do not persist

### Memory Management

Activate when user says: "remember that...", "note that...", "I prefer...", "from now on...", "forget...", "remove from memory..."

| Intent | Target |
|---|---|
| Project / product | Workspace `CLAUDE.md` (or path the user names) |
| Skill sub-topic | `skills/<skill-name>/persona/<topic>.md` when that skill uses `persona/` |
| Legacy | `skills/<skill-name>/memory/baseline.md` only if it still exists |

Write rules: always show before/after diff, wait for approval, archive (never delete), update `last-updated`.
<!-- /system-skills -->
