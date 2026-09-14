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

Output: readiness score, app archetype, tool rewrite suggestions, positive/negative routing corpus, conformance/eval plan, ChatGPT host verification checklist, submission handoff, telemetry plan.

### Managed routing/eval
Continuously re-test tool selection and workflow completion as ChatGPT/model behavior changes. This is likely more defensible than one-time conversion.

### Plugin opportunity miner
Scan existing MCPs and rank only capabilities that require live state/action, authoritative data, permissions, transactions, or other things a smarter base model cannot simply internalize.

## Non-goals
- rebuilding MCP servers from scratch when a working one exists;
- blindly republishing third-party MCPs without rights;
- treating local/simulator evals as proof ChatGPT itself routes correctly;
- maximizing plugin count instead of useful successful invocations.
