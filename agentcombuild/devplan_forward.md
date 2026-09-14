# devplan_forward.md — projected plan from here (2026-09-14)

Status: PROJECTED. Base: `8ef23a4` (GO 15/15 green). This plan starts from
verified state, not ambition. Anything listed as proven below has a test or
an artifact behind it; everything else is explicitly marked OPEN.

---

# 0. Honest ledger (start here, no exceptions)

## PROVEN (test or artifact on disk)

```text
E0 canonicalization ............ CANONICAL.md + 9 modules + isolation gate green
ab1/ab2/ab3 frozen ............. historical suites green, never extended
Actuality core ................. DAG + CEL + readback + registry, 29/29
Grants + signatures ............ fail-closed matrix green (sim keys)
A-log + stoplight .............. re-execution, forgery/NOGO, secrets refused
Agent harness .................. RUN records enforced, seeker, compiler, 38/38
E2 compiler .................... 7-leaf UK DAG, contract-stable/plan-moves
E4 tournament .................. 3 lanes + rogue disqualified, lessons proposed
Real QP constructors ........... claim/task/gate/grant ids minted by ~/qp
Real QP settlement ............. transition + settle + verify green (local)
Real atask cycle ............... sandbox init/add/run/finish green
Real seed0 propose ............. candidate lessons from tournament failures
Wire compat .................... official MCP handshake + SDK constructors live
Contracts enforced ............. 5 schemas checked incl. real objects
Duality bank ................... file + ATIF + compact + fidelity gate
```

## SIMULATED (honest doubles, same shapes)

```text
Provider channels .............. MCP transport, readback, send — all fixtures
Live Agents API ................ no key on box; session binder shaped, uncalled
Voice/telephony ................ structural placeholders only
OPA/Rego + WASM judges ........ specified, not implemented
GitGoblin remote ............... local archaeology real; entity API unwired
```

## OPEN (known gaps, owned)

```text
GitHub CI statuses ............. workflows not yet committed; all green is local-only
Trajectory bank contents ....... infrastructure banked, zero live trajectories
Promotion flow ................. schema exists, never exercised end-to-end
Memory/context layer ........... projector wired, no retrieval bottleneck yet
Sandbox escalation ............. LOCAL_FAST only; risk ladder untriggered
Clock trust .................... caller-supplied `now` (documented limitation)
Judgment provenance ............ gates check shape; pipeline provides provenance
Second-run improvement ......... the terminal test, never attempted
Live permission ................ no business, no key, no delegated credential
```

Rule for everything below: never work a higher phase while its dependency
is still simulated. The phase gates enforce this mechanically where
possible, by review where not.

---

# 1. Terminal state (unchanged — the only definition that matters)

```text
RUN 1 → verified external transition → structured learning generated
RUN 2 → retrieves that learning → selects a better route
      → reaches equivalent actuality at lower cost/time/failures
```

Formally, with $C$ comparable contracts and $K$ the banked knowledge:

$$
E[cost \mid C, K_{n+1}] < E[cost \mid C, K_n]
\quad\text{with gates held fixed}
$$

If gates moved, it isn't improvement — it's redefinition. The benchmark
script must assert gate-sets identical across the two runs.

---

# 2. F1 — independent second machine (next commit)

GitHub currently shows no statuses: all green evidence comes from the same
machine that wrote the code. Fix this before anything live.

```text
.github/workflows/agentcom-contract.yml   (keyless, every push/PR)
  - canonical boundary tests
  - core + compiler + contracts suites
  - openai-native offline tests
  - archive-import prohibition
  - fail-closed security tests (P0)
  - MCP + SDK wire tests (venv install, still keyless)
  - tamper tests + secret scan (patterns, not vibes)

.github/workflows/agentcom-live.yml       (manual dispatch only)
  - genuine provider probes when credentials exist
  - NEVER required by, or blocking, the contract workflow
```

Acceptance: green check on a fresh commit that no local process produced.

---

# 3. F2 — live legs, smallest possible (needs: one API key)

Order matters. Non-consequential first, consequential only after the read
path proves itself against reality for one full week of runs.

```text
F2a  provider read (cmail.read or equivalent)
     action → MCP → real response → normalized event → trajectory bank
     proves: transport, auth, normalization, banking — zero blast radius

F2b  one bounded consequential action (the E6 rehearsal)
     grant → both belts → gateway enforcement → execute → readback →
     QP settlement → receipt in trajectory → L0→L1 advance
     proves: the whole authority chain against a live provider
```

Kill rule: any live failure of unknown cause pauses F2 and opens a
blocker object. Live debugging without a blocker record is forbidden —
the failure corpus is the asset.

---

# 4. F3 — admit agentcom-uk (needs: one real permission)

Still exactly one business, one painful workflow, one minimum delegated
permission, one bounded case — the compiled 7-leaf DAG in
`autobuild/compiler/actuality_compile.py` is already the frozen target,
so admission is a *selection* event (Seesaw → scheduler), not a build.

```text
StrategicDecision (seesaw proposal + human accept)
        ↓ CampaignRoot (project + asset + objective + D_SCARCE_STATE world)
        ↓ ContractRoot (already compiled — verify, don't rewrite)
        ↓ GitGoblin prebuild (local index now, entity API when live)
        ↓ Seed0 lanes (direct / seeker3 / gg-first on the hard leaf)
        ↓ A-Task sandbox DAG (local) → live queue only after F2b green
```

Do not admit a second campaign until the first reaches L1 with a real
receipt. Portfolio breadth before depth is how the scheduler rots.

---

# 5. F4 — bank everything, then compile memory (needs: runs)

The bank exists and is empty of live experience. Fill order:

```text
1. every simulated chain run banks (starts now — free)
2. every tournament banks winner + losers (starts now — free)
3. every live run banks with provider trace ids (needs F2)
4. at 100 banked trajectories: memory compiler v1
   100 trajectories → reinforcing clusters → 20-lesson context pack
   → measured: does the pack improve lane-0 (no-memory) outcomes?
```

The fidelity gate already refuses lossy filings, so bank growth never
degrades the store. If the memory pack shows no measured improvement,
that is a result — publish the negative and keep the bank.

---

# 6. F5 — first real promotion (needs: banked evidence)

Exercise the full ladder once, end to end, on something small and real —
candidate: the `readback.agree.v1` primitive or the `policy.seeker3`
lane weighting:

```text
OBSERVATION (banked trajectories show readback checks catching mismatch)
  → CANDIDATE_PRIMITIVE (registry entry, versioned)
  → replay vs historical contracts + holdout set
  → human approver + signed tag (PromotionReceipt fields filled)
  → available capability, watched for 30 days
```

If replay or holdout fails, the candidate dies in public with reasons.
A promotion system that has never refused anything is decoration.

---

# 7. F6 — memory/context layer (trigger-gated, NOT scheduled)

Build this only when retrieval becomes the measured bottleneck:

```text
TRIGGER: >200 banked trajectories AND lane setup routinely re-derives
         known facts (measured: same research re-run ≥3× for one fact)
```

Until then the compiler banks + git-backed notes are sufficient, and a
memory service would be latency tax without a customer. When triggered:
MemFS-shaped repo per persistent worker (`system/` always loaded,
`knowledge/` progressive), promotion scored on
adherence/retrievability/generalization/hygiene (already specified in
`trajectory/memory.py`), memory commits as policy revisions competing in
Seed0 lanes — never as truth.

---

# 8. F7 — sandbox escalation (risk-derived, not architectural)

```text
LOCAL_FAST ........ default: known repo, known agent, no dangerous creds
OPENAI_SANDBOX .... triggers: unknown deps, agent-written install scripts,
                    broader shell than the envelope allows
HARD_ISOLATED ..... triggers: third-party code, multi-tenant, serious creds,
                    financial authority, adversarial workloads
```

The contract declares its execution class; the runner refuses to execute
above the contract's class and logs below it as waste. Containerize on
evidence of need (a realized isolation failure or a contract that demands
it), never on anxiety.

---

# 9. Benchmarks (E7–E9, hard numbers or they didn't happen)

```text
E7  outcome changes scheduling: show one scheduler decision BEFORE and
    AFTER a verified outcome where the AFTER differs BECAUSE of it
    (decision diff with the outcome redacted as control).

E8  governed learning live: one candidate primitive/policy passes
    replay + holdout + human approval and receives a PromotionReceipt;
    one candidate visibly FAILS the same path (a gate that never says
    no is not a gate).

E9  decisive benchmark: same ContractRoot class, pre/post promotion
    history compared on success probability, attempts-to-TRUE, tokens,
    wall time, USD, external calls, human minutes, regressions —
    gates byte-identical between eras.
```

---

# 10. Priority order (do not reorder without a written reason)

| # | Work | Unblocks | Needs |
|---|---|---|---|
| 1 | F1 CI second machine | trust in all green | nothing — code only |
| 2 | F4 bank-every-run habit | memory compiler later | nothing — code only |
| 3 | F2a live read leg | provider reality | one API key |
| 4 | F3 campaign admission | E6 meaning | one permission |
| 5 | F2b bounded live action | E6 proof | F2a green + grant |
| 6 | F5 first promotion | learning loop | banked evidence |
| 7 | F6 memory layer | scale | measured bottleneck |
| 8 | F7 sandbox escalation | untrusted work | realized need |

Do NOT prioritize: dashboard polish, plugin features, scheduler richness,
WASM/Rego judges, second campaign, voice, OPA policies, embeddings —
until the table above says so.

---

# 11. Standing rules for the whole road

```text
Simulation is labeled or it is lying.
Gates identical across compared eras or the comparison is void.
No lane branch outlives its tournament (merge or record-and-delete).
No trajectory without provenance (contract + candidate SHA + policy).
No promotion without a refusal somewhere in the same batch.
No new module without an owner in CANONICAL.md.
No dependency without a pin (repo + rev).
```

And the one-sentence version:

> **Agents speculate. Reality validates. QP commits. History compounds —
> and from here on, every claim links to the test or artifact that would
> prove it wrong.**
