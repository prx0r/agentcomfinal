#!/bin/bash
# GO.sh — one-click simulated chain for the factory.
# Runs every built attempt's suite + review + demo. Simulation only:
# no external actions, no spend, fixed timestamps. Exit 0 = chain green.
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
pass=0; miss=0
step() { echo "=== $1 ==="; }
ok() { echo "OK: $1"; pass=$((pass+1)); }
no() { echo "MISS: $1"; miss=$((miss+1)); }

step "ab1 suite"
(cd "$ROOT/autobuild1" && python3 -m pytest tests/ -q) && ok "ab1 suite" || no "ab1 suite"
step "ab1 review"
(cd "$ROOT/autobuild1" && python3 review/check.py) && ok "ab1 review" || no "ab1 review"
step "ab1 demo"
(cd "$ROOT/autobuild1" && PYTHONPATH=src python3 -m ab1.cli demo > /dev/null) && ok "ab1 demo" || no "ab1 demo"

step "ab2 suite"
(cd "$ROOT/autobuild2" && PYTHONPATH=../autobuild1/src:src python3 -m pytest tests/ -q) && ok "ab2 suite" || no "ab2 suite"
step "ab2 review"
(cd "$ROOT/autobuild2" && python3 review/check.py) && ok "ab2 review" || no "ab2 review"
step "ab2 demo"
(cd "$ROOT/autobuild2" && PYTHONPATH=../autobuild1/src:src python3 -m ab2.cli demo > /dev/null) && ok "ab2 demo" || no "ab2 demo"

echo "--- chain: $pass ok, $miss miss ---"
[ "$miss" -eq 0 ]
