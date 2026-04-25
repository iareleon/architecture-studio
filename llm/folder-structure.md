# Project Folder Structure

```bash
project-skill-forge/
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
│   ├── cowork/                   # Claude Cowork scheduled task templates
│   │   ├── task-inbox-process.txt
│   │   ├── task-super-wiki-refresh.txt
│   │   └── task-wiki-harvest-refresh.txt
│   └── pilot/
│       └── estate/               # Estate agency pilot templates
│           ├── cowork-schedule.md
│           ├── memory-estate-baseline.md
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
└── skills/                       # All Skillforge skills (flat, one dir per skill)
    ├── architect/
    ├── cloud-engineer/
    ├── development-engineer/
    ├── devops/
    ├── diagrammer/
    ├── documenter/
    ├── git/
    ├── memory/
    ├── personal/
    ├── project-manager/
    ├── security/
    ├── skill-manager/
    ├── social-media/
    ├── tester/
    ├── vault-paths/
    └── wiki-harvest/
```

Each skill directory contains a `SKILL.md` and optional `workflows/`, `references/`, `persona/`, and `templates/` subdirectories. See [docs/domain-layout.md](../docs/domain-layout.md) and [skills/README.md](../skills/README.md).
