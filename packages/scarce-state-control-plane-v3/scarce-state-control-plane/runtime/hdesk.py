from __future__ import annotations
from datetime import datetime, timezone
import json, uuid
from .model import ROOT, load_json
PATH=ROOT/'data/human_tasks.json'

def state(): return load_json(PATH)
def templates(): return load_json(ROOT/'data/human_task_templates.json')

def _save(x): PATH.write_text(json.dumps(x,indent=2)+'\n')

def priority(t):
    mins=max(1.0,float(t.get('estimated_minutes',5)))
    return round(float(t.get('blocking_value',1))/mins,4)

def queue():
    s=state(); rows=[]
    for t in s['tasks']:
        if t.get('status')=='OPEN': rows.append({**t,'attention_value_per_minute':priority(t)})
    rows.sort(key=lambda x:(-x['attention_value_per_minute'],x.get('created_at','')))
    return {'rule':'Human attention is reserved for strategic direction, inaccessible physical/platform action, identity/KYC, bounded spend authority and relationship/taste judgement. Debugging stays with agents.','open':rows,'count':len(rows)}

def add(kind,question,project_id=None,options=None,recommendation=None,why_human='',blocking_value=1,estimated_minutes=5):
    allowed={x['id'] for x in templates()['allowed_kinds']}
    if kind not in allowed: raise ValueError('invalid H-task kind')
    s=state(); tid='H-'+uuid.uuid4().hex[:10]
    task={'id':tid,'kind':kind,'project_id':project_id,'question':question,'options':options or [],'recommendation':recommendation,'why_human':why_human,
          'blocking_value':float(blocking_value),'estimated_minutes':float(estimated_minutes),'status':'OPEN','created_at':datetime.now(timezone.utc).isoformat()}
    s['tasks'].append(task); _save(s); return task

def answer(task_id,decision,note=''):
    s=state(); found=None
    for t in s['tasks']:
        if t['id']==task_id:
            if t['status']!='OPEN': raise ValueError('task not open')
            if t.get('options') and decision not in t['options']: raise ValueError('decision must be one of task options')
            t['status']='ANSWERED'; found=t; break
    if not found: raise KeyError(task_id)
    ans={'task_id':task_id,'decision':decision,'note':note,'answered_at':datetime.now(timezone.utc).isoformat()}
    s['answers'].append(ans); _save(s); return ans
