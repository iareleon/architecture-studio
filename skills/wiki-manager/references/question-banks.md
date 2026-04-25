# Question Banks — Wiki Harvest Sessions

Focused questions per wiki page topic.
Load the relevant section only. Never ask all questions in one session.

## Vision

1. Who is the person that buys this? What is their title, their company size, their daily frustration?
2. What does their current "solution" look like — Word docs, Confluence chaos, spreadsheets?
3. When they first use this and it works, what is the first thing they notice is different?
4. What does success look like 6 months after deployment — what metric has moved?
5. What is the single biggest reason this wouldn't get bought?
6. Is the first target a single enterprise client or a multi-tenant product?
7. What pain have you personally witnessed that this solves?

## Architecture

1. Should the primary data layer be abstracted from day one, or use the simplest option until there's a reason to swap?
2. Single-tenant or multi-tenant — one instance per client install, or shared infra with isolated data?
3. What is the minimum viable deployment unit — single container, or Compose from day one?
4. Who maintains configuration files — the platform team, the client's team, or both?

## Knowledge model

1. What is the minimum schema needed to run the first meaningful operation?
2. How do you handle confidence — when the system extracts a pattern, how sure does it need to be before writing?
3. How do decisions version over time — does an existing record get updated, or does a new one get created?
4. Should external vault content be treated as seed knowledge or a separate corpus?

## Compliance model

1. Which domain do you want to define rubrics for first?
2. For that domain, name three principles you'd score any artefact against.
3. What does "partial" look like vs "addressed" for one of those principles?
4. Who is the human reviewer that resolves conflicting signals?

## Integrations

1. For file-based sources: should the agent watch for changes continuously, or ingest on manual trigger?
2. For structured sources: what specifically should be extracted — decisions only, or also context and history?
3. Should task/ticket data be ingested as artefacts, or only as references?

## UX

1. Is the primary interface a dashboard, a CLI, or a chat?
2. How does a user submit content for processing — file upload, URL, or paste?
3. What does the most useful single view look like — a score card, a radar, a list of gaps?
4. Who else besides the primary user interacts with this — reviewers, auditors, executives?
