# review/ — the runtime that judges this harness

`check.py` runs the suite + shape/file/ban checks and writes
`VERDICT.json` + `NEXT.md`. Same statuses as attempts: any FAIL blocks.

```bash
cd /agentcomfinal/agentcombuild/agentloop && python3 review/check.py
```
