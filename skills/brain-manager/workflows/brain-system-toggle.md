# Memory System Skills Toggle Subflow

Switches the system skills mode in `model.md` between **always-on** and **manual**.

## Detect Current Mode

Read `${SKILLFORGE_DIR}/model.md`. Find the block between:
```
<!-- system-skills: <mode> -->
...
<!-- /system-skills -->
```

- If `<!-- system-skills: always-on -->` is found → current mode is **always-on**
- If `<!-- system-skills: manual -->` is found → current mode is **manual**
- If neither marker is found → tell user: "No system skills block found in model.md. Add one by re-running the installer or choosing a mode below."

## Propose the Switch

Show the current mode and the proposed change:

```
Current mode: always-on (system skills are active every session)
New mode:     manual    (invoke /skill-manager or /brain-manager when needed)

This will replace the System Capabilities block in model.md.
The change takes effect in the next session.

Switch to manual mode? (yes / no)
```

## Apply on Approval

1. Read the full contents of `${SKILLFORGE_DIR}/model.md`
2. Replace everything between `<!-- system-skills: * -->` and `<!-- /system-skills -->` (inclusive) with the contents of the appropriate template (under the `skill-manager` skill, shipped with the repo):
   - Switching to manual → `${SKILLFORGE_DIR}/skills/skill-manager/templates/persona/system-skills-manual.md`
   - Switching to always-on → `${SKILLFORGE_DIR}/skills/skill-manager/templates/persona/system-skills-always-on.md`
3. Write the updated file
4. Confirm: `"System skills set to <new-mode>. Restart your Claude session for the change to take effect."`

## Constraints

- Never modify any section of `model.md` outside the system-skills block
- Always show before/after of the block being replaced before writing
- Do not proceed without explicit approval
