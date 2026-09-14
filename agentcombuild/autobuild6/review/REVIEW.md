# review/ — the runtime that will judge this attempt

Status: NOT STARTED (see `../README.md` for the hypothesis).

When the attempt is built, add `check.py` (thin scope wrapper over
`../../autobuild0/reviewkit.py`, following `autobuild2/review/check.py`)
so `GO.sh` picks it up. It must write `VERDICT.json` + `NEXT.md` and exit
nonzero on any FAIL — promotion stays blocked until green.
