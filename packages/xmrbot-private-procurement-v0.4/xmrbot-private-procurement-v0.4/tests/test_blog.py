import pytest
from xmrbot.agent.tools import ToolRegistry
from xmrbot.mcp.server import MCPServer
from xmrbot.services import Services


@pytest.mark.asyncio
async def test_blog_lifecycle_through_local_mcp():
    services = Services(":memory:")
    server = MCPServer(ToolRegistry(services))
    draft = await server.handle({
        "jsonrpc":"2.0","id":1,"method":"tools/call",
        "params":{"name":"xmr_blog_draft","arguments":{
            "title":"Why hashprice matters",
            "dek":"A deterministic mining metric.",
            "body_md":"## Definition\n\nHashprice prices one unit of RandomX hashrate.",
            "tags":["mining","hashprice"],
            "source_refs":[{"name":"XMRBot methodology","url":"https://xmrbot.com/v1/methodologies"}]
        }}
    })
    post = draft["result"]["structuredContent"]
    assert post["status"] == "draft"
    assert post["slug"] == "why-hashprice-matters"
    assert services.repo.list_blog(10, False) == []

    published = await server.handle({
        "jsonrpc":"2.0","id":2,"method":"tools/call",
        "params":{"name":"xmr_blog_publish","arguments":{"slug":post["slug"]}}
    })
    pub = published["result"]["structuredContent"]
    assert pub["status"] == "published"
    assert pub["published_at"]
    assert services.repo.get_blog(post["slug"]).title == "Why hashprice matters"

    package = await server.handle({
        "jsonrpc":"2.0","id":3,"method":"tools/call",
        "params":{"name":"xmr_content_from_blog","arguments":{"slug":post["slug"]}}
    })
    out = package["result"]["structuredContent"]
    assert out["recipe"] == "blog-to-video"
    assert out["youtube_manifest"]["requires_oauth_upload_adapter"] is True
    assert out["sources"][0]["name"] == "XMRBot methodology"


def test_blog_upsert_increments_version():
    services = Services(":memory:")
    from xmrbot.content.blog import BlogPostInput
    a = services.repo.upsert_blog_draft(BlogPostInput(title="Versioned post", body_md="one"))
    b = services.repo.upsert_blog_draft(BlogPostInput(title="Versioned post", body_md="two", slug=a.slug))
    assert b.content_version == 2
    assert b.body_md == "two"
