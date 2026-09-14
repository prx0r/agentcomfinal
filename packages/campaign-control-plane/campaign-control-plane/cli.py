
#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from runtime.model import projects,project,ROOT
from runtime.validators import validate_checkpoint
from runtime.graph import assert_acyclic,ready

def cmd_check(args):
    assert_acyclic(); total=0; fixture_pass=0
    for p in projects():
        ev=ROOT/'data/fixtures/events'/f"{p['id']}.jsonl"
        for cp in p['checkpoints']:
            total+=1; r=validate_checkpoint(cp,ev)
            if r['proof_state']=='VALIDATOR_PASS_FIXTURE_ONLY': fixture_pass+=1
            else: print(json.dumps(r,indent=2))
    print(f'graph=ACYCLIC checkpoints={total} fixture_validator_passes={fixture_pass} live_proven=0')
    return 0 if total==fixture_pass else 1

def cmd_project(args): print(json.dumps(project(args.id),indent=2))
def cmd_next(args):
    p=project(args.id); proven=args.proven or []
    print(json.dumps(ready(p,proven)[:5],indent=2))
def cmd_poll(args):
    from runtime.poll_github import poll_all
    print(json.dumps(poll_all(),indent=2))

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    s=sub.add_parser('check'); s.set_defaults(fn=cmd_check)
    s=sub.add_parser('project'); s.add_argument('id'); s.set_defaults(fn=cmd_project)
    s=sub.add_parser('next'); s.add_argument('id'); s.add_argument('--proven',action='append'); s.set_defaults(fn=cmd_next)
    s=sub.add_parser('poll-github'); s.set_defaults(fn=cmd_poll)
    a=ap.parse_args(); raise SystemExit(a.fn(a) or 0)
if __name__=='__main__': main()
