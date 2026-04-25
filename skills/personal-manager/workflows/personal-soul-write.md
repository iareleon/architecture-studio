# Soul Capture — Write Subflow

Writes a personal reflection to the Thought Scaffold soul layer.

## 1. Receive the reflection

Listen to what was shared. Do not ask clarifying questions yet.
Do not summarise it back immediately — let it land.

## 2. One optional follow-up

If the reflection is very short or the context is unclear, ask one question:
```
Is there more to this, or does that capture it?
```
If the user says "that's it" — proceed. Never push for more.

## 3. Generate the note

Derive a slug from the core theme: `kebab-case-theme.md`
The title should name what was felt, not what was concluded.

Good titles:
- `the-weight-of-building-alone.md`
- `fear-of-building-the-wrong-thing.md`
- `what-i-actually-want-from-this.md`
- `when-the-system-feels-hollow.md`

Bad titles:
- `reflection-001.md`
- `personal-goals.md`
- `notes.md`

## 4. Write the note

```yaml
---
title: {title}
type: soul
tags: [{relevant tags}]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: ingested
route-to: ""
---
```

Body:
- Open with the reflection as shared — exact voice, exact weight
- Add context if needed — what prompted this, what was happening
- Cross-reference related notes: `[[forgemaster-model]]`, `[[the-thought-scaffold]]`, etc.
- End with "See also:" links if relevant

Do not:
- Add a "lessons learned" section
- Suggest action steps
- Reframe the fear as an opportunity
- End with encouragement or resolution

## 5. Update index and log

Add to `wiki/index.md` under Soul section:
```
- [[soul/{slug}]] — {one honest sentence describing what this captures}
```

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] personal-soul | {title}
Captured from: {conversation / raw dump}. Cross-references: {list}.
```

## 6. Confirm

```
Soul note written: wiki/soul/{slug}.md
```

No further commentary. No reassurance. Just confirmation.
