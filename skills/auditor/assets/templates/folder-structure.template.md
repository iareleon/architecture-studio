# Project Folder Structure

This file defines the required and dynamic structure of the architecture studio.

> **Important:** When updating this structure using the Windows `tree` command, always exclude the header lines (e.g., "Folder PATH listing", "Volume serial number...", "C:."). Ensure the block below is formatted as `bash`.

> **Note on Meetings and Actions:** All content in `raw/actions/` and `raw/decisions/` must have reference links to the source documents in `raw/meets/`.

```bash
├── .geminiignore        # Ignored files configuration
├── .obsidian/           # Obsidian vault settings
├── GEMINI.md            # AI Master Brain instructions
├── README.md            # Project Playbook
├── export/              # Output for documenter skill (Google Docs)
├── llm/                 # AI working memory core
│   ├── folder-structure.md # This file
│   └── install.md       # Installation decisions
├── project/             # Dynamic project files (HLDs, designs)
├── raw/                 # Immutable source documents and traceability logs
│   ├── actions/         # Action files (Must link to meets/)
│   ├── assets/          # Static assets (images, PDFs)
│   ├── change-log.md    # Master change index
│   ├── changes/         # Individual audit change files
│   ├── decisions/       # Decisions extracted from meets/ (Must link to meets/)
│   ├── discovery/       # Individual discovery logs
│   ├── discovery-log.md # Master discovery index
│   └── meets/           # Meeting notes and recordings
├── skills/              # Available AI Skills
│   ├── auditor/
│   ├── documenter/
│   │   ├── assets/
│   │   └── scripts/
└── wiki/                # Living documentation (Optional)
```