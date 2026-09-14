# SESSION LOG 20260914-082249

Steps: 12, failures: 0. Bank: `/agentcomfinal/agentcombuild/runs/sess-20260914-082249`. All artifacts below.

## suite:ab1 rc=0 330ms
```
/usr/bin/python3 -m pytest tests/ -q
```
.................                                                        [100%]
17 passed in 0.04s

## suite:ab2 rc=0 523ms
```
/usr/bin/python3 -m pytest tests/ -q
```
...............                                                          [100%]
15 passed in 0.24s

## suite:ab3 rc=0 1643ms
```
/usr/bin/python3 -m pytest tests/ -q
```
.............................                                            [100%]
29 passed in 1.34s

## suite:agentloop rc=0 397ms
```
/usr/bin/python3 -m pytest tests/ -q
```
......................................                                   [100%]
38 passed, 1 skipped in 0.09s

## suite:core rc=0 1064ms
```
/usr/bin/python3 -m pytest core/tests/ -q
```
........................                                                 [100%]
24 passed in 0.77s

## suite:compiler rc=0 411ms
```
/usr/bin/python3 -m pytest autobuild/compiler/ trajectory/test_formats.py contracts/ -q
```
.....................                                                    [100%]
21 passed in 0.13s

## suite:openai-native rc=0 601ms
```
/usr/bin/python3 -m pytest tests/ -q
```
.......................                                                  [100%]
23 passed, 1 skipped in 0.31s

## suite:agentcom rc=0 3246ms
```
/usr/bin/python3 -m pytest agentcom/tests/ -q
```
......                                                                   [100%]
6 passed in 2.96s

## e4 rc=0 88ms
```
/usr/bin/python3 experiments/policies/tournament_e4.py
```
    ]
  ],
  "mode": "SIMULATED"
}

## uk-compile rc=0 45ms
```
/usr/bin/python3 -c from autobuild.compiler import actuality_compile as A;import json; c=A.compile_uk();open('trajectory/candidates/uk_contract.json','w').write(json.dumps(c, indent=2));print('leaves:', len(c['leaves']), 'unprovable:', c['unprovable'])
```
leaves: 7 unprovable: []

## redteam rc=0 122ms
```
/usr/bin/python3 agentcombuild/autobuild0/redteam_ab12.py
```
HELD  R6 smuggled-gate                   
HELD  R7 acceptance-edit                 receipt pins old bytes; new acceptance needs new ContractRoot (ab4)
HELD  R8 unknown-gate                    
--- 9 held, 0 open ---

## live-wire rc=0 4650ms
```
/home/ubuntu/.venvs/agentcom/bin/python -m pytest agentcombuild/agentloop/tests/test_tracing_live.py experiments/policies/test_sdk_policy.py experiments/openai_native/tests/test_wire_live.py -q
```
.....                                                                    [100%]
5 passed in 3.38s
OPENAI_API_KEY is not set, skipping trace export

