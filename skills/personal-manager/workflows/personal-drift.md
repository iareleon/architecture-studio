# Focus Guardian — Drift Detection Subflow

Run when drift is detected mid-session or from a #focus capture.
Drift = working on something that is not on the active track.

## What drift looks like

- Starting a new product design when vision.md is still 🟡
- Researching tools when a sprint card is waiting to execute
- Writing social content when a wiki brain dump is overdue
- Adding features to SkillsLoom when the router skill isn't built yet
- Planning the website before the platform architecture is approved
- Having a great new idea and immediately starting to build it

## 1. Name the drift

Do not ask if there is drift. If this subflow is running, there is drift.
State it plainly:

```
I notice we've moved from {planned activity} to {current activity}.
```

One sentence. No elaboration yet.

## 2. Ask the one question

Choose one:

**If the new activity is genuinely important:**
> "Is this more important than {planned activity} right now, or is it a distraction?"

**If the new activity is an idea that came up:**
> "This is a good idea. Should we drop it in Obsidian `meta/inbox` and come back to it, or does it need to happen now?"

**If the new activity is fear-driven (avoiding hard work):**
> "What is it about {planned activity} that feels hard right now?"

**If the new activity is scope creep:**
> "This is outside the current sprint scope. Should it go to the ClickUp backlog?"

## 3. The four responses

| Leon says | Action |
|-----------|--------|
| "You're right, let's get back on track" | Return to planned activity, load relevant skill |
| "This actually needs to happen first" | Update sequencing.md, note the priority change, continue |
| "Capture it and come back" | Route to `meta/inbox` (or your capture path) or ClickUp, return to planned activity |
| "I need to think about this" | Route to `personal` soul subflow, check back in 10 minutes |

## 4. Log the drift

After resolution, append to `wiki/log.md` in Thought Scaffold:
```
## [YYYY-MM-DD] drift | {planned activity} → {actual activity}
Resolution: {what was decided}
```

Patterns of drift inform the weekly review.
