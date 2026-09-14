from __future__ import annotations
from .model import projects, project, load_json, ROOT

def _priority_value(p):
    x=p.get('priority_inputs',{})
    importance=float(x.get('importance',1)); asset=float(x.get('asset_value',1)); beta=float(x.get('moat_beta',1))
    effort=max(1.0,float(x.get('effort',1))); human=max(1.0,float(x.get('human_burden',1)))
    # Coarse heuristic only: ranking proposal, never canonical truth.
    return round((importance*asset*beta)/(effort*(0.5+0.5*human)),3)

def plan(pid):
    p=project(pid); u=p['underengineer']
    state=load_json(ROOT/'data/underengineer_state.json')['projects'].get(pid,{'completed_steps':[]})
    done=set(state.get('completed_steps',[]))
    next_step=next((s for s in u['steps'] if s['id'] not in done),None)
    return {
      'project_id':pid,'name':p['name'],'strategic_role':p['strategic_role'],
      'priority_score':_priority_value(p),
      'software_survival':p['software_substitution_test']['survival'],
      'scarce_state_target':u['scarce_state_target'],
      'first_real_moat_event':u['first_real_moat_event'],
      'minimal_live_product':u['minimal_live_product'],
      'next_step':next_step,'completed_steps':sorted(done),
      'not_now':u['explicitly_not_now'],'graduation_rule':u['graduation_rule'],
      'kill_or_rethink_rule':u['kill_or_rethink_rule'],
      'observation_pause':u['observation_pause'],
      'required_components_now':u.get('required_components_now',[])
    }

def ranked():
    ps=[plan(p['id']) for p in projects()]
    assets=[x for x in ps if x['strategic_role']=='asset_campaign']
    hybrids=[x for x in ps if x['strategic_role']=='hybrid_infrastructure']
    infra=[x for x in ps if x['strategic_role']=='infrastructure']
    assets.sort(key=lambda x:(-x['priority_score'],x['name']))
    hybrids.sort(key=lambda x:(-x['priority_score'],x['name']))
    infra.sort(key=lambda x:(-x['priority_score'],x['name']))
    return {
      'rule':'Rank scarce-asset campaigns first. Pull hybrid/infrastructure only when required by the selected campaign minimum path.',
      'asset_campaigns':assets,'hybrid_infrastructure':hybrids,'infrastructure':infra
    }

def feature_allowed(pid, reason:str):
    """Deterministic triage primitive for proposed features.
    Allowed reasons are deliberately narrow; everything else defaults NOT_NOW.
    """
    allowed={'required_for_first_moat_event','safety','verification','empirical_unblocker'}
    return {'project_id':pid,'reason':reason,'decision':'NOW' if reason in allowed else 'NOT_NOW','allowed_reasons':sorted(allowed)}


def order(pid=None):
    """One concise dispatch packet for the project manager/agent controller."""
    if pid is None:
        rs=ranked()['asset_campaigns']
        if not rs: return None
        pid=rs[0]['project_id']
    x=plan(pid)
    return {
      'primitive':'UNDERENGINEER/1.0',
      'project_id':pid,
      'selected_because':'Highest current heuristic scarce-state progress / resource score' if pid==ranked()['asset_campaigns'][0]['project_id'] else 'Explicit project selection',
      'goal':x['scarce_state_target'],
      'first_real_moat_event':x['first_real_moat_event'],
      'next_step':x['next_step'],
      'required_components_now':x['required_components_now'],
      'forbidden_scope_expansion':x['not_now'],
      'dispatch_contract':{
        'worker_may':'search, reuse, code, test and propose any implementation inside the selected step',
        'worker_may_not':'claim success from code presence, expand NOT_NOW scope, self-attest live proof, or obtain consequential authority outside QP',
        'completion':'step acceptance plus independently attested evidence; first moat event must later increment a declared scarce asset through a verified receipt',
        'after_first_moat_event':'STOP feature expansion and return observations to thesis/UNDERENGINEER before selecting the next feature'
      }
    }
