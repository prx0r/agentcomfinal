"""Deterministic strategic admission checks before specification compilation."""

def validate_strategic(spec):
    failures=[]
    decision=spec.get('decision')
    if decision not in {'BUILD','VALIDATE','WATCH','REUSE','DROP'}:
        failures.append('unknown strategic decision')
    if decision in {'BUILD','VALIDATE'}:
        if not spec.get('durable_scarcity'):
            failures.append('executable strategy missing durable_scarcity')
        if not spec.get('kill_conditions'):
            failures.append('executable strategy missing kill_conditions')
    return {'gate_id':'autobuild-strategic-admission-v1','result':'PASS' if not failures else 'FAIL','failures':failures}
