# GIT_STRATEGY.md — git as infrastructure, not just history

Git is the cheapest distributed primitive store we have: content-addressed,
branched, signed, replicated. Use it as machine infrastructure wherever the
semantics already match, instead of rebuilding those properties in Python.

## 1. Branches are lanes; merges are promotions

Seed0 lanes map 1:1 onto git branches (or worktrees for live isolation):

```text
main                      <- only QP-validated, reviewed states
lane/policy.seeker3       <- one execution policy, one ContractRoot
lane/policy.gitgoblin-first
lane/contract-<short>     <- short-lived experiment branches
```

Tournament winner merges to main. The merge IS the promotion ceremony:
CI (gates) + human review (ugly/ambiguous cases) + merge commit message
carrying the PromotionReceipt fields (subject, evidence, replay, approver).
Rejected lanes are kept (banked failures are queryable) but never merged.
`git worktree` gives each lane an isolated checkout without re-cloning.

Rule: no lane branch lives past its tournament. Merge or record-and-delete.

## 2. Existing projects' GitHub as the component universe

Already established practice, now doctrine:

- **Pin, don't float**: every external repo dependency records
  `repo + rev` (STACK.md pin pattern: `prx0r/atask @ d091d46`). Upstream
  moves → mirror-test the new pin → adapt → move the pin. Floating `main`
  is how reproducibility dies.
- **Clone shallow, read locally**: `--depth 1` + grep/AST is the prebuild
  archaeology loop (already in `adapters/gitgoblin.py`). The network is for
  fetching; judgment stays local and deterministic.
- **Activity is CODE_PRESENT, never PROVEN**: commit velocity, stars,
  recency feed prioritization heuristics only. The campaign gate
  (`commits-not-proof`) stays red until an Actuality leaf turns TRUE.
- **Remote tree as independent readback**: "agent pushed X" is verified by
  `git ls-remote` / fetched tree containing the change — the canonical
  example of independent readback for push claims. Implement as a readback
  primitive when the pilot needs it (E3/E6).
- **PRs as promotion gates**: learned primitives/policies graduate via PR
  (diff + CI + reviewer) exactly like code. A merged promotion PR with
  green gates *is* a PromotionReceipt with a human approver field filled.

## 3. Tags and ledgers for releases and money

- Releases are annotated tags from green main only (`v0.x.y`), per atask
  release discipline. Tagging is a governed transition: suite + acheck +
  receipted ledger entry first.
- Money movement keeps its own ledger (aworker pattern: every mutation
  receipted with content-addressed ids). `git log --grep=ledger` should be
  able to reconstruct spend per campaign; provider invoices remain the
  audit source of truth, the ledger is the brake input.

## 4. What git does NOT do (boundaries)

- Git does not judge truth (QP does), schedule work (AgentCom does), or
  prove behavior (validators do). A green CI badge on a branch is
  CODE_PRESENT + TESTS_GREEN — strong signals, still not PROVEN.
- Never store secrets in git to "share with the agent" — env/vault/QP
  gateway only. The secret-scan that caught our Pinterest token is load-
  bearing infrastructure; keep push protection ON.
- Never rewrite published history (`main`, tags). Lane branches may rebase
  while private; merged history is append-only, mirroring the event stores.

## 5. Concrete next applications (for agentbuild1 and friends)

- `agentbuild1`-style attempts: one branch per attempt (`exp/agentbuild-N`),
  nightly tournament merges the winner's *learnings* (not code) into main
  as trajectory records + candidate lessons.
- Prebuild before every BUILD: `gitgoblin.search_local` over pinned
  checkouts first, remote entity search second, BUILD only on miss (already
  the gate; this doc is its rationale).
- Break-glass: if the event store is ever lost, `main` + tags + ledgers
  reconstruct portfolio state to last green — git as the disaster-recovery
  tier. Test the restore yearly, not during the disaster.
