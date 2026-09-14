from __future__ import annotations
from .model import projects, load_json, ROOT

def asset_score(a):
    # Multiplication only for core exclusivity/externality; amplifiers are additive so absence of network effects does not zero a useful asset.
    core=float(a.get('exclusivity',1))*float(a.get('externality',1))
    amp=(float(a.get('feedback',1))+float(a.get('network_effects',1))+float(a.get('trust',1))+float(a.get('ai_moat_beta',1)))/4.0
    discount=(float(a.get('public_replicability',1))+float(a.get('platform_capture',1))+float(a.get('synthetic_substitutability',1)))/15.0
    return round(core*amp*max(0.1,1-discount),3)

def declared_assets():
    out=[]
    for p in projects():
        for a in p.get('scarce_assets',[]):
            x=dict(a); x['project_id']=p['id']; x['project_name']=p['name']; x['strategic_score']=asset_score(a); out.append(x)
    return sorted(out,key=lambda x:(-x['strategic_score'],x['project_name'],x['id']))

def ledger():
    return load_json(ROOT/'data/scarce_asset_ledger.json')

def substitution_summary():
    return [{'project_id':p['id'],'name':p['name'],'role':p['strategic_role'],**p['software_substitution_test']} for p in projects()]
