from __future__ import annotations
from .experiments import select_world
from .underengineer import plan

def simulate_project(pid):
    """Deterministic sensitivity table. Useful for ordering only; proof ceiling=SIMULATION."""
    p=plan(pid); worlds=select_world(pid)['ranked_worlds']
    rows=[]
    for w in worlds:
        if w['id']=='internal_simulation': continue
        base=w['score']
        rows.append({'world':w['id'],'pessimistic':round(base*0.5,4),'base':base,'optimistic':round(base*1.5,4),
                     'first_moat_event':p['first_real_moat_event']})
    return {'project_id':pid,'proof_state':'SIMULATION_ONLY','canonical_effect':'NONE','rows':rows,
            'rule':'Use this to choose what to test. Never treat these values as usage, revenue, demand or scarce-state evidence.'}
