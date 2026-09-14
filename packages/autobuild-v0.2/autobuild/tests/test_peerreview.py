import copy,json,tempfile,subprocess,sys
from pathlib import Path
import pytest
from autobuild.compiler import compile_plan
from autobuild.canonical import digest,canonical_bytes
from autobuild.roots import contract_root, plan_root
from autobuild.specgate import validate_target
from autobuild.underengineer import select_minimum
from autobuild.prebuild import apply_reuse_plan
from autobuild.accretion import accrue
from autobuild.bridges import qp_bridge,atask_bridge
from autobuild.ledger import append_record,verify_ledger
from autobuild.promotion import assess_promotion
from autobuild.validator_codegen import materialize

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())

def target():return compile_plan(load('examples/breadup_minimum_moat/plan.json'))['target_spec']

def test_canonical_100x():
    p=load('examples/breadup_minimum_moat/plan.json')
    assert len({digest(compile_plan(copy.deepcopy(p))['target_spec']) for _ in range(100)})==1

def test_nan_refused():
    with pytest.raises(ValueError): canonical_bytes({'x':float('nan')})

def test_bad_validator_refused():
    t=target();t['requirements'][0]['validator']={'nonsense':True}
    assert validate_target(t)['result']=='FAIL'

def test_missing_requirement_id_refused_not_crash():
    t=target();del t['requirements'][0]['id']
    r=validate_target(t);assert r['result']=='FAIL'

def test_feature_cycle_refused_not_recursion():
    p=load('examples/breadup_minimum_moat/plan.json'); p['features'][0]['depends_on']=['outcome_ledger']
    with pytest.raises(ValueError,match='cycle'):select_minimum(p['features'])

def test_unknown_rights_cannot_count_as_reuse():
    t=target();plan={'kind':'REUSE_PLAN','version':'2.1','contract_root':contract_root(t),'input_plan_root':plan_root(t),'entries':[]}
    for r in t['requirements']:
        plan['entries'].append({'requirement_id':r['id'],'action':'REUSE','reuse_fitness':1.0,'candidate':{'kind':'library','name':'x','license':'UNKNOWN','rights':'UNKNOWN'},'reason':'candidate under rights review'})
    out=apply_reuse_plan(t,plan)['target_spec']
    assert out['reuse']['coverage']==0.0
    assert set(out['reuse']['missing_requirement_ids'])=={r['id'] for r in t['requirements']}
    assert all(e['action']=='BLOCK' for e in out['reuse']['components'])

def _run_fact(rid,value,evidence):
    return {'kind':'RUN_CONTRIBUTION','run_id':rid,'contract_root':'x','execution_plan_root':None,'operational_result':'FAILED','cost':1,'duration_ms':1,'tokens':1,'contributions':{'facts':[{'subject':'api','predicate':'works','value':value,'evidence_ids':[evidence]}],'negative_facts':[],'edges':[],'fixtures':[],'components':[],'outcomes':[],'duplicates':[],'unsupported_claims':[]}}

def test_semantic_dedupe_ignores_evidence_provenance():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'a.jsonl';accrue(p,_run_fact('r1',True,'e1')); r2=accrue(p,_run_fact('r2',True,'e2'))
        assert r2['new_knowledge_records']==0 and r2['accretion_gate']=='FAIL'

def test_contradiction_becomes_conflict():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'a.jsonl';accrue(p,_run_fact('r1',True,'e1')); r2=accrue(p,_run_fact('r2',False,'e2'))
        assert r2['conflicts']==1
        assert '"record_type":"CONFLICT"' in p.read_text()

def test_accretion_chain_detects_tamper():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'l.jsonl';append_record(p,{'x':1});append_record(p,{'x':2}); assert verify_ledger(p)['result']=='PASS'
        text=p.read_text().replace('"x":1','"x":9',1);p.write_text(text); assert verify_ledger(p)['result']=='FAIL'

def test_dependency_edges_preserved_in_bridges():
    t=target()
    t['requirements'][1]['depends_on']=[t['requirements'][0]['id']]
    assert validate_target(t)['result']=='PASS'
    qb=qp_bridge(t); q={x['requirement_id']:x for x in qb['task_constructor_specs']}
    ab=atask_bridge(t); a={x['requirement_id']:x for x in ab['tasks']}
    assert q[t['requirements'][1]['id']]['depends_on_requirement_ids']
    assert a[t['requirements'][1]['id']]['blocked_by']

def test_primitive_promotion_requires_heldout_evidence():
    assert assess_promotion(['a','b','c'],[])['result']=='FAIL'
    good=[{'pass':True,'regression':False} for _ in range(10)]
    assert assess_promotion(['a','b','c'],good)['result']=='PASS'
    bad=good+[{'pass':False,'regression':True}]
    assert assess_promotion(['a','b','c'],bad)['result']=='FAIL'

def test_generated_atask_validator_is_executable():
    t=compile_plan(load('examples/cmail_authority/plan.json'))['target_spec']; ab=atask_bridge(t)
    with tempfile.TemporaryDirectory() as d:
        d=Path(d); files=materialize(ab,d/'validators'); assert files
        # domain-control validator has a file evidence selector
        task=next(x for x in ab['tasks'] if x['requirement_id']=='req-domain-control')
        script=d/'validators'/Path(task['validator_filename']).name
        ev=ROOT/'.autobuild/evidence/domain.json'; ev.parent.mkdir(parents=True,exist_ok=True)
        try:
            ev.write_text(json.dumps({'verified':True}))
            proc=subprocess.run([sys.executable,str(script),task['id'],str(d/'tasks.jsonl'),str(d/'alog')],cwd=ROOT,capture_output=True,text=True)
            assert proc.returncode==0
            assert json.loads(proc.stdout)['pass'] is True
        finally:
            if ev.exists():ev.unlink()

def test_feature_dependencies_project_into_requirement_and_atask_dag():
    p=load("examples/breadup_minimum_moat/plan.json")
    t=compile_plan(p)["target_spec"]
    by={r["id"]:r for r in t["requirements"]}
    assert by["req-valuation"]["depends_on"] == ["req-item-json"]
    assert by["req-listing-live"]["depends_on"] == ["req-valuation"]
    assert by["req-outcome-row"]["depends_on"] == ["req-listing-live"]
    ab=atask_bridge(t)
    task_by={x["requirement_id"]:x for x in ab["tasks"]}
    assert task_by["req-item-json"]["blocked_by"] == []
    assert task_by["req-valuation"]["blocked_by"] == [task_by["req-item-json"]["id"]]
    assert task_by["req-listing-live"]["blocked_by"] == [task_by["req-valuation"]["id"]]
    assert task_by["req-outcome-row"]["blocked_by"] == [task_by["req-listing-live"]["id"]]

def test_nonfinite_target_fails_closed_without_exception():
    p=load("examples/breadup_minimum_moat/plan.json")
    t=compile_plan(p)["target_spec"]
    t["features"][0]["scores"]["moat"] = float("nan")
    result=validate_target(t)
    assert result["result"] == "FAIL"
    assert result["plan_root"] is None
    assert any("canonically serializable" in x for x in result["failures"])

def test_autobuild_cannot_self_mint_verified_knowledge():
    from autobuild.verified_import import make_verification_import_request, make_verified_record
    req=make_verification_import_request({"subject":"x","predicate":"p","value":1}, "sha256:claimed")
    assert req["epistemic_status"] == "PENDING_EXTERNAL_VERIFICATION"
    import pytest
    with pytest.raises(RuntimeError):
        make_verified_record({"x":1},{"id":"sha256:fake"},True)

def test_prebuild_plan_must_bind_exact_target_root():
    t=target()
    plan={"kind":"REUSE_PLAN","version":"2.1","contract_root":"sha256:wrong","input_plan_root":plan_root(t),"entries":[]}
    with pytest.raises(ValueError,match="contract_root mismatch"):
        apply_reuse_plan(t,plan)

def test_prebuild_rejects_unknown_action_and_nonfinite_fit():
    t=target(); rid=t["requirements"][0]["id"]
    base={"kind":"REUSE_PLAN","version":"2.1","contract_root":contract_root(t),"input_plan_root":plan_root(t),"entries":[]}
    p=copy.deepcopy(base); p["entries"]=[{"requirement_id":rid,"action":"MAGIC","reuse_fitness":1.0}]
    with pytest.raises(ValueError,match="invalid action"):
        apply_reuse_plan(t,p)
    p=copy.deepcopy(base); p["entries"]=[{"requirement_id":rid,"action":"BUILD","reuse_fitness":float("nan")}]
    with pytest.raises(ValueError,match="finite"):
        apply_reuse_plan(t,p)

def test_plan_gate_fails_closed_on_malformed_inputs():
    from autobuild.plangate import validate_plan
    p=load("examples/breadup_minimum_moat/plan.json")
    bad=copy.deepcopy(p); bad["strategic_spec"]=None
    assert validate_plan(bad)["result"] == "FAIL"
    bad=copy.deepcopy(p); bad["features"]=None
    assert validate_plan(bad)["result"] == "FAIL"
    bad=copy.deepcopy(p); bad["features"][0]["requirements"]=None
    assert validate_plan(bad)["result"] == "FAIL"
    bad=copy.deepcopy(p); bad["features"][0]["scores"]["moat"]=float("nan")
    r=validate_plan(bad); assert r["result"] == "FAIL" and r["plan_root"] is None

def test_contract_root_stays_frozen_across_reuse_plan_while_plan_root_changes():
    from autobuild.roots import contract_root, plan_root
    t=target(); before_contract=contract_root(t); before_plan=plan_root(t)
    out=apply_reuse_plan(t,load("fixtures/prebuild_response.json"))["target_spec"]
    assert contract_root(out) == before_contract
    assert plan_root(out) != before_plan

def test_contract_root_ignores_semantically_unordered_requirement_and_and_order():
    from autobuild.roots import contract_root
    t=target(); a=contract_root(t)
    t2=copy.deepcopy(t)
    t2["requirements"]=list(reversed(t2["requirements"]))
    t2["completion"]["requirement_ids"]=list(reversed(t2["completion"]["requirement_ids"]))
    t2["completion"]["circuit"]["args"]=list(reversed(t2["completion"]["circuit"]["args"]))
    assert contract_root(t2)==a
