from __future__ import annotations
from datetime import datetime, timezone
import json, uuid
from .model import ROOT, load_json

REAL={'external','economic','scarce_state'}
VALID_SOURCES=REAL|{'simulation','fixture','replay'}
VALID_RESULTS={'SUCCESS','FAIL','INCONCLUSIVE','OPEN'}
PATH=ROOT/'data/experiment_runs.jsonl'

def runs():
    out=[]
    if not PATH.exists(): return out
    for line in PATH.read_text().splitlines():
        if line.strip(): out.append(json.loads(line))
    return out

def family_for_project(project_id):
    for f in load_json(ROOT/'data/strategy_families.json')['families']:
        if project_id in f.get('projects',[]): return f['id']
    return None

def record(project_id,world,evidence_source,result,strategy_family=None,metric=None,cost=None,human_minutes=None,receipt_ref=None,hypothesis='',experiment_id=None):
    if evidence_source not in VALID_SOURCES: raise ValueError('invalid evidence_source')
    if result not in VALID_RESULTS: raise ValueError('invalid result')
    if evidence_source in REAL and result in {'SUCCESS','FAIL'} and not receipt_ref: raise ValueError('real resolved outcomes require receipt_ref')
    row={'experiment_id':experiment_id or 'E-'+uuid.uuid4().hex[:12],'project_id':project_id,'strategy_family':strategy_family or family_for_project(project_id),
         'world':world,'hypothesis':hypothesis,'frozen_at':datetime.now(timezone.utc).isoformat(),'evidence_source':evidence_source,'result':result,
         'metric':metric,'cost':cost,'human_minutes':human_minutes,'receipt_ref':receipt_ref}
    with PATH.open('a') as fh: fh.write(json.dumps(row,sort_keys=True)+'\n')
    return row

def strategy_performance():
    cfg=load_json(ROOT/'data/strategy_families.json'); rs=runs(); out=[]
    for fam in cfg['families']:
        valid=[r for r in rs if r.get('strategy_family')==fam['id'] and r.get('evidence_source') in REAL and r.get('result') in {'SUCCESS','FAIL'}]
        wins=sum(1 for r in valid if r['result']=='SUCCESS'); losses=len(valid)-wins
        a=fam.get('prior_alpha',1)+wins; b=fam.get('prior_beta',1)+losses; mean=a/(a+b)
        if len(valid)<3: state='INSUFFICIENT_REAL_OUTCOMES'
        elif mean>=0.67: state='PROMOTE_CANDIDATE'
        elif mean<=0.33: state='KILL_OR_RETHINK'
        else: state='MIXED'
        out.append({**fam,'real_attempts':len(valid),'real_successes':wins,'real_failures':losses,'posterior_mean':round(mean,4),
                    'simulation_attempts':sum(1 for r in rs if r.get('strategy_family')==fam['id'] and r.get('evidence_source')=='simulation'),
                    'promotion_state':state,'scheduler_multiplier':round(1.0 if len(valid)<3 else 0.5+mean,4)})
    return out

def replication_candidates():
    return [x for x in strategy_performance() if x['promotion_state']=='PROMOTE_CANDIDATE']
