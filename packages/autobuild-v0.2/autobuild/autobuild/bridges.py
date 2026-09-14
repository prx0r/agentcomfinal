from .canonical import digest, content_id
from .roots import contract_root, plan_root, lineage_root


def qp_bridge(target):
    """Emit adapter specs, never counterfeit QP canonical objects/ids.
    /qp constructors remain the only source of QP object identities.

    ContractRoot freezes WHAT counts as success. ExecutionPlanRoot binds the
    current reuse/build route so run provenance remains exact without changing
    target identity.
    """
    croot=contract_root(target); proot=plan_root(target); lroot=lineage_root(target)
    claims=[]; tasks=[]; gates=[]; grants=[]
    missing=set(target.get("reuse",{}).get("missing_requirement_ids",[]))
    for r in target.get("requirements",[]):
        spec_id=content_id("claimspec",{"contract":croot,"requirement":r["id"]})
        claims.append({
          "kind":"QP_CLAIM_CONSTRUCTOR_SPEC","spec_id":spec_id,"requirement_id":r["id"],
          "constructor":"make_claim","args":{"statement":r["statement"],"domain":f"autobuild.{target['id']}","result":"UNKNOWN"},
          "contract_root":croot,"execution_plan_root":proot,
          "note":"Adapter must retain mapping requirement_id -> QP-returned claim.id."
        })
    for r in target.get("requirements",[]):
        gate_spec_id=content_id("gatespec",{"contract":croot,"requirement":r["id"],"validator":r["validator"]})
        gates.append({
          "kind":"QP_GATE_CONSTRUCTOR_SPEC","spec_id":gate_spec_id,"requirement_id":r["id"],"validator":r["validator"],
          "validator_root":digest(r["validator"]),"contract_root":croot,"execution_plan_root":proot,
          "input_schema":{"evidence_contract":r["evidence_contract"]},
          "note":"Adapter must compile/register equivalent deterministic gate in /qp, then call QP make_gate with QP-owned program_hash."
        })
        tasks.append({
          "kind":"QP_TASK_CONSTRUCTOR_SPEC","spec_id":content_id("taskspec",{"contract":croot,"requirement":r["id"]}),
          "requirement_id":r["id"],"constructor":"make_task",
          "task_kind":"IMPLEMENT_AND_VERIFY" if r["id"] in missing else "INTEGRATE_AND_VERIFY",
          "target_requirement_id":r["id"],"depends_on_requirement_ids":list(r.get("depends_on",[])),
          "acceptance":{"contract_root":croot,"execution_plan_root":proot,"requirement_id":r["id"],"claim_state":"TRUE","gate_spec_id":gate_spec_id,"evidence_contract":r["evidence_contract"]},
          "note":"Adapter resolves target_requirement_id to the actual QP claim id returned by make_claim."
        })
        if r.get("authority",{}).get("required"):
            a=r["authority"]
            grants.append({
              "kind":"QP_GRANT_CONSTRUCTOR_SPEC","requirement_id":r["id"],"constructor":"make_grant",
              "args":{"capability":a.get("capability"),"constraints":a.get("constraints",{}),"predicates":a.get("predicates",[]),"minimum_proof_level":a.get("minimum_proof_level",0)},
              "unresolved_at_compile":["subject","expiry","signature"],
              "note":"Grant cannot be canonicalized by Autobuild; issuer/subject/expiry/signature are runtime authority facts."
            })
    return {
      "kind":"QP_BRIDGE","version":"2.2","contract_root":croot,
      "execution_plan_root":proot,"lineage_root":lroot,
      "claim_constructor_specs":claims,"task_constructor_specs":tasks,
      "gate_constructor_specs":gates,"grant_constructor_specs":grants,
    }


def atask_bridge(target):
    croot=contract_root(target); proot=plan_root(target); lroot=lineage_root(target)
    hard=[r for r in target.get("requirements",[]) if r.get("criticality")=="HARD"]
    index={r["id"]:i for i,r in enumerate(hard)}
    missing=set(target.get("reuse",{}).get("missing_requirement_ids",[]))
    task_id_by_req={r["id"]:content_id("a",{"contract":croot,"requirement":r["id"]}) for r in hard}
    accept=[{"index":i,"requirement_id":r["id"],"statement":r["statement"]} for i,r in enumerate(hard)]
    tasks=[]
    for r in hard:
        ev=r["evidence_contract"]; declared=[]
        if ev.get("command"): declared.append(f"command:{ev['command']}")
        if ev.get("file"): declared.append(f"file:{ev['file']}")
        if not declared: declared.append(f"file:.autobuild/evidence/{r['id']}.json")
        tasks.append({
          "id":task_id_by_req[r["id"]],"summary":r["statement"],"accept":r["statement"],
          "covers_goal":[index[r["id"]]],
          "blocked_by":[task_id_by_req[d] for d in r.get("depends_on",[]) if d in task_id_by_req],
          "mode":"build" if r["id"] in missing else "integrate","declared_evidence":declared,
          "validator_spec":r["validator"],"validator_filename":f"validators/{task_id_by_req[r['id']]}.py",
          "requirement_id":r["id"],"contract_root":croot,"execution_plan_root":proot,
        })
    return {
      "kind":"ATASK_BRIDGE","version":"2.1","contract_root":croot,
      "execution_plan_root":proot,"lineage_root":lroot,
      "goal":{"statement":target["objective"],"acceptance":accept},"tasks":tasks,
      "note":"Adapter materializes validators and invokes local /atask CLI. /atask alone promotes DONE."
    }
