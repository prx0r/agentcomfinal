from __future__ import annotations
from .model import ROOT, load_json, project


def catalog():
    return load_json(ROOT/'data/experiment_worlds.json')


def target_profiles():
    return load_json(ROOT/'data/target_profiles.json')


def world(world_id):
    for w in catalog()['worlds']:
        if w['id']==world_id:
            return w
    raise KeyError(world_id)


def experiment_value(w):
    """Coarse deterministic ranking heuristic, never canonical truth."""
    numerator=float(w['information_gain'])*float(w['feedback_quality'])*float(w['economic_relevance'])
    money=1.0+max(0.0,float(w.get('money_cost',0)))/10.0
    time=1.0+max(0.0,float(w.get('feedback_hours',0)))/24.0
    human=1.0+max(0.0,float(w.get('human_minutes',0)))/30.0
    irreversible=max(1.0,float(w.get('irreversibility',1)))
    return round(numerator/(money*time*human*irreversible),4)


def select_world(pid, include_simulation=True):
    p=project(pid); strategy=p.get('experiment_strategy',{})
    rows=[]
    for wid in strategy.get('candidates',[]):
        if wid=='internal_simulation' and not include_simulation: continue
        w=world(wid).copy(); w['score']=experiment_value(w); rows.append(w)
    rows.sort(key=lambda x:(-x['score'],x['id']))
    return {'project_id':pid,'target_profile':strategy.get('target_profile'),'learning_goal':strategy.get('learning_goal'),'ranked_worlds':rows,'selected':rows[0] if rows else None,
            'warning':'Selection score is a planning heuristic. Simulation can rank an external experiment but cannot graduate a market claim.'}


def live_worlds(pid):
    x=select_world(pid)
    return [w for w in x['ranked_worlds'] if w['id']!='internal_simulation']
