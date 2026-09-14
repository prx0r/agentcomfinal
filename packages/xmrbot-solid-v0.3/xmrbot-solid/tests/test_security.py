from xmrbot.agent.plans import wallet_plan
from xmrbot.agent.tools import ToolRegistry
from xmrbot.services import Services


def test_wallet_plan_never_exports_secrets():
    p=wallet_plan()
    assert p["cloud_receives_seed"] is False
    assert "export_seed" in p["disabled_actions"]


def test_mcp_surface_has_no_seed_or_key_export():
    names=[x.name for x in ToolRegistry(Services(":memory:")).metadata()]
    joined=" ".join(names).lower()
    assert "export_seed" not in joined
    assert "private_key" not in joined
    assert "send" not in names


def test_local_daemon_rejects_non_loopback_bind():
    import pytest
    import typer
    from xmrbot.local.daemon import serve
    with pytest.raises(typer.BadParameter):
        serve(host="0.0.0.0", port=47831)
