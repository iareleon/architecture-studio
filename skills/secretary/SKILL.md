---
name: secretary
description: Format meeting notes, extract actions, and extract decisions. Use when asked to process raw meeting notes, scripts, transcripts, extract tasks/decisions, or manage files in raw/meets/.
---
# Meeting Secretary

## Core Responsibilities
- **Format Meeting Notes:** Clean up raw meeting notes and transcripts using the provided script.
- **Extract Actions:** Extract action items from meeting notes and append them to a central action list, ensuring they are linked to the source meeting note.
- **Decision Scrubbing:** Identify and log decisions made or pending discovery from meeting notes and scripts.

## Workflows

### 1. Format Meeting Notes
When requested to format raw meeting notes or transcripts:
- Ensure the raw meeting notes file is in the `raw/` directory.
- Execute `python scripts/format_meeting_notes.py <file_path> [--script]` to clean up the content. Use the `--script` flag if formatting a transcript.
- Once completed, move the formatted file from `raw/` to the `raw/meets/` directory.

### 2. Extract Actions
When asked to extract things the user must be aware of or do from notes:
- Read the specified meeting note.
- Extract the relevant action items.
- Append them to `raw/actions/my-actions.md`.
- **CRITICAL:** Ensure that every extracted action item includes a clear markdown link back to the source meeting note.

### 3. Decision Scrubbing
When requested to scrub for decisions (made or to be discovered):
- **Source:** ONLY read from `/raw/meets/`. This includes meeting notes and scripts.
- **Central Log:** Create or update `raw/decisions/decision-log.md`.
- **No Change Logs:** DO NOT create any entries in `llm/change-log.md` or files in `llm/changes/` for this specific workflow.
- **Goal:** Scrub for decisions made OR those that need to be discovered.
- **Templates:** 
  - If `raw/decisions/decision-log.md` does not exist, initialize it using `skills/secretary/assets/templates/decision.log`.
- **Linking:** Maintain link integrity using Obsidian-style `[[ ]]` links for the "Meeting Ref" column (e.g., `[[2026-04-17]]`).
- **Content:** The log must strictly contain the decision table. Do not include Discovery Items, Next Steps, or any other topics.
