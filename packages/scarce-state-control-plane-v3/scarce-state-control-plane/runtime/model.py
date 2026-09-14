from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def load_json(path): return json.loads(Path(path).read_text())
def portfolio(): return load_json(ROOT/'data/portfolio.json')
def projects(): return [load_json(p) for p in sorted((ROOT/'data/projects').glob('*.json'))]
def project(pid):
    p=ROOT/'data/projects'/f'{pid}.json'
    if not p.exists(): raise KeyError(pid)
    return load_json(p)
def bottlenecks(): return load_json(ROOT/'data/meta_bottlenecks.json')
def components(): return portfolio().get('shared_components',load_json(ROOT/'data/shared_components.json'))
