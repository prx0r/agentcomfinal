# GITPLANS.md — git-native system designs for agentcomfinal

Source material reviewed: `~/worker` (WorkerKit, letta runtime, harbor
wiring, `docs/specs/git-*-new`, `git_primitives.py`, `tests/test_letta.py`),
`~/aworker/AWORKER-PLAN.md`. Our side: `GIT_STRATEGY.md` (doctrine),
`experiments/policies/` (lanes), `trajectory/`, lineage, Actuality DAG.
Convention below: REFERENCE = already true in our tree; PLAN = design to
build, with target file and acceptance.

---

## P1. Worktree tournament lanes (PLAN → `experiments/policies/`)

Design (from `git-assets-new` worktree isolation + our `lanes.py`):

```text
main (QP-validated states only)
 │
 ├── worktree lane/policy.seeker3      ContractRoot: cr:9f2..
 ├── worktree lane/policy.gg-first     ContractRoot: cr:9f2..
 ├── worktree lane/policy.direct       ContractRoot: cr:9f2..
 │
 ▼ tournament (identical gates)
 merge winner ──merge──▶ main (+ PromotionReceipt fields in message)
 discard losers (branches kept: banked failures stay queryable)
```

Rule: no lane branch outlives its tournament. Merge or record-and-delete.
`git worktree` gives isolated checkouts without re-cloning; losers are
`git branch -D`'d only after their trajectories land in `trajectory/`.
Acceptance: one script runs 3 worktree lanes on the E4 leaf and merges
only the winner; losers' branches gone, trajectories banked.

## P2. Pinned-run bundles (PLAN → `core/lineage.py` + `trajectory/`)

Design (from `letta-mod.md` run bundles): extend RunRoot/EvidenceRoot from
bare hashes to pinned bundles:

```text
RunRoot = {
  worker_version, memory_commit, skills_commit, workspace_commit,
  opportunity_ref, assessor_ref, trajectory_sha256, artifact_sha256
}
```

Every component a ref, never a blob (Hydra rule). Our lineage `run` and
`evidence` roots gain a `pins{}` map; `verify_chain` additionally asserts
each pin resolves (`git cat-file -e`). Acceptance: tamper any pinned
commit → verification fails naming the exact pin.

## P3. Git-backed agent memory (PLAN → `agentloop` knowledge ledger)

Design (from MemFS + Context Repositories): memory is a real git repo.

```text
memory/  (repo)
├── system/            always loaded (identity, laws, standing facts)
├── skills/            progressive disclosure (loaded on relevance)
├── episodes/          append-only, one file per run
└── candidates/        ACE deltas live here, never on main

reflection subagent ──merge──▶ main (after paired held-out gate)
```

WorkerVersion = refs (`memory_commit`, `skill_commit` + parent), per
`git_primitives.py`. Our knowledge ledger entries gain `memory_ref`
fields; cross-session continuity = fetch + checkout, not context stuffing.
Acceptance: two sessions share one memory repo; second session cites a
fact committed by the first, with the ref.

## P4. Notes-annotated empirics (PLAN → `review/` + `trajectory/`)

Design (from `git notes` spec): attach eval data to commits WITHOUT
mutating them:

```text
commit cr:abc123  (the code that ran)
   └── refs/notes/agentcom/evals → VERDICT.json, cost, gates
   └── refs/notes/agentcom/actuality → leaf TRUE/FALSE/UNKNOWN table
```

`review/check.py` writes its verdict to notes on HEAD as well as to
`VERDICT.json`. History stays immutable; empirics accumulate alongside.
Acceptance: `git log` shows code; `git notes list` shows what reality
said about it, per commit.

## P5. Bisect-driven regression hunting (PLAN → `trajectory/`)

Design (from `git bisect run` spec): when an Actuality leaf flips
TRUE→FALSE/UNKNOWN across runs, bisect the memory/config/commit range:

```text
last-green commit ──bisect run──▶ first-red commit
   └── each step: checkout + re-run probe + judge leaf (no full suite)
```

Output is a single culprit commit + the leaf table diff. Turns "something
regressed" into a named cause with evidence. Acceptance: seeded regression
in a fixture repo is found automatically with the culprit commit cited.

## P6. Signed tags as certified releases (PLAN → promotion flow)

Design (from `worker/.../v12` tags + `.af` certs): promotion mints a
signed tag, not a database row:

```text
candidate primitive/policy
   ↓ replay + holdout pass
   ↓ human/council approver
   ↓
git tag -s promote/<id>  (+ PromotionReceipt fields in tag message)
```

Verification = `git verify-tag` + replay the pinned corpus. Our
`contracts/promotion.schema.json` gains `tag` + `signature` fields.
Acceptance: `verify-tag` passes and the pinned replay reproduces TRUE.

## P7. Campaign-as-bundle export (PLAN → BusinessBundle compiler)

Design (from `.school`/campaign-repro-bundle): extend the bundle compiler
so every BusinessBundle ships git provenance:

```text
business.bundle/
├── ... (existing layout)
└── provenance/
    ├── refs.json      (repo → pinned rev for every input)
    ├── manifest.json  (file → sha256)
    └── bundle.gitbundle (git bundle create --all: refs + history)
```

A bundle is then portable AND re-verifiable offline: unpack, check pins,
replay judges. Acceptance: bundle built on machine A verifies byte-clean
on machine B with `--offline`.

## P8. Harbor-style trial layout (PLAN → `trajectory/`)

Design (from Harbor trials): standardize each attempt directory:

```text
trajectory/attempts/ATT-04/
├── lock.json          execution input manifest (pins, env, policy)
├── result.json        verdict + costs
├── trajectory.json    full event trace
├── verifier/          the exact judges that ran (content ids)
└── artifacts/         outputs with sha256
```

No parallel lock file — `lock.json` IS the lock (single writer rule).
Our `experiments/openai_native` chain output already approximates this;
formalize the shape once and reuse for lanes, pilot, and tournaments.
Acceptance: any attempt dir from any subsystem validates against one schema.

## P9. Regrade without rerun (PLAN → stoplight + bank)

Design (from harbor regrade): when a judge upgrades (CEL→Rego, new
threshold), do NOT rerun the world. Re-judge stored evidence:

```text
stored a-logs / evidence corpus (immutable)
        ↓ new judge version
regrade → new verdict table + diff vs old verdicts
        ↓ flips explained per leaf
```

Our stoplight already recomputes verdicts instead of reading them — extend
that into a `regrade` command over a whole corpus dir. Secret evals always
run with `environment_mode=separate` (RewardKit rule). Acceptance: judge
upgrade regrades 100 stored trajectories with zero probe re-execution and
a per-leaf flip report.

## P10. RewardKit-style multidimensional ranking (PLAN → lanes/scheduler)

Design (from `reward.json`): replace single-number cost ranking with:

```text
reward.json per lane:
  gates_pass (hard gate, lexicographic first)
  cost_usd, wall_ms, tokens, attempts, external_calls, human_minutes
  new_reusable_knowledge, maintainability
```

Winner = gates-pass set, then Pareto/cost rank — never vibes, never raw
speed alone. Feeds the E9 benchmark table directly. Acceptance: tournament
output includes the full reward matrix, and the winner is reproducible
from the matrix by the documented rule.

## P11. Trajectory duality: full + compact (REFERENCE → formalize)

Already half-true here: `RunIntelligence` (rich view) vs RUN record
(compact filed truth). Formalize per ATIF/Letta duality: full trace for
replay/deep audit, ~5x-compact trajectory for scheduler/Seed0 ingestion,
with a mechanical `compact()` transform and a fidelity test (compact
preserves verdicts + costs + winner-relevant fields, drops prose).
Acceptance: scheduler decisions on compact == decisions on full, tested.

## P12. Lifecycle hooks → event bus (PLAN → telemetry adapter)

Design (from letta lifecycle hooks witnessing git events): our OpenAI
event adapter gains git sources — commit/push/merge/PR events normalize
into the same telemetry records as session events:

```text
git event (commit/push/merge/tag/notes)
        ↓ normalize_event(source="git")
trajectory ledger  ← same schema as openai.agents events
```

Then "who changed what, when, with what verdict attached" is one query
across code AND agent telemetry. Acceptance: a merged lane PR appears in
the trajectory bank with its VERDICT note attached, queryable by
contract root.

## Build order (cheapest verdicts first)

P8 (schema only) → P4 (notes writer in review/) → P1 (worktree script on
E4 leaf) → P10 (reward matrix in lanes) → P2 (pins in lineage) →
P9 (regrade command) → P5 (bisect runner) → P7 (bundle provenance) →
P6 (signed tags) → P3 (memory repo) → P12 (git event source) → P11.

Each ships with its acceptance test or it didn't happen.
