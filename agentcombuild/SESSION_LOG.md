# SESSION LOG 20260914-091011

Status: LOCAL_GREEN / LIVE_INCOMPLETE. Steps: 13, failures: 0. Bank: `/agentcomfinal/agentcombuild/runs/sess-20260914-091011`.

Modes: LOCAL = this machine; SIMULATED = fixtures standing in for providers; LIVE = real provider (UNKNOWN until executed).

## suite:ab1 rc=0 391ms
```
/usr/bin/python3 -m pytest tests/ -q
```
.................                                                        [100%]
17 passed in 0.04s

## suite:ab2 rc=0 557ms
```
/usr/bin/python3 -m pytest tests/ -q
```
...............                                                          [100%]
15 passed in 0.25s

## suite:ab3 rc=0 1675ms
```
/usr/bin/python3 -m pytest tests/ -q
```
.............................                                            [100%]
29 passed in 1.35s

## suite:agentloop rc=0 430ms
```
/usr/bin/python3 -m pytest tests/ -q
```
......................................                                   [100%]
38 passed, 1 skipped in 0.10s

## suite:core rc=0 1133ms
```
/usr/bin/python3 -m pytest core/tests/ -q
```
.........................                                                [100%]
25 passed in 0.81s

## suite:compiler rc=0 463ms
```
/usr/bin/python3 -m pytest autobuild/compiler/ trajectory/test_formats.py contracts/ -q
```
........................                                                 [100%]
24 passed in 0.15s

## suite:openai-native rc=0 765ms
```
/usr/bin/python3 -m pytest tests/ -q
```
..........................                                               [100%]
26 passed, 1 skipped in 0.40s

## suite:agentcom rc=0 12820ms
```
/usr/bin/python3 -m pytest agentcom/tests/ -q
```
....................                                                     [100%]
20 passed in 12.47s

## e4 rc=0 93ms
```
/usr/bin/python3 experiments/policies/tournament_e4.py
```
    ]
  ],
  "mode": "SIMULATED"
}

## uk-compile rc=0 54ms
```
/usr/bin/python3 -c from autobuild.compiler import actuality_compile as A;import json; c=A.compile_uk();open('trajectory/candidates/uk_contract.json','w').write(json.dumps(c, indent=2));print('leaves:', len(c['leaves']), 'unprovable:', c['unprovable'])
```
leaves: 7 unprovable: []

## redteam rc=0 123ms
```
/usr/bin/python3 agentcombuild/autobuild0/redteam_ab12.py
```
HELD  R6 smuggled-gate                   
HELD  R7 acceptance-edit                 receipt pins old bytes; new acceptance needs new ContractRoot (ab4)
HELD  R8 unknown-gate                    
--- 9 held, 0 open ---

## live-wire rc=0 4939ms
```
/home/ubuntu/.venvs/agentcom/bin/python -m pytest agentcombuild/agentloop/tests/test_tracing_live.py experiments/policies/test_sdk_policy.py experiments/openai_native/tests/test_wire_live.py -q
```
.....                                                                    [100%]
5 passed in 3.62s
OPENAI_API_KEY is not set, skipping trace export

## live-agents-session rc=0 0ms
```
managed session (key-gated)
```
NOT_CONFIGURED

