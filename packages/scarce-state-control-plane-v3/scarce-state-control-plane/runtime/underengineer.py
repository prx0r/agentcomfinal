from __future__ import annotations
from .model import projects, project, load_json, ROOT

def _priority_value(p):
    x=p.get('priority_inputs',{})
    importance=float(x.get('importance',1)); asset=float(x.get('asset_value',1)); beta=float(x.get('moat_beta',1))
    effort=max(1.0,float(x.get('effort',1))); human=max(1.0,float(x.get('human_burden',1)))
    return round((importance*asset*beta)/(effort*(0.5+0.5*human)),3)

def plan(pid):
    p=project(pid); u=p['underengineer']
    state=load_json(ROOT/'data/underengineer_state.json')['projects'].get(pid,{'completed_steps':[]})
    done=set(state.get('completed_steps',[])); next_step=next((s for s in u['steps'] if s['id'] not in done),None)
    return {'project_id':pid,'name':p['name'],'strategic_role':p['strategic_role'],'priority_score':_priority_value(p),
      'software_survival':p['software_substitution_test']['survival'],'scarce_state_target':u['scarce_state_target'],
      'first_real_moat_event':u['first_real_moat_event'],'minimal_live_product':u['minimal_live_product'],'next_step':next_step,
      'completed_steps':sorted(done),'not_now':u['explicitly_not_now'],'graduation_rule':u['graduation_rule'],'kill_or_rethink_rule':u['kill_or_rethink_rule'],
      'observation_pause':u['observation_pause'],'required_components_now':u.get('required_components_now',[]),
      'target_profile':p.get('experiment_strategy',{}).get('target_profile'),'learning_goal':p.get('experiment_strategy',{}).get('learning_goal')}

def ranked():
    ps=[plan(p['id']) for p in projects()]
    def grp(role): return sorted([x for x in ps if x['strategic_role']==role],key=lambda x:(-x['priority_score'],x['name']))
    return {'rule':'Rank scarce-asset campaigns first. Pull hybrid/infrastructure only when required by a selected experiment minimum path.',
      'asset_campaigns':grp('asset_campaign'),'hybrid_infrastructure':grp('hybrid_infrastructure'),'infrastructure':grp('infrastructure')}

def feature_allowed(pid, reason:str):
    allowed={'required_for_first_moat_event','safety','verification','empirical_unblocker'}
    return {'project_id':pid,'reason':reason,'decision':'NOW' if reason in allowed else 'NOT_NOW','allowed_reasons':sorted(allowed)}

def order(pid=None):
    if pid is None:
        rs=ranked()['asset_campaigns'];
        if not rs: return None
        pid=rs[0]['project_id']
    x=plan(pid)
    from .experiments import select_world
    wx=select_world(pid)
    live=next((w for w in wx['ranked_worlds'] if w['id']!='internal_simulation'),None)
    return {'primitive':'UNDERENGINEER/2.0','project_id':pid,
      'selected_because':'Highest current heuristic scarce-state progress / resource score' if ranked()['asset_campaigns'] and pid==ranked()['asset_campaigns'][0]['project_id'] else 'Explicit project selection',
      'goal':x['scarce_state_target'],'first_real_moat_event':x['first_real_moat_event'],'next_step':x['next_step'],
      'target_profile':x['target_profile'],'recommended_external_world':live,'simulation_preflight':bool(wx['ranked_worlds']),
      'required_components_now':x['required_components_now'],'forbidden_scope_expansion':x['not_now'],
      'dispatch_contract':{
        'worker_may':'search, reuse, code, simulate, test and propose implementations inside the selected step; prepare the selected external experiment',
        'worker_may_not':'claim success from code/simulation, expand NOT_NOW scope, self-attest live proof, invent account capacity, or obtain consequential authority outside QP',
        'completion':'step acceptance plus independently attested evidence; real demand/economic/moat claims require the matching external experiment world',
        'after_first_moat_event':'STOP feature expansion, normalize the outcome, update strategy evidence, and return observations before choosing the next feature'
      }}
