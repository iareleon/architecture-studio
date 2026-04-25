# Question Banks — Wiki Harvest Sessions

Focused questions per wiki page topic.
Load the relevant section only. Never ask all questions in one session.

## Vision

1. Who is the person that buys this? What is their title, their company size, their daily frustration?
2. What does their current "solution" look like — Word docs, Confluence chaos, spreadsheets?
3. When they first use Meridian and it works, what is the first thing they notice is different?
4. What does success look like 6 months after deployment — what metric has moved?
5. What is the single biggest reason this wouldn't get bought?
6. Is the first target a single enterprise client or a multi-tenant product?
7. What pain have you personally witnessed in your enterprise engagements that this solves?

## Architecture

1. Should the graph port be abstracted from day one, or use Kuzu directly until there's a reason to swap?
2. Single-tenant (one graph per client install) or multi-tenant (shared infra, isolated graphs)?
3. What is the minimum viable deployment — single Docker container, or Compose from day one?
4. Who maintains the rubric YAML files — the platform team, the client's architects, or both?

## Knowledge model

1. What is the minimum graph schema needed to run the first compliance score?
2. How do you handle confidence — when the knowledge writer extracts a pattern, how sure does it need to be before writing?
3. How do architectural decisions version over time — does an ADR get updated, or does a new node get created?
4. Should the Obsidian vault content be treated as seed knowledge or a separate corpus?

## Compliance model

1. Which domain do you want to define rubrics for first — EA, Cyber, Data, Integration, or Cloud?
2. For that domain, name three principles you'd score any HLD against.
3. What does "partial" look like vs "addressed" for one of those principles?
4. Who is the human reviewer that resolves conflicting signals?

## Integrations

1. For Obsidian: should the agent watch for file changes continuously, or ingest on manual trigger?
2. For Mermaid: should we parse the mermaid-js AST, or write a lightweight Python parser?
3. For GitHub: what specifically should be extracted — ADRs only, or also READMEs and commit messages?
4. Should ClickUp/Jira tickets be ingested as architectural artefacts, or only as task references?

## UX

1. Is the primary interface the dashboard or the CLI?
2. How does an architect submit an HLD for scoring — file upload, URL, or paste?
3. What does the most useful single view look like — a score card, a radar, a list of gaps?
4. Who else besides the lead architect uses this — junior architects, compliance auditors, CTOs?
