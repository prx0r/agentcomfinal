# AgentCom Plugin Canonical (2026-09-13)

> Imported into `agentcomfinal` from R2 `agentcom` bucket. This file is the import README — original README preserved alongside (see below).

- **slug:** `agentcom-plugin-canonical`
- **source zip:** `docs/agentcom-plugin-canonical-2026-09-13.zip` (50003 bytes)
- **unpacked:** 28 files, 118971 bytes (after removing `__pycache__` / `.pytest_cache` / `*.pyc`: 0 entries cleaned)
- **top-level inside:** `agentcom_plugin_canonical`
- **original README(s):** `agentcom_plugin_canonical/README.md`

## What this is

Canonical plugin spec + router standard + lint/validation checks + agent prompts (BUILD / REVIEW / ROUTING_EVAL) + schemas/templates/evals. This is the submission gate.

## Layout (top 2 levels)

```
  agentcom_plugin_canonical/CANONICAL_GUIDE.md (9345b)
  agentcom_plugin_canonical/CHECKLIST.md (4344b)
  agentcom_plugin_canonical/README.md (3644b)
  agentcom_plugin_canonical/agentcom/ROUTER_STANDARD.md (2005b)
  agentcom_plugin_canonical/agentcom/router_contract.json (932b)
  agentcom_plugin_canonical/checks/plugin_lint.py (10304b)
  agentcom_plugin_canonical/checks/run_all.py (538b)
  agentcom_plugin_canonical/checks/source_scan.py (1780b)
  agentcom_plugin_canonical/checks/validate_schema.py (739b)
  agentcom_plugin_canonical/data/alpha.json (3530b)
  agentcom_plugin_canonical/data/failure_modes.json (8354b)
  agentcom_plugin_canonical/data/requirements.json (5811b)
  agentcom_plugin_canonical/data/rubric.json (2724b)
  agentcom_plugin_canonical/data/submission_limits.json (1415b)
  agentcom_plugin_canonical/evals/domain_negative_examples.jsonl (592b)
  agentcom_plugin_canonical/evals/domain_positive_examples.jsonl (683b)
  agentcom_plugin_canonical/evals/routing_case.schema.json (515b)
  agentcom_plugin_canonical/prompts/BUILD_AGENT.md (2641b)
  agentcom_plugin_canonical/prompts/ROUTING_EVAL_AGENT.md (1248b)
  agentcom_plugin_canonical/prompts/SUBMISSION_REVIEW_AGENT.md (2297b)
  agentcom_plugin_canonical/schemas/plugin_spec.schema.json (8066b)
  agentcom_plugin_canonical/schemas/provider_ledger.schema.json (2621b)
  agentcom_plugin_canonical/sources/community_alpha_digest.md (3352b)
  agentcom_plugin_canonical/sources/evidence_claims.jsonl (19261b)
  agentcom_plugin_canonical/sources/source_index.json (11736b)
  agentcom_plugin_canonical/templates/chatgpt-app-submission.example.json (1420b)
  agentcom_plugin_canonical/templates/plugin_spec.clean_example.json (4759b)
  agentcom_plugin_canonical/templates/plugin_spec.template.json (4315b)
```

## Original README excerpt

_Source: `agentcom_plugin_canonical/README.md`_

```markdown
# AgentCom Plugin Canonical Kit

Version: 2026-09-13

A machine-readable and agent-usable conformance kit for building, evaluating, and submitting OpenAI ChatGPT/Codex plugins backed by remote MCP servers.

This kit separates:

- **HARD**: current OpenAI submission/policy requirements that should block release when violated.
- **GUIDANCE**: current official recommendations that materially improve reliability/reviewability.
- **ALPHA**: high-signal OpenAI staff/community observations that are useful but can change quickly.
- **HEURISTIC**: AgentCom operating rules inferred from the evidence; useful for optimization, not platform policy.

The central principle is: **own a narrow external capability that ChatGPT cannot reliably do natively, expose it through a tiny intent-aligned tool surface, and make the implementation boring, fast, auditable, authorized, and easy to review.**

## Start here

1. Read `CANONICAL_GUIDE.md`.
2. Copy `templates/plugin_spec.template.json` into your project as `plugin_spec.json` and fill it from source truth.
3. Run:

```bash
python checks/plugin_lint.py plugin_spec.json
```

4. Fix every `ERROR`. Treat `WARN` as a release blocker unless explicitly waived with evidence.
5. Generate/maintain routing evals using `evals/` and `prompts/ROUTING_EVAL_AGENT.md`.
6. Before submission, run `prompts/SUBMISSION_REVIEW_AGENT.md` against the actual MCP source implementation, not only the manifest.
7. Use OpenAI's official `chatgpt-app-submission` skill when available to produce the final `chatgpt-app-submission.json`.

## Files

- `CANONICAL_GUIDE.md` — human-readable canonical operating guide.
- `CHECKLIST.md` — final submission-day human + agent gate.
- `data/submission_limits.json` — current numeric/package limits from official submission-error docs.
- `data/failure_modes.json` — official blockers + recurring community failure patterns with deterministic diagnostics.
- `schemas/provider_ledger.schema.json` — authorization/ToS/value-add ledger for every third-party provider.
- `sources/evidence_claims.jsonl` — flattened claim-level evidence corpus for agents/retrieval.
- `checks/validate_schema.py` — validates a plugin spec against the canonical JSON Schema.
- `data/requirements.json` — hard requirements and official guidance.

... (+19 more lines in agentcom_plugin_canonical/README.md)
```

## How to use

- Raw zip stays in `docs/agentcom-plugin-canonical-2026-09-13.zip` — this folder is the unpacked working copy.
- Run tests if present: `python -m pytest packages/agentcom-plugin-canonical -q` (adjust to inner dir, e.g. `packages/agentcom-plugin-canonical/agentcom_plugin_canonical`).
- See `/AUDIT.md` for how this package relates to the other 11 + 16 notes.
