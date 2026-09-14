import json
from pathlib import Path
from seesaw.engine import score_portfolio, get_project, score_features, event_impact

ROOT=Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT/name).read_text())

def test_portfolio_scores():
    p=load("data/projects.json")
    rows=score_portfolio(p)
    assert rows
    assert all(0 <= r["strategic_value"] <= 100 for r in rows)

def test_feature_actions():
    p=load("data/projects.json")
    cmail=get_project(p,"cmail")
    rows=score_features(cmail)
    actions={r["name"]:r["action"] for r in rows}
    assert actions["generic email drafting"] in {"REUSE","DROP","WATCH"}
    assert actions["verified domain/email identity"]=="OWN"

def test_event():
    p=load("data/projects.json")
    e=load("examples/plugin_compiler_free.json")
    rows=event_impact(p,e)
    assert len(rows)==len(p["projects"])
