# XMRBot content automation

The publication system treats the blog post plus its `source_refs` as the canonical research object. Social/video outputs are derivatives.

## Trusted internal-agent workflow

Use local stdio MCP where possible:

1. `xmr_blog_draft` — upsert a draft with title, Markdown, tags and source references.
2. Review the returned draft and its source references.
3. `xmr_blog_publish` — publish the exact slug.
4. `xmr_content_from_blog` — emit the source-preserving production package.
5. Render the video/shorts using your media pipeline.
6. Human/editor approves the rendered media.
7. A credentialed YouTube publisher adapter uploads the final video.

HTTP content writes are disabled unless `XMRBOT_EDITOR_TOKEN` is configured. State-changing MCP calls over HTTP require the same bearer token. This prevents a public MCP endpoint from becoming an unauthenticated CMS.

## Why upload is a separate adapter

YouTube publication requires OAuth credentials and channel authorization. The core repository outputs a deterministic upload manifest but does not fake a successful upload. Implement `xmrbot.content.publishers.YouTubePublisher` in a deployment-specific package or service and give that service only the minimum required credentials.

## Machine-readable publication surfaces

- `/v1/blog`
- `/v1/blog/{slug}`
- `/v1/blog/{slug}/raw`
- `/blog/feed.xml`
- `/v1/content/recipes`
- `/v1/content/from-blog/{slug}`
- MCP tools: `xmr_blog_*`, `xmr_content_*`
- MCP resources: `xmrbot://blog`, `xmrbot://recipes`
