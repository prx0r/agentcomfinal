import json
from pathlib import Path
from autobuild.compiler import compile_plan
from autobuild.prebuild import apply_reuse_plan
from autobuild.validators import evaluate as eval_validator
from autobuild.circuit import evaluate as eval_completion
from autobuild.specgate import validate_target

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())

def test_breadup_end_to_end_true_unknown_false():
    plan=load('examples/breadup_minimum_moat/plan.json')
    target=compile_plan(plan)['target_spec']
    target=apply_reuse_plan(target,load('fixtures/prebuild_response.json'))['target_spec']
    assert validate_target(target)['result']=='PASS'
    evidence={
      'req-item-json':{'item':{'category':'camera'}},
      'req-valuation':{'predicted_price':700,'source_count':8},
      'req-listing-live':{'status':'LIVE'},
      'req-outcome-row':{'realized_price':680,'fees':42,'elapsed_seconds':81000,'margin':138},
    }
    states={r['id']:eval_validator(r['validator'],evidence.get(r['id']))['state'] for r in target['requirements']}
    assert eval_completion(target['completion']['circuit'],states)=='TRUE'
    states_unknown={r['id']:eval_validator(r['validator'],None if r['id']=='req-outcome-row' else evidence.get(r['id']))['state'] for r in target['requirements']}
    assert eval_completion(target['completion']['circuit'],states_unknown)=='UNKNOWN'
    evidence_bad=dict(evidence); evidence_bad['req-listing-live']={'status':'DRAFT'}
    states_false={r['id']:eval_validator(r['validator'],evidence_bad.get(r['id']))['state'] for r in target['requirements']}
    assert eval_completion(target['completion']['circuit'],states_false)=='FALSE'

def test_claimed_economic_validation_requires_structured_qp_circuit():
    t=compile_plan(load('examples/breadup_minimum_moat/plan.json'))['target_spec']
    assert validate_target(t)['result']=='PASS'
    del t['economic_validation']['qp_circuit']
    r=validate_target(t)
    assert r['result']=='FAIL'
    assert any('qp_circuit' in x for x in r['failures'])
