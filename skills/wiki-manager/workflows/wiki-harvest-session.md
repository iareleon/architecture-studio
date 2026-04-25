# Wiki Harvest — Session

Runs a live brain dump session for a target wiki page.

If a persona is loaded (e.g. `persona/meridian.md` or `persona/knowledge-os.md`), follow its path guidance, ADR constraints, and authorisation rules. Generic defaults apply when no persona is loaded.

## 1. Identify target page

If not stated, ask:
```
Which wiki page are we harvesting today?
(e.g. vision, architecture, knowledge-model, compliance-model)
```

## 2. Read current state

Read the target wiki page in full.

If a persona is loaded: also read the files specified in the persona's path guidance (e.g. ADR index, key decisions, cross-vault links).

Identify:
- Current status (🟡 / 🟠 / 🟢)
- Open questions listed at the bottom of the page
- Sections marked "To be confirmed via brain dump"
- Conflicts with confirmed decisions or ADRs

## 3. Orient the user

State in one sentence what the page currently covers and what's missing. Do not summarise the whole page — name the gap:

```
[Page] is at 🟡 harvesting. The main gap is: [one sentence].
I'll ask you [N] focused questions. Answer however feels natural.
```

## 4. Ask focused questions

Work through open questions one at a time. Load `references/question-banks.md` for suggested questions per topic.

After each answer:
- Confirm understanding: restate in one sentence
- Ask: "Anything to add, or shall I move on?"
- Then ask the next question

Maximum 8 questions per session. Stop earlier if the key gaps are filled.

## 5. Capture and write

After all questions are answered:
1. Draft the updated page sections
2. Show the diff — what changed, what was added
3. Ask: "Does this capture it correctly? (yes / edit / skip)"
4. On yes: write the updated page, update `last_updated` frontmatter, advance status if appropriate
5. On edit: take the correction, re-show, repeat
6. On skip: leave unchanged, note the gap remains open

## 6. Status check

After writing:
- If all open questions answered and content is solid → propose 🟠 drafting
- If gaps remain → stay at 🟡 harvesting, update open questions list
- Never advance to 🟢 in this subflow — approval requires explicit user confirmation

## 7. Log

Append to the vault's `wiki/log.md` and `_os/log.md`:
```
## [YYYY-MM-DD] harvest | {page name}
Questions covered: N. Status: 🟡→🟠 or unchanged. Gaps remaining: [list].
```

Then run `folder-structure-sync.md` for the wiki subfolder modified.
