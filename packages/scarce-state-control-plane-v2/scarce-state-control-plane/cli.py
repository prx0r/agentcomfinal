#!/usr/bin/env python3
import argparse,json
from runtime.model import projects,project,ROOT
from runtime.validators import validate_checkpoint
from runtime.graph import assert_acyclic,ready
from runtime.underengineer import plan,ranked,feature_allowed,order
from runtime.scarcity import declared_assets,ledger,substitution_summary

def cmd_check(args):
    assert_acyclic(); total=0; fixture_pass=0
    for p in projects():
        ev=ROOT/'data/fixtures/events'/f"{p['id']}.jsonl"
        if not ev.exists():
            print(f'missing fixture: {ev}'); continue
        for cp in p['checkpoints']:
            total+=1; r=validate_checkpoint(cp,ev)
            if r['proof_state']=='VALIDATOR_PASS_FIXTURE_ONLY': fixture_pass+=1
            else: print(json.dumps(r,indent=2))
    live_proven=0
    print(f'graph=ACYCLIC checkpoints={total} fixture_validator_passes={fixture_pass} live_proven={live_proven}')
    return 0 if total==fixture_pass else 1

def dump(x): print(json.dumps(x,indent=2))
def cmd_project(args): dump(project(args.id))
def cmd_next(args): dump(ready(project(args.id),args.proven or [])[:5])
def cmd_poll(args):
    from runtime.poll_github import poll_all
    dump(poll_all())
def cmd_underengineer(args): dump(plan(args.id) if args.id else ranked())
def cmd_assets(args): dump({'declared':declared_assets(),'ledger':ledger()})
def cmd_substitution(args): dump(substitution_summary())
def cmd_feature(args): dump(feature_allowed(args.id,args.reason))
def cmd_order(args): dump(order(args.id))

def main():
    ap=argparse.ArgumentParser(description='Scarce State Control Plane v2'); sub=ap.add_subparsers(dest='cmd',required=True)
    s=sub.add_parser('check'); s.set_defaults(fn=cmd_check)
    s=sub.add_parser('project'); s.add_argument('id'); s.set_defaults(fn=cmd_project)
    s=sub.add_parser('next'); s.add_argument('id'); s.add_argument('--proven',action='append'); s.set_defaults(fn=cmd_next)
    s=sub.add_parser('underengineer'); s.add_argument('id',nargs='?'); s.set_defaults(fn=cmd_underengineer)
    s=sub.add_parser('assets'); s.set_defaults(fn=cmd_assets)
    s=sub.add_parser('substitution'); s.set_defaults(fn=cmd_substitution)
    s=sub.add_parser('feature'); s.add_argument('id'); s.add_argument('reason'); s.set_defaults(fn=cmd_feature)
    s=sub.add_parser('order'); s.add_argument('id',nargs='?'); s.set_defaults(fn=cmd_order)
    s=sub.add_parser('poll-github'); s.set_defaults(fn=cmd_poll)
    a=ap.parse_args(); raise SystemExit(a.fn(a) or 0)
if __name__=='__main__': main()
