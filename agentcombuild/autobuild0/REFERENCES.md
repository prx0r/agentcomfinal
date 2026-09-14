# autobuild0 — shared references (pointers, not copies)

All paths absolute. Builds import or read from here; nothing is vendored
except where a file says so. Checked 2026-09-14.

## Local checkouts (ubuntu)

| repo | path | branch | role for autobuild |
|---|---|---|---|
| qp (A-COM kernel) | `/home/ubuntu/qp` | ? | kernel principles + reusable modules (see QP_PRINCIPLES.md) |
| atask (control language) | `/home/ubuntu/atask` | ? | run layer, stoplight proof, keypad; `atask.py`, `ATASK.md`, `VALIDATORS.md` |
| plugin (astra factory) | `/home/ubuntu/plugin` | ? | factory counterpart; `HANDOVER.md`, `apps/` |
| aloop | `/home/ubuntu/aloop` | ? | loop runtime (attempts 5/9) |
| gitgoblin | `/home/ubuntu/gitgoblin` | ? | repo-graph target (autobuild consumers) |
| gg-as | `/home/ubuntu/gg-as` + `/gg-as` | ? | controller kernel |
| seed0 | `/home/ubuntu/seed0` | ? | learning layer above atask presses |
| breadup | `/home/ubuntu/breadup` | ? | commerce-OS demo domain |
| pogtown | `/home/ubuntu/pogtown` | ? | game-truth domain (never in kernel) |
| cmail | `/home/ubuntu/cmail` + `/cmail` (main) | main | comms capability demo |
| aisec | `/home/ubuntu/aisec` + `/aisec` | master | security demo |
| csec | `/home/ubuntu/csec` + `/csec` | ? | security demo |
| voiceagent | `/home/ubuntu/voiceagent` + `/voiceagent` | ? | voice demo |
| ab | `/home/ubuntu/ab` + `/ab` | ? | controller (agentcom platform/kernel) |
| drop | `/home/ubuntu/drop` + `/drop` | ? | fragmented-commerce demo |
| feedify | `/home/ubuntu/feedify` | ? | demand-sensing demo |
| x402 | `/home/ubuntu/x402` | ? | payments rails |
| killfeed | `/home/ubuntu/killfeed` | ? | killfeed-adjacent work |
| agentcom (parent) | `/agentcom` | ? | monorepo map, THESIS/ARCHITECTURE/REPOS |

NOT on ubuntu (remote only): `prx0r/atask` ✓ exists, `prx0r/plugin` ✓
exists — cloned 2026-09-14 to the paths above.

## OpenAI Agents SDK (live dependency, outside the kernel)
- Package: `openai-agents==0.22.2` in `/home/ubuntu/.venvs/agentcom`
  (matches `~/acom-openai/requirements.txt` pin). System python does NOT
  have it — factory suites stay stdlib-only and skip live tests there.
- SDK repo (source + docs): `/home/ubuntu/openai-agents-python`.
- Vendored reference docs: `autobuild0/vendor_docs/openai-agents/`
  (`tracing.md` + `ref/tracing/*` + PROVENANCE.md).
- Consumer: `agentloop/src/loop/tracing.py` (lazy import, mirror fallback);
  live wire-compat proven by `agentloop/tests/test_tracing_live.py` under
  the venv (trace + nested custom spans reach a real TracingProcessor).

## Frontier clones (reference, 2026-09-14)

- `/home/ubuntu/harbor` (harbor-framework/harbor) — trial runtime, ATIF
  spec at `docs/content/docs/agents/trajectory-format.mdx`. Consumer:
  `trajectory/atif.py` (export our trajectories to ATIF shape).
- `/home/ubuntu/letta-trajectory` (@letta-ai/trajectory v0.3.0, TS/bun —
  no Python wrapper), schema at `schema/trajectory-v1.schema.json`.
  Consumer: `trajectory/memory.py` (compact projection in letta shape).
- `/home/ubuntu/cg` (cogymkernel) — canonical local experiment executor:
  `cogym_kernel` imports stdlib-clean; `DeterministicExecutor`,
  content-addressed RunReceipts, hard gates. Consumer: `adapters/cg.py`
  (version + smoke + lane→worldpack manifest). Full AsyncRunner episodes
  run inside /cg, receipts banked here.
- gg-as vs gitgoblin: SAME family, gg-as is the LIVE working copy
  (campaigns, sector configs, run data + history); `gitgoblin/` is the
  reference copy. Canonicalize on gg-as for prebuild data.

## In this repo

- Raw R2 dump: `/agentcomfinal/docs/` + `_manifest.json`
- Unpacked zips: `/agentcomfinal/packages/<slug>/` + `00_IMPORT_README.md`
- Notes: `/agentcomfinal/notes/` — start with
  `scarcity-thesis-moving-scarcity-surface.md`
- Audit: `/agentcomfinal/AUDIT.md` — dupes, themes, gaps
- Plan: `/agentcomfinal/DEV_PLAN.md` — protocols + attempt roadmap

## Canonical picks (don't re-decide per attempt)

- Control plane: `packages/scarce-state-control-plane-v3/`
- XMRBot: `packages/xmrbot-private-procurement-v0.4/`
- Plugin spec: `packages/agentcom-plugin-canonical/` schemas
- Compiler: `packages/autobuild-v0.2/` (+ `docs/00-08`)
- Seesaw scorer: `packages/seesaw-agent-module/` + `~/qp/seesaw/graph.py`
- Kernel: `~/qp/acom/` + `~/qp/schemas/acom.json`
- Runs: `~/atask/atask.py` + `driver.py pulse`

## Schema index (import, don't copy)

- `~/qp/schemas/acom.json` — STATE/CLAIM/EVIDENCE/TASK/RUN/GATE/GRANT/RECEIPT
- `packages/agentcom-plugin-canonical/agentcom_plugin_canonical/schemas/plugin_spec.schema.json`
- `packages/agentcom-plugin-canonical/agentcom_plugin_canonical/schemas/provider_ledger.schema.json`
- `packages/autobuild-v0.2/autobuild/schemas/plan_spec.schema.json`
- `packages/autobuild-v0.2/autobuild/schemas/target_spec.schema.json`
- `packages/autobuild-v0.2/autobuild/schemas/run_contribution.schema.json`
- `packages/campaign-control-plane/campaign-control-plane/schemas/{thesis,checkpoint,event,htask,receipt}.schema.json`
- `packages/scarce-state-control-plane-v2/scarce-state-control-plane/schemas/` (+attested/underengineer/scarce_asset)
- `packages/scarce-state-control-plane-v3/.../schemas/` (+experiment_run, human_task_v3)
- `packages/seesaw-agent-module/seesaw-agent-module/schemas/` (project/feature/disruptive_event)
