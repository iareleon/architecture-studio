# Personal — Soul route subflow

Use when the user **explicitly** wants material from a soul note promoted or linked into an operational vault.

## 1. Confirm intent

State what would move, and to which vault path. If the user has not asked for a move, do not use this subflow.

## 2. Resolve paths

Load `vault-paths` and the destination vault’s `CLAUDE.md` before any write.

## 3. Verbatim or excerpt

Default: one-way summary line in the target doc with a wikilink back to the **full** soul note. Never reframe the emotional content for “utility.”

## 4. No ticketification

Do not create ClickUp or task lists from soul content unless the user explicitly asks for tasks.
