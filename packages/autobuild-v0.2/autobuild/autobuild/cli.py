import argparse,json
from pathlib import Path
from .compiler import compile_plan
from .plangate import validate_plan
from .specgate import validate_target
from .underengineer import select_minimum
from .prebuild import make_request,apply_reuse_plan
from .bridges import qp_bridge,atask_bridge
from .delta import changeset
from .accretion import accrue
from .canonical import digest
from .report import target_markdown
from .roots import contract_root, plan_root, lineage_root

def load(p):return json.loads(Path(p).read_text())
def save(p,obj):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,sort_keys=True)); return p

def main():
    ap=argparse.ArgumentParser(prog="autobuild"); sub=ap.add_subparsers(dest="cmd",required=True)
    c=sub.add_parser("compile"); c.add_argument("plan"); c.add_argument("--out",required=True)
    vp=sub.add_parser("validate-plan"); vp.add_argument("plan")
    v=sub.add_parser("validate"); v.add_argument("target")
    u=sub.add_parser("underengineer"); u.add_argument("plan"); u.add_argument("--threshold",type=float,default=.70)
    p=sub.add_parser("prebuild"); p.add_argument("target"); p.add_argument("--out",required=True)
    ar=sub.add_parser("apply-prebuild"); ar.add_argument("target"); ar.add_argument("plan"); ar.add_argument("--out",required=True)
    b=sub.add_parser("bridges"); b.add_argument("target"); b.add_argument("--out",required=True)
    d=sub.add_parser("diff"); d.add_argument("before"); d.add_argument("after")
    a=sub.add_parser("accrue"); a.add_argument("run"); a.add_argument("--ledger",required=True)
    r=sub.add_parser("report"); r.add_argument("target")
    h=sub.add_parser("hash"); h.add_argument("artifact")
    x=ap.parse_args()
    if x.cmd=="compile":
        result=compile_plan(load(x.plan)); out=Path(x.out); out.mkdir(parents=True,exist_ok=True); save(out/"target_spec.json",result["target_spec"]); save(out/"spec_gate.json",result["gate"]); (out/"TARGET.md").write_text(target_markdown(result["target_spec"])); print(json.dumps({"contract_root":contract_root(result["target_spec"]),"plan_root":plan_root(result["target_spec"]),"lineage_root":lineage_root(result["target_spec"]),"gate":result["gate"]["result"],"out":str(out)},indent=2))
    elif x.cmd=="validate":print(json.dumps(validate_target(load(x.target)),indent=2))
    elif x.cmd=="underengineer":print(json.dumps(select_minimum(load(x.plan).get("features",[]),x.threshold),indent=2))
    elif x.cmd=="prebuild":save(x.out,make_request(load(x.target))); print(x.out)
    elif x.cmd=="apply-prebuild":
        result=apply_reuse_plan(load(x.target),load(x.plan)); save(x.out,result["target_spec"]); save(str(x.out)+".changeset.json",result["changeset"]); save(str(x.out)+".receipt.json",result["receipt"]); print(x.out)
    elif x.cmd=="bridges":
        t=load(x.target); out=Path(x.out); out.mkdir(parents=True,exist_ok=True); save(out/"qp_bridge.json",qp_bridge(t)); save(out/"atask_bridge.json",atask_bridge(t)); print(out)
    elif x.cmd=="diff":print(json.dumps(changeset(load(x.before),load(x.after)),indent=2))
    elif x.cmd=="accrue":print(json.dumps(accrue(x.ledger,load(x.run)),indent=2))
    elif x.cmd=="report":print(target_markdown(load(x.target)))
    elif x.cmd=="hash":print(digest(load(x.artifact)))
if __name__=="__main__":main()
