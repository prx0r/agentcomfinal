# ab1 SPEC (ab1/0.1)

## Pipeline

```
PLAN (json) → specgate → seesaw score → gates → RECEIPT (jsonl store) → report (view)
```

Every stage emits JSON. Markdown/stdout are views, never truth.

## Objects

- **Plan**: `{goal: {statement, acceptance[]}, features[]}`. Feature:
  `{id, description, acceptance, evidence[{kind, ref}], moat{E,X,F,N,T,B},
  cost, software_substitutable}`. Missing acceptance or declared evidence =
  refused (atask rule).
- **Score**: `{id, S, action}` with `S=(E·X·F·N·T·β)/cost`, missing moat keys
  default 1, cost default 1. Actions OWN/BUILD/BUY/REUSE/VALIDATE/WATCH/DROP.
  Software-substitutable with hard-moat ≤1 can never be OWN.
- **Gate result**: `{id, inputs, verdict: PASS|FAIL, proof}`. Unknown id =
  FAIL. Raise = FAIL. `program_hash` = sha256(gate source).
- **Receipt**: `{protocol: ab1/0.1, transition: BUILD, subject, state_before,
  proposal, evidence, gates[], now, passed, proof_level: V0-unsigned,
  state_after, id}`. `id = "receipt:" + sha12(canonical(body minus id))`.
  Unsigned in attempt 1 (signing is attempt 2).
- **Store**: jsonl lines `{prev, receipt}`; genesis prev = `GENESIS`.

## Gates (built-in)

`specgate-v1` (plan valid) · `evidence-declared-v1` (every feature has
kind+ref evidence) · `two-sources-v1` (≥2 distinct source ids) ·
`score-threshold-v1` (project value ≥ min) · `no-duplicate-v1` (ids unique).

## State

`{cursor, projects: {subject: {status, value, actions}}}`. PASS → proposal
applied, cursor+1. FAIL → state unchanged. `now` injected (`--now`), default
fixed `2026-09-14T00:00:00Z` so output is byte-deterministic.
