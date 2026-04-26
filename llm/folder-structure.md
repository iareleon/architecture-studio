# Project Folder Structure

```bash
project-skillsloom/
├── .github/
│   └── workflows/
│       └── validate.yml
├── .gitignore
├── FIRST-BRAIN.md
├── LICENSE
├── README.md
├── docs/                         # Published documentation (GitHub Pages)
│   ├── cli.md
│   ├── domain-layout.md
│   ├── getting-started.md
│   ├── how-it-works.md
│   ├── index.md
│   ├── knowledge-os.md
│   ├── skill-catalog.md
│   └── skill-spec.md
├── knowledge-os/                 # Knowledge OS integration pack
│   ├── knowledge-os.env.example
│   └── pilot/
│       └── estate/               # Estate agency pilot templates
│           ├── cli-schedule.md
│           ├── README.md
│           └── vault-skeleton.md
├── llm/                          # LLM-facing reference files
│   ├── folder-structure.md
│   └── install.json
├── raw/                          # Project working log (changes, decisions, discovery)
│   ├── change-log.md
│   ├── discovery-log.md
│   ├── changes/
│   ├── decisions/
│   │   └── decision-log.md
│   └── discovery/
├── scripts/                      # CLI and helper scripts
│   ├── skillmanager.sh
│   ├── install.sh
│   ├── agents.sh
│   ├── check-skill-names.sh
│   └── hooks/
│       └── pre-commit
└── skills/                       # All SkillsLoom skills (flat: skills/<name>/SKILL.md)
```

Each skill directory contains a `SKILL.md` and optional `workflows/`, `references/`, `persona/`, and `templates/` subdirectories. See [docs/domain-layout.md](../docs/domain-layout.md) and [skills/README.md](../skills/README.md).
