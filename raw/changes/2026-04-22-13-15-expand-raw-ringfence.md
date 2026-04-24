# Change: Expand /raw/ Ringfence for Cost Efficiency

- **Date-Time:** 2026-04-22-13-15
- **Status:** [done]
- **Phase Impacted:** Governance & Context Optimization

## 1. Context
The user requested to expand the explicit read rule in `GEMINI.md` to cover the entire `/raw` layer. This ensures that all files under `/raw/` (including logs, changes, discovery, and reports) are excluded from implicit reads by the LLM, optimizing context usage.

## 2. Changes Applied
- Modified `GEMINI.md` to update the **Cost Efficiency** directive.
- Changed the scope from `/raw/changes` and `/raw/discovery` to the entire `/raw/` directory.

## 3. Verification
- Verified that `GEMINI.md` reflects the change.
- Confirmed that the directive now explicitly mentions the entire `/raw/` directory.

## 4. Impact
- Reduced risk of "context flooding" from large log files and audit records in the `/raw` layer.
- Enforces a pattern of explicit retrieval for all traceability and source data.
