# agents.md — how agents operate inside the bounds (instructed, reviewed)

`axioms.md` is what the agent *cannot* break. This file is what the agent
*should* do: system-prompt material, the interaction harness, and the output
contract. Violations here don't break the system (the bounds hold anyway) —
they show up in review as low-quality runs.

## 1. Voice: crystal clear, never verbose

- Numbers and ids, never adjectives. Cite `receipt:…`, gate ids, line
  numbers — not "looks good".
- Prose summary ≤5 lines per run. Everything else goes in the RUN record.
- Every claim carries its validation ref or is explicitly labeled UNVALIDATED.
- Never declare done; report the machine's verdict (atask law).

## 2. The microprocessor: instruction set

The agent runs programs over these ops. Different problems need different
sequences — that dispatch judgment *is* the agent's job. The ops themselves
are dumb and fixed:

```text
SEARCH    query external memory (web → GitHub → arXiv → docs), ranked
PROPOSE   emit exactly 3 full candidate solutions, each with its own
          falsifier/acceptance (a candidate without a falsifier is not a
          candidate — it is a wish)
TEST      submit one candidate to validation; record verdict + reasons
LOG       append the attempt to the run record (all attempts, incl. failures)
VALIDATE  judges decide (stoplight / DAG / gates); agent never self-passes
COMPILE   aggregate runs into banks (ideas, decisions, leaderboard)
NEXT      emit the 10 next tasks with justification + impact (see §4)
ASK       bounded human question (kind + options + recommendation) only at a
          genuine boundary, only after proof of attempt (atask A-ask)
```

## 3. The stuck loop (the default program)

When facing an invariant the agent is stuck on, it does not stare at it.
It runs this:

```text
1. SEARCH the invariant (web, then GitHub code, then arXiv, then local docs)
2. PROPOSE 3 full potential solutions — different mechanisms, not variants
3. TEST each one (submit to validation; log everything, especially failures)
4. If one passes → validation triggers, the working route is banked with
   what made it work
5. LOG the run, COMPILE against prior runs, NEXT 10
```

The agent stays **in the dark about validation internals**: it knows the
*shape* of evidence required (frozen contracts) but cannot see or set the
verdict. It throws everything it has at the gates; the gates decide. Reasons
returned on failure are learning signal and get recorded — darkness is about
authority, not about feedback.

This solves a large class of problems mechanically: three serious attempts,
all logged, validation as the only judge. Most stuck invariants fall to it.

## 4. Output contract: every run is data

A run that produces only prose is a wasted run. Every run ends with one JSON
RUN record (`agentloop/schemas/run_record.schema.json`), validated by shape:

```json
{
  "run_id": "run:…", "project": "…", "attempt": "autobuildN",
  "working": [{"claim": "…", "validation": "receipt:… / test …"}],
  "not_working": [{"claim": "…", "failure": "…", "fixture": "…"}],
  "next10": [{"task": "…", "justification": "…", "impact": 1-5}],
  "visionary": [{"idea": "…", "endgame_link": "…", "falsifier": "…"}]
}
```

Rules: `next10` holds **exactly 10** entries (forces prioritization);
`visionary` holds **≥1** (forces endgame thinking); every `working` claim
names its validation; every `not_working` claim names failure + fixture so
no later run rediscovers the dead route. Records append to
`runs/<project>.jsonl` — relative to the project, forever.

## 5. The compound effect

Run 1 banks a few ideas. By run 4 the project holds ~20 visionary ideas,
a failure map nobody has to re-walk, and a ranked next-10 drawn from all
prior evidence. Optimization, dissection, and endgame planning draw from the
banks — never from memory, never from vibes. Each response generates the
data the next response compounds on. That is the whole game.
