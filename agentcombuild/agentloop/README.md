# agentloop — the agent harness (working v0)

Implements `agents.md §2–§5`: structured RUN records (shape-enforced),
the seeker stuck-loop (SEARCH → 3 candidates → TEST → LOG, dark validation),
research backends (sim always; GitHub/arXiv over stdlib urllib, injectable
fetcher for hermetic tests), and the compiler (ideas bank, decisions,
merged next-10 leaderboard).

```bash
cd /agentcomfinal/agentcombuild/agentloop
PYTHONPATH=../autobuild1/src:src python3 -m pytest tests/ -q
```

Records live per project: `runs/<project>.jsonl` (see `agents.md §4`).
