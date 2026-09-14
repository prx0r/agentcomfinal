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

step "ab3 suite"
(cd "$ROOT/autobuild3" && PYTHONPATH=../autobuild1/src:src python3 -m pytest tests/ -q) && ok "ab3 suite" || no "ab3 suite"
step "ab3 review"
(cd "$ROOT/autobuild3" && python3 review/check.py) && ok "ab3 review" || no "ab3 review"
step "ab3 demo"
(cd "$ROOT/autobuild3" && PYTHONPATH=../autobuild1/src:src python3 -m ab3.cli demo > /dev/null) && ok "ab3 demo" || no "ab3 demo"

step "redteam"
(cd "$ROOT" && python3 autobuild0/redteam_ab12.py > /dev/null) && ok "redteam" || no "redteam"

step "agentloop suite"
(cd "$ROOT/agentloop" && PYTHONPATH=../autobuild1/src:src python3 -m pytest tests/ -q) && ok "agentloop suite" || no "agentloop suite"
step "agentloop review"
(cd "$ROOT/agentloop" && python3 review/check.py) && ok "agentloop review" || no "agentloop review"

step "core suite (E0 canonical)"
(cd "$ROOT/.." && PYTHONPATH=/agentcomfinal python3 -m pytest core/tests/ -q) && ok "core suite" || no "core suite"

step "openai-native-0 suite"
(cd "$ROOT/../experiments/openai_native" && PYTHONPATH=src:/agentcomfinal/agentcombuild/agentloop/src:/agentcomfinal python3 -m pytest tests/ -q) && ok "openai-native suite" || no "openai-native suite"

step "compiler + E4 tournament suite"
(cd "$ROOT/.." && PYTHONPATH=/agentcomfinal python3 -m pytest autobuild/compiler/ trajectory/test_formats.py contracts/ -q) && ok "compiler+E4+formats+contracts suite" || no "compiler+E4+formats+contracts suite"

echo "--- chain: $pass ok, $miss miss ---"
[ "$miss" -eq 0 ]
