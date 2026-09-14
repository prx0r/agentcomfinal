import json,tempfile
from pathlib import Path
from autobuild.canonical import digest
from autobuild.roots import contract_root, plan_root
from autobuild.compiler import compile_plan
from autobuild.underengineer import select_minimum
from autobuild.prebuild import apply_reuse_plan
from autobuild.bridges import qp_bridge,atask_bridge
from autobuild.delta import changeset
from autobuild.validators import evaluate
from autobuild.tristate import TRUE,FALSE,UNKNOWN
from autobuild.accretion import accrue
from autobuild.ledger import append_record,verify_ledger

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())

def test_compile_is_deterministic():
    p=load('examples/breadup_minimum_moat/plan.json'); a=compile_plan(p); b=compile_plan(p)
    assert digest(a['target_spec'])==digest(b['target_spec']); assert a['gate']['result']=='PASS'

def test_underengineer_defers_social_feed():
    p=load('examples/breadup_minimum_moat/plan.json'); u=select_minimum(p['features'])
    assert 'outcome_ledger' in u['selected_ids']; assert 'social_feed' in u['deferred_ids']

def test_prebuild_only_missing_delta():
    p=load('examples/breadup_minimum_moat/plan.json'); t=compile_plan(p)['target_spec']; r=load('fixtures/prebuild_response.json'); out=apply_reuse_plan(t,r)['target_spec']
    assert 'req-outcome-row' in out['reuse']['missing_requirement_ids']; assert 'req-listing-live' not in out['reuse']['missing_requirement_ids']

def test_bridges_reference_contract_and_plan_roots():
    p=load('examples/cmail_authority/plan.json'); t=compile_plan(p)['target_spec']; qb=qp_bridge(t); ab=atask_bridge(t)
    assert qb['contract_root']==contract_root(t); assert ab['contract_root']==contract_root(t)
    assert qb['execution_plan_root']==plan_root(t); assert ab['execution_plan_root']==plan_root(t)
    assert all(x['acceptance']['contract_root']==contract_root(t) for x in qb['task_constructor_specs'])

def test_unknown_does_not_pass():
    v={'kind':'eq','params':{'path':'x','value':1}}
    assert evaluate(v,None)['state']==UNKNOWN; assert evaluate(v,{'x':1})['state']==TRUE; assert evaluate(v,{'x':2})['state']==FALSE

def test_delta_is_exact():
    c=changeset({'x':1,'nested':{'a':2}},{'x':2,'nested':{'a':2,'b':3}}); paths={x['path'] for x in c['changes']}
    assert '$.x' in paths and '$.nested.b' in paths

def test_accretion_keeps_failed_run_and_dedupes_knowledge():
    run=load('fixtures/run_contribution.json')
    with tempfile.TemporaryDirectory() as d:
        path=Path(d)/'a.jsonl'; r1=accrue(path,run); r2=accrue(path,run)
        assert r1['result']=='PASS'; assert r2['duplicates_suppressed']>0; assert '"operational_result":"FAILED"' in path.read_text()

def test_ledger_integrity():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'l.jsonl'; append_record(p,{'a':1}); append_record(p,{'b':2}); assert verify_ledger(p)['result']=='PASS'

def test_completion_circuit_true_only_when_all_true():
    from autobuild.circuit import evaluate, all_of
    c=all_of(['a','b'])
    assert evaluate(c,{'a':'TRUE','b':'TRUE'})=='TRUE'
    assert evaluate(c,{'a':'TRUE','b':'UNKNOWN'})=='UNKNOWN'
    assert evaluate(c,{'a':'TRUE','b':'FALSE'})=='FALSE'

def test_lego_primitive_composition():
    from autobuild.primitives import make_primitive,compose
    p1=make_primitive('observe',[],['item.observation'],'t1','v1')
    p2=make_primitive('list',['item.observation'],['listing.live'],'t2','v2')
    r=compose([p1,p2],[],['listing.live'])
    assert r['result']=='PASS'
    assert [s['primitive_id'] for s in r['steps']]==[p1['id'],p2['id']]

def test_resource_consuming_duplicate_only_run_fails_accretion_gate():
    run=load('fixtures/run_contribution.json')
    with tempfile.TemporaryDirectory() as d:
        path=Path(d)/'a.jsonl'
        accrue(path,run)
        second=accrue(path,run)
        assert second['new_knowledge_records']==0
        assert second['accretion_gate']=='FAIL'

def test_strategic_admission_requires_kill_condition():
    from autobuild.admission import validate_strategic
    x=validate_strategic({'decision':'BUILD','durable_scarcity':'x'})
    assert x['result']=='FAIL'
