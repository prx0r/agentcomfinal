from fastapi.testclient import TestClient
from xmrbot.app import app

client = TestClient(app)


def test_llms_robots_sitemap_and_machine_map():
    llms = client.get('/llms.txt')
    assert llms.status_code == 200
    assert 'xmr_tools' in llms.text and '/v1/site/map' in llms.text
    robots = client.get('/robots.txt')
    assert robots.status_code == 200 and 'Sitemap:' in robots.text
    sitemap = client.get('/sitemap.xml')
    assert sitemap.status_code == 200 and '/terminal' in sitemap.text and '/blog' in sitemap.text
    site = client.get('/v1/site/map')
    assert site.status_code == 200
    paths = {x.get('path') for x in site.json()['human_surfaces']}
    assert {'/terminal','/blog','/recipes'} <= paths


def test_http_blog_writes_disabled_without_editor_token():
    r = client.post('/v1/blog/draft', json={'title':'No public write','body_md':'test'})
    assert r.status_code == 503


def test_http_mcp_state_change_disabled_without_editor_token():
    r = client.post('/mcp', json={
        'jsonrpc':'2.0','id':1,'method':'tools/call',
        'params':{'name':'xmr_blog_draft','arguments':{'title':'No public MCP write','body_md':'test'}}
    })
    assert r.status_code == 503
