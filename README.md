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
- **Agent harness (working):** `agentcombuild/agentloop/` — RUN records, seeker, research backends, compiler, generated policy, 27/27 green
- **Attempts 4–10:** hypotheses stubbed, see `agentcombuild/DEV_PLAN.md §5`
- **Click go:** `bash agentcombuild/GO.sh` — simulated chain (reviews + suites + demos + redteam)
