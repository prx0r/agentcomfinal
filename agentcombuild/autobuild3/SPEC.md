# ab3 SPEC (ab3/0.1) — telemetry + judgment

## a-log (agent writes, never judges)

Per-task jsonl: `<dir>/a-logs/<task>.jsonl`. Line:

```json
{"seq": 0, "task": "send-lead-reply", "idx": [0],
 "action": "sent booking offer", "evidence": {"kind": "command", ...},
 "prev": "GENESIS", "hash": "..."}
```

`hash = sha12(canonical({seq,task,idx,action,evidence,prev}))`.
`append` REFUSES (raises, never files): unknown task, out-of-range idx,
`kind: secret`, secret-ish keys/values (`token/password/api_key/private`,
`sk-/ghp_-/pina_-/xox` prefixes, `PRIVATE KEY` blocks).
Evidence kinds: `command {argv[], expect?}` and `file {path, sha256?}` are
re-runnable; `ref` is context-only and never sufficient for coverage.

## covers (task → goal index map, atask rule)

Every feature carries `covers: [goal acceptance indices]`, non-empty, valid.
Queue = plan features. No covers = covers nothing (fail-open forbidden).

## stoplight (judge re-executes everything)

`judge(task)`:
1. Load queue + log. Missing/empty log → NOGO (`no-log`).
2. Chain recompute. Break → NOGO (`chain-broken`).
3. Re-run EVERY line's evidence now: `command` only if argv[0] basename is
   allowlisted (`echo/python3/ls/cat/test/true/false`), else
   `refused-to-run`; `file` checks existence (+hash); `ref` → not-rerunnable.
   Any red re-run → NOGO citing seq (false telemetry fails the task).
4. Coverage: every acceptance idx needs ≥1 green line, else NOGO.
5. Validator `validators/<task>.py [task queue alog]`, 60s timeout, exit 0 +
   single-line `{"pass","reasons"}` JSON; anything else → `validator-error`
   NOGO. Validators are additive-only: pass never excuses failed coverage.

Verdict `{task, verdict: GO|NOGO, reasons[], lines, green}`. GO lines are
written to `verdicts/<task>.json` for convenience — and IGNORED by `acheck`,
which always recomputes (planted verdicts change nothing).

## Status (derived, never declared)

PROPOSED (no lines) · EXECUTING (lines, no GO) · STALE (EXECUTING + old
mtime) · DONE (recomputed GO) · NOGO (recomputed fail). There is no status
field for an agent to set.
