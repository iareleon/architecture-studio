# Change: Implement 'as' Alias System for CLI-Style Commands

- **Date-Time:** 2026-04-22-13-30
- **Status:** [done]
- **Phase Impacted:** Governance & CLI UX Evolution

## 1. Context
The user requested a natural CLI experience to execute skill-specific commands using the syntax `as <skill> <args>`. This improves the ergonomics of interacting with various expert agents within the workspace.

## 2. Changes Applied
- **Custom Command**: Created `.gemini/commands/as.toml` to serve as a universal dispatcher.
- **Dispatch Logic**: Implemented mapping for common aliases (`git`, `librarian`, `audit`, etc.) to their respective skill names.
- **Documentation**: Updated `README.md` with setup instructions for a PowerShell alias to enable the `as` syntax without the leading `/`.

## 3. Verification
- Verified the creation of `.gemini/commands/as.toml`.
- Ensured the prompt logic in the TOML file handles alias-to-skill mapping and argument passing.

## 4. Impact
- Enables a streamlined workflow for power users.
- Standardizes how skills are invoked through short, memorable aliases.
- Maintains modularity by using a single dispatcher for all skills.
