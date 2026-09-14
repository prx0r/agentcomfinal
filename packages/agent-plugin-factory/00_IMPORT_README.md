# Agent Plugin Factory v0.1

> Imported into `agentcomfinal` from R2 `agentcom` bucket. This file is the import README — original README preserved alongside (see below).

- **slug:** `agent-plugin-factory`
- **source zip:** `docs/agent-plugin-factory-v0.1.zip` (19679 bytes)
- **unpacked:** 17 files, 22249 bytes (after removing `__pycache__` / `.pytest_cache` / `*.pyc`: 1 entries cleaned)
- **top-level inside:** `agent-plugin-factory`
- **original README(s):** `agent-plugin-factory/README.md`

## What this is

Minimal factory that turns a 'packet' (candidate + MCP snapshot) into a scored plugin spec. CLI + registry + evals. Example: domain-checker.

## Layout (top 2 levels)

```
  agent-plugin-factory/AGENTS.md (610b)
  agent-plugin-factory/README.md (2378b)
  agent-plugin-factory/VALIDATION.json (310b)
  agent-plugin-factory/docs/architecture.md (2739b)
  agent-plugin-factory/docs/business.md (1401b)
  agent-plugin-factory/docs/evals.md (1236b)
  agent-plugin-factory/factory/__init__.py (20b)
  agent-plugin-factory/factory/cli.py (922b)
  agent-plugin-factory/factory/evals.py (923b)
  agent-plugin-factory/factory/packet.py (694b)
  agent-plugin-factory/factory/registry.py (382b)
  agent-plugin-factory/factory/scoring.py (1157b)
  agent-plugin-factory/packets/domain-checker.json (5886b)
  agent-plugin-factory/pyproject.toml (147b)
  agent-plugin-factory/sources/projects.md (1451b)
```

## Original README excerpt

_Source: `agent-plugin-factory/README.md`_

```markdown
# Agent Plugin Factory

**MVP:** finished MCP -> host-verified ChatGPT plugin.

The project deliberately starts *after* the MCP capability works. It focuses on the part that is still hard: deciding which external capability fills a real ChatGPT gap, shaping the tool surface so ChatGPT can discover it, evaluating routing in the real host, preparing submission artifacts, and learning from production usage.

## Core loop

```text
MCP Registry / GitHub / owned MCPs
  -> Candidate Scout
  -> ChatGPT Gap + Externality Gate
  -> MCP Characterization
  -> Pluginization Delta
  -> Tool/Metadata Optimization
  -> Routing Corpus
  -> MCPJam / simulator evals
  -> REAL ChatGPT Developer Mode evals
  -> Submission Packet
  -> Publish
  -> Telemetry + Regression Corpus
```

A protocol-valid MCP is not automatically a good plugin. A good plugin needs protocol correctness, a useful external capability, routing/discovery fitness, safe host behavior, and a viable distribution/monetization path.

## Quickstart

```bash
python -m factory.cli score examples/domain-checker/candidate.json
python -m factory.cli packet examples/domain-checker/candidate.json examples/domain-checker/mcp_snapshot.json --out packets/domain-checker.json
python -m factory.cli registry --limit 100 --out packets/registry.json
```

The registry command uses the public official MCP Registry API when run with internet access.

## Product wedge

### Pluginize your MCP
Input: a working MCP endpoint/repo + purpose + rights declaration.


... (+13 more lines in agent-plugin-factory/README.md)
```

## How to use

- Raw zip stays in `docs/agent-plugin-factory-v0.1.zip` — this folder is the unpacked working copy.
- Run tests if present: `python -m pytest packages/agent-plugin-factory -q` (adjust to inner dir, e.g. `packages/agent-plugin-factory/agent-plugin-factory`).
- See `/AUDIT.md` for how this package relates to the other 11 + 16 notes.
