#!/usr/bin/env python3
"""Reproducible adversarial checks used for the 2026-09-14 peer review."""
import copy, json, random
from pathlib import Path

from autobuild.compiler import compile_plan
from autobuild.specgate import validate_target
from autobuild.plangate import validate_plan
from autobuild.prebuild import apply_reuse_plan
from autobuild.roots import contract_root, plan_root
from autobuild.bridges import atask_bridge, qp_bridge
from autobuild.validators import evaluate as eval_validator
from autobuild.circuit import evaluate as eval_completion

ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text())


def target_fuzz(base,n=1000,seed=1337):
    r=random.Random(seed); accepted=crashes=0
    ops=['delete_id','bad_validator','bad_dep','dup_req','unknown_completion','bad_evidence','nan_score']
    for _ in range(n):
        x=copy.deepcopy(base); op=r.choice(ops)
        try:
            if op=='delete_id': x['requirements'][r.randrange(len(x['requirements']))].pop('id',None)
            elif op=='bad_validator': x['requirements'][r.randrange(len(x['requirements']))]['validator']={'nonsense':True}
            elif op=='bad_dep': x['requirements'][r.randrange(len(x['requirements']))]['depends_on']=['req-does-not-exist']
            elif op=='dup_req': x['requirements'].append(copy.deepcopy(x['requirements'][0]))
            elif op=='unknown_completion': x['completion']['requirement_ids'].append('req-does-not-exist')
            elif op=='bad_evidence': x['requirements'][r.randrange(len(x['requirements']))]['evidence_contract']={}
            elif op=='nan_score': x['features'][0]['scores']['moat']=float('nan')
            if validate_target(x)['result']=='PASS': accepted += 1
        except Exception:
            crashes += 1
    return {'mutations':n,'malformed_accepted':accepted,'crashes':crashes,'failed_closed':n-accepted-crashes}


def plan_fuzz(plan,n=500,seed=7):
    r=random.Random(seed); accepted=crashes=0
    ops=['no_id','no_objective','features_none','feature_no_id','bad_score','strategic_none','kill_none','req_none']
    for _ in range(n):
        x=copy.deepcopy(plan); op=r.choice(ops)
        try:
            if op=='no_id': x.pop('id',None)
            elif op=='no_objective': x.pop('objective',None)
            elif op=='features_none': x['features']=None
            elif op=='feature_no_id': x['features'][0].pop('id',None)
            elif op=='bad_score': x['features'][0]['scores']['moat']='wat'
            elif op=='strategic_none': x['strategic_spec']=None
            elif op=='kill_none': x['strategic_spec']['kill_conditions']=None
            elif op=='req_none': x['features'][0]['requirements']=None
            if validate_plan(x)['result']=='PASS': accepted += 1
        except Exception:
            crashes += 1
    return {'mutations':n,'malformed_accepted':accepted,'crashes':crashes,'failed_closed':n-accepted-crashes}


def main():
    plan=load('examples/breadup_minimum_moat/plan.json')
    pre=compile_plan(plan)['target_spec']
    post=apply_reuse_plan(pre,load('fixtures/prebuild_response.json'))['target_spec']
    evidence={
      'req-item-json':{'item':{'category':'camera'}},
      'req-valuation':{'predicted_price':700,'source_count':8},
      'req-listing-live':{'status':'LIVE'},
      'req-outcome-row':{'realized_price':680,'fees':42,'elapsed_seconds':81000,'margin':138},
    }
    def completion(ev):
        states={r['id']:eval_validator(r['validator'],ev.get(r['id']))['state'] for r in post['requirements']}
        return eval_completion(post['completion']['circuit'],states)
    missing=dict(evidence); missing.pop('req-outcome-row')
    wrong=copy.deepcopy(evidence); wrong['req-listing-live']={'status':'DRAFT'}
    ab=atask_bridge(post); qb=qp_bridge(post)
    out={
      'target_fuzz':target_fuzz(pre),
      'plan_fuzz':plan_fuzz(plan),
      'contract_root_stable_across_prebuild':contract_root(pre)==contract_root(post),
      'contract_root':contract_root(pre),
      'plan_root_before':plan_root(pre),
      'plan_root_after':plan_root(post),
      'existing_capability_coverage':post['reuse']['coverage'],
      'missing_requirement_ids':post['reuse']['missing_requirement_ids'],
      'completion':{'all_pass':completion(evidence),'missing_evidence':completion(missing),'wrong_listing':completion(wrong)},
      'atask_dag':[(t['requirement_id'],t['blocked_by'],t['mode']) for t in ab['tasks']],
      'qp':{'claims':len(qb['claim_constructor_specs']),'tasks':len(qb['task_constructor_specs']),'gates':len(qb['gate_constructor_specs']),'grants':len(qb['grant_constructor_specs'])},
    }
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__': main()
