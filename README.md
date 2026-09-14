# agentcomfinal

Consolidated import of the R2 `agentcom` bucket — 12 working packages + 16 thesis notes, unpacked, documented, and audited.

- **Raw dump (immutable):** `docs/` — 30 unique files from R2 + `_manifest.json`
- **Working code:** `packages/` — 12 unpacked zips, each with `00_IMPORT_README.md`
- **Theses / notes:** `notes/` — 16 curated docs with sanitized names + frontmatter
- **Audit:** `AUDIT.md` — what we have, dupes, themes, gaps, next steps

## Quickstart

```bash
ls docs/ notes/ packages/
cat AUDIT.md
# per package:
cat packages/<slug>/00_IMPORT_README.md
# run tests where present, e.g.:
python -m pytest packages/autobuild-v0.2/autobuild -q
python -m pytest packages/campaign-control-plane -q
```

## Canonicals (recommended)

- Control plane → `packages/scarce-state-control-plane-v3/`
- XMRBot → `packages/xmrbot-private-procurement-v0.4/`
- Plugin spec/gate → `packages/agentcom-plugin-canonical/`
- Compiler → `packages/autobuild-v0.2/`
- Thesis → `notes/scarcity-thesis-moving-scarcity-surface.md`

See `AUDIT.md §7` for merge plan. Do not commit secrets — R2/GitHub tokens stay in env only.

## Autobuild program (`agentcombuild/` — the factory)

- **Idea:** `agentcombuild/agentcomidea.md` — founding brief
- **Axiom:** `agentcombuild/actuality.md` — Actuality: progress only via externally produced evidence satisfying frozen gates
- **Criteria:** `agentcombuild/agentcomcriteria.md` — binary rubric, seed0 style
- **Gates:** `agentcombuild/GATES.md` — full gate catalog L0–L4
- **Plan:** `agentcombuild/DEV_PLAN.md` — zip review, qp/atask principles, protocols, roadmap
- **Shared refs:** `agentcombuild/autobuild0/` — repo inventory, schema index, qp principles, reviewkit, red-team
- **Attempt 1 (working):** `agentcombuild/autobuild1/` — stdlib oneshot, 17/17 green
- **Attempt 2 (working):** `agentcombuild/autobuild2/` — signed receipts + grant gates, 15/15 green
- **Attempt 3 (working):** `agentcombuild/autobuild3/` — a-log telemetry + Actuality core (probe/judge, CEL, DAG, readback, registry), 29/29 green
- **Agent harness (working):** `agentcombuild/agentloop/` — RUN records, seeker, research backends, compiler, generated policy, knowledge/blockers, tracing adapter, 38/38 green
- **Attempts 4–10:** hypotheses stubbed, see `agentcombuild/DEV_PLAN.md §5`
- **Gitbuild flow:** `agentcombuild/gitbuild/` — worktree lanes, frozen evaluator, notes, promotion; first live demo: scanner-variant tournament (see BUILD_NOTES pattern per experiment)
- **Click go:** `bash agentcombuild/GO.sh` — simulated chain (reviews + suites + demos + redteam)

## Canonical endstate (E0, per `agentcombuild/agentcomdevplan.md`)

- **Ownership:** `CANONICAL.md` — nine modules, one owner each
- **AgentCom core:** `core/` (ids, 8-root lineage, scheduler, portfolio)
- **Contracts:** `contracts/` (strategic/campaign/actuality/trajectory/promotion schemas, enforced by `contracts/check.py`)
- **Autobuild:** `autobuild/` (compiler incl. demoted seesaw + fixed priority, actuality incl. execution envelopes, registry)
- **Adapters:** `adapters/` (real qp/atask/seed0/gitgoblin/seesaw/cg — references, never clones)
- **Lanes + trajectory:** `experiments/policies/`, `trajectory/` (L0–L5 ladder, duality bank, ATIF/memory/OTel bridges)
- **History:** `agentcombuild/autobuild{1,2,3}` frozen; future experiments run as Seed0 lanes
- **OpenAI-native (working sim):** `experiments/openai_native/` — BusinessBundle compiler, Skill-from-policy, session binder, MCP gateways, vault split, two-belt approvals, acceptance chain with real QP receipt, 26/26 green
- **Orchestrator:** `agentcom build <spec>` — one command: spec → contract → reuse → lanes → gates → QP → commit + `dist/` artifact
- **Truth dashboard:** `agentcom actuality` — 10-leaf validation DAG with per-leaf QP receipts (current state: NOT_PROVEN, see output)
