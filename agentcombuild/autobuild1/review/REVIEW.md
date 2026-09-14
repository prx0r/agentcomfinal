# review/ — the runtime that judges the attempt

`check.py` measures this attempt against its scope rows in
`../agentcomcriteria.md` and writes two outputs:

- `VERDICT.json` — machine verdict (criteria statuses, test counts, banned hits)
- `NEXT.md` — what the next run should do (carried debt + next scope)

Run it:

```bash
cd /agentcomfinal/agentcombuild/autobuildN
python3 review/check.py
```

Statuses: PASS / PARTIAL / DEFERRED / FAIL. Any FAIL (or red suite) blocks
promotion — fix the link, don't add features.
