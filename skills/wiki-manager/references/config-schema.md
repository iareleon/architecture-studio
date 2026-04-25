# Config Schema — wiki-manager.config.yaml

Full field reference for `{OBSIDIAN_META}/wiki-manager.config.yaml`.
Create or update using the `wiki-manager-config` workflow.

## Structure

```yaml
# wiki-manager.config.yaml
# Location: {OBSIDIAN_META}/wiki-manager.config.yaml
# Maintained by wiki-manager (run wiki-manager-config to update)

install:
  obsidian_root: ~/Obsidian           # Root containing all vault subdirectories
  obsidian_meta: ~/Obsidian/meta      # Meta/master vault — hub for inbox and super-wiki

inbox:
  raw: inbox/raw/                     # Relative to obsidian_meta — initial capture
  review: inbox/review/               # Relative to obsidian_meta — staged after classify
  approved: inbox/approved/           # Relative to obsidian_meta — ready to dispatch
  log: inbox/.classify.log            # Relative to obsidian_meta — optional classify log

routing:
  # Rules used by inbox-classify to determine intent and destination.
  # Applied in order; first match wins.
  # intent:        short tag, also used in filenames
  # signals:       content patterns (natural language description for LLM)
  # target_vault:  vault id from the vaults list below
  # target_subpath: path within that vault; {ts} = YYYYMMDD-HHMMSS timestamp
  - intent: soul
    signals: "Fear, anxiety, personal goals, inner reflection, my dream"
    target_vault: personal
    target_subpath: "inbox/raw/{ts}-soul.md"

  - intent: bible-study
    signals: "Bible passage, scripture, theology, exegesis"
    target_vault: bible-study
    target_subpath: "inbox/raw/{ts}-bible-study.md"

  - intent: idea
    signals: "Product idea, feature, what if we built, market, startup"
    target_vault: product
    target_subpath: "inbox/raw/{ts}-idea.md"

  - intent: engineering
    signals: "Architecture, engineering, spec, ADR, system design, code"
    target_vault: engineering
    target_subpath: "inbox/raw/{ts}-engineering.md"

  - intent: post
    signals: "LinkedIn post, content idea, social media, caption, thread"
    target_vault: social-media
    target_subpath: "inbox/raw/{ts}-post.md"

  - intent: business
    signals: "Client, strategy, business decision, revenue"
    target_vault: business
    target_subpath: "inbox/raw/{ts}-business.md"

  - intent: hobbies
    signals: "Photography, shoot, gear, technique, camera"
    target_vault: hobbies
    target_subpath: "inbox/raw/{ts}-hobbies.md"

  - intent: task
    signals: "Task, I need to, remember to"
    target_vault: personal
    target_subpath: "inbox/raw/{ts}-task.md"

  # ambiguous is the fallback — do not add a routing entry for it;
  # inbox-classify flags these files automatically when no rule matches with confidence >= 0.5

vaults:
  # All managed vaults.
  # inbox: true  = participates in inbox pipeline (inbox-dispatch + vault-inbox-sync)
  # inbox: false = wiki-sync discovers and indexes it, but inbox does not route to it
  - id: personal
    path: ~/Obsidian/personal
    inbox: true

  - id: bible-study
    path: ~/Obsidian/bible-study
    inbox: true

  - id: social-media
    path: ~/Obsidian/social-media
    inbox: true

  - id: engineering
    path: ~/Obsidian/engineering
    inbox: true

  - id: product
    path: ~/Obsidian/product
    inbox: true

  - id: business
    path: ~/Obsidian/business
    inbox: true

  - id: hobbies
    path: ~/Obsidian/hobbies
    inbox: true

  - id: arch-agency
    path: ~/Obsidian/arch-agency
    inbox: false

  - id: the-thought-scaffold
    path: ~/Obsidian/the-thought-scaffold
    inbox: false
```

## Field notes

- `target_subpath`: defined with an `inbox/raw/` prefix in the routing config so that `inbox-dispatch` places the file in the vault's staging area (`{vault}/inbox/raw/`) for user review. Before moving the file, `inbox-dispatch` rewrites this field in the frontmatter to strip the `inbox/` prefix (e.g. `inbox/raw/{ts}-soul.md` → `raw/{ts}-soul.md`). By the time `vault-inbox-sync` reads it, `target_subpath` already points to the final immutable `raw/` location within the vault.
- Vaults with `inbox: false` are still discovered and indexed by `wiki-sync`. They just do not receive dispatched inbox files.
- Add new vaults by appending to the `vaults` list and re-running any relevant operations.
