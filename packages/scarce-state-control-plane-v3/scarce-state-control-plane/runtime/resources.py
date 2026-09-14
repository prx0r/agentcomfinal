from __future__ import annotations
from .model import ROOT, load_json

def resources(): return load_json(ROOT/'data/resource_constraints.json')
def resource_map(): return {r['id']:r for r in resources()['resources']}

def explain_requirements(world):
    rm=resource_map(); return [rm[r] for r in world.get('resources',[]) if r in rm]
