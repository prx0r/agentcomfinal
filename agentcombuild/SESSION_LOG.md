# SESSION LOG 20260914-081113

Steps: 11, failures: 0. Bank: `/agentcomfinal/agentcombuild/runs/sess-20260914-081113`. All artifacts below.

## suite:ab1 rc=0 325ms
```
/usr/bin/python3 -m pytest tests/ -q
```
.................                                                        [100%]
17 passed in 0.04s

## suite:ab2 rc=0 558ms
```
/usr/bin/python3 -m pytest tests/ -q
```
...............                                                          [100%]
15 passed in 0.23s

## suite:ab3 rc=0 1638ms
```
/usr/bin/python3 -m pytest tests/ -q
```
.............................                                            [100%]
29 passed in 1.33s

## suite:agentloop rc=0 370ms
```
/usr/bin/python3 -m pytest tests/ -q
```
......................................                                   [100%]
38 passed, 1 skipped in 0.08s

## suite:core rc=0 1053ms
```
/usr/bin/python3 -m pytest core/tests/ -q
```
.......................                                                  [100%]
23 passed in 0.76s

## suite:compiler rc=0 468ms
```
/usr/bin/python3 -m pytest autobuild/compiler/ trajectory/test_formats.py contracts/ -q
```
...................                                                      [100%]
19 passed in 0.14s

## suite:openai-native rc=0 607ms
```
/usr/bin/python3 -m pytest tests/ -q
```
....................                                                     [100%]
20 passed, 1 skipped in 0.31s

## e4 rc=0 90ms
```
/usr/bin/python3 experiments/policies/tournament_e4.py
```
    ]
  ],
  "mode": "SIMULATED"
}

## uk-compile rc=0 43ms
```
/usr/bin/python3 -c from autobuild.compiler import actuality_compile as A;import json; c=A.compile_uk();open('trajectory/candidates/uk_contract.json','w').write(json.dumps(c, indent=2));print('leaves:', len(c['leaves']), 'unprovable:', c['unprovable'])
```
leaves: 7 unprovable: []

## redteam rc=0 121ms
```
/usr/bin/python3 agentcombuild/autobuild0/redteam_ab12.py
```
HELD  R6 smuggled-gate                   
HELD  R7 acceptance-edit                 receipt pins old bytes; new acceptance needs new ContractRoot (ab4)
HELD  R8 unknown-gate                    
--- 9 held, 0 open ---

## live-wire rc=0 4829ms
```
/home/ubuntu/.venvs/agentcom/bin/python -m pytest agentcombuild/agentloop/tests/test_tracing_live.py experiments/policies/test_sdk_policy.py experiments/openai_native/tests/test_wire_live.py -q
```
.....                                                                    [100%]
5 passed in 3.48s
OPENAI_API_KEY is not set, skipping trace export

