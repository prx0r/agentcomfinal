#!/usr/bin/env python3
import argparse,json
from runtime.model import projects,project,ROOT
from runtime.validators import validate_checkpoint
from runtime.graph import assert_acyclic,ready
from runtime.underengineer import plan,ranked,feature_allowed,order
from runtime.scarcity import declared_assets,ledger,substitution_summary

def dump(x): print(json.dumps(x,indent=2))
def cmd_check(args):
    assert_acyclic(); total=0; fixture_pass=0
    for p in projects():
        ev=ROOT/'data/fixtures/events'/f"{p['id']}.jsonl"
        if not ev.exists(): print(f'missing fixture: {ev}'); continue
        for cp in p['checkpoints']:
            total+=1; r=validate_checkpoint(cp,ev)
            if r['proof_state']=='VALIDATOR_PASS_FIXTURE_ONLY': fixture_pass+=1
            else: print(json.dumps(r,indent=2))
    print(f'graph=ACYCLIC checkpoints={total} fixture_validator_passes={fixture_pass} live_proven=0')
    return 0 if total==fixture_pass else 1
def cmd_project(a): dump(project(a.id))
def cmd_next(a): dump(ready(project(a.id),a.proven or [])[:5])
def cmd_poll(a):
    from runtime.poll_github import poll_all; dump(poll_all())
def cmd_underengineer(a): dump(plan(a.id) if a.id else ranked())
def cmd_assets(a): dump({'declared':declared_assets(),'ledger':ledger()})
def cmd_substitution(a): dump(substitution_summary())
def cmd_feature(a): dump(feature_allowed(a.id,a.reason))
def cmd_order(a): dump(order(a.id))
def cmd_worlds(a):
    from runtime.experiments import catalog,select_world; dump(select_world(a.id) if a.id else catalog())
def cmd_profiles(a):
    from runtime.experiments import target_profiles; dump(target_profiles())
def cmd_schedule(a):
    from runtime.scheduler import schedule; dump(schedule())
def cmd_resources(a):
    from runtime.resources import resources; dump(resources())
def cmd_simulate(a):
    from runtime.simulation import simulate_project; dump(simulate_project(a.id))
def cmd_hdesk(a):
    from runtime.hdesk import queue; dump(queue())
def cmd_hadd(a):
    from runtime.hdesk import add; dump(add(a.kind,a.question,a.project,a.option,a.recommendation,a.why_human,a.blocking_value,a.minutes))
def cmd_hanswer(a):
    from runtime.hdesk import answer; dump(answer(a.task_id,a.decision,a.note))
def cmd_perf(a):
    from runtime.performance import strategy_performance,replication_candidates; dump({'families':strategy_performance(),'replication_candidates':replication_candidates()})
def cmd_record(a):
    from runtime.performance import record; dump(record(a.project,a.world,a.evidence_source,a.result,a.strategy_family,a.metric,a.cost,a.human_minutes,a.receipt_ref,a.hypothesis))
def cmd_selflab(a):
    from runtime.selflab import breadup_self_lab; dump(breadup_self_lab())

def main():
    ap=argparse.ArgumentParser(description='Autonomous Economic Discovery Control Plane v3'); sub=ap.add_subparsers(dest='cmd',required=True)
    for name,fn in [('check',cmd_check),('assets',cmd_assets),('substitution',cmd_substitution),('poll-github',cmd_poll),('schedule',cmd_schedule),('resources',cmd_resources),('hdesk',cmd_hdesk),('performance',cmd_perf),('selflab',cmd_selflab),('profiles',cmd_profiles)]:
        s=sub.add_parser(name); s.set_defaults(fn=fn)
    s=sub.add_parser('project'); s.add_argument('id'); s.set_defaults(fn=cmd_project)
    s=sub.add_parser('next'); s.add_argument('id'); s.add_argument('--proven',action='append'); s.set_defaults(fn=cmd_next)
    s=sub.add_parser('underengineer'); s.add_argument('id',nargs='?'); s.set_defaults(fn=cmd_underengineer)
    s=sub.add_parser('feature'); s.add_argument('id'); s.add_argument('reason'); s.set_defaults(fn=cmd_feature)
    s=sub.add_parser('order'); s.add_argument('id',nargs='?'); s.set_defaults(fn=cmd_order)
    s=sub.add_parser('worlds'); s.add_argument('id',nargs='?'); s.set_defaults(fn=cmd_worlds)
    s=sub.add_parser('simulate'); s.add_argument('id'); s.set_defaults(fn=cmd_simulate)
    s=sub.add_parser('htask-add'); s.add_argument('kind'); s.add_argument('question'); s.add_argument('--project'); s.add_argument('--option',action='append'); s.add_argument('--recommendation'); s.add_argument('--why-human',default=''); s.add_argument('--blocking-value',type=float,default=1); s.add_argument('--minutes',type=float,default=5); s.set_defaults(fn=cmd_hadd)
    s=sub.add_parser('htask-answer'); s.add_argument('task_id'); s.add_argument('decision'); s.add_argument('--note',default=''); s.set_defaults(fn=cmd_hanswer)
    s=sub.add_parser('experiment-record'); s.add_argument('project'); s.add_argument('world'); s.add_argument('evidence_source'); s.add_argument('result'); s.add_argument('--strategy-family'); s.add_argument('--metric',type=float); s.add_argument('--cost',type=float); s.add_argument('--human-minutes',type=float); s.add_argument('--receipt-ref'); s.add_argument('--hypothesis',default=''); s.set_defaults(fn=cmd_record)
    a=ap.parse_args(); raise SystemExit(a.fn(a) or 0)
if __name__=='__main__': main()
