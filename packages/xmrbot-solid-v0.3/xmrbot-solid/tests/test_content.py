from xmrbot.content.events import detect_events
from xmrbot.content.workflows import workflow_for_event
from xmrbot.core.types import NetworkSnapshot


def snap(diff, price=500):
    return NetworkSnapshot(height=1,difficulty=diff,estimated_hashrate_hs=diff/120,reward_xmr=.6,xmr_usd=price)


def test_difficulty_event_and_workflow():
    events=detect_events(snap(600e9),snap(720e9))
    assert any(e["event"]=="difficulty_move" for e in events)
    wf=workflow_for_event(events[0])
    assert "youtube" in wf and "shorts" in wf and "target_url" in wf
