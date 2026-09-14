from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from xmrbot.content.blog import BlogPost


@dataclass(frozen=True)
class Recipe:
    id: str
    title: str
    description: str
    steps: tuple[str, ...]
    outputs: tuple[str, ...]


RECIPES: dict[str, Recipe] = {
    "blog-to-video": Recipe(
        id="blog-to-video",
        title="Blog → YouTube package",
        description="Turn a published XMRBot article into a source-grounded video package without changing the underlying facts.",
        steps=(
            "Load the canonical published blog post and its source_refs.",
            "Resolve any live XMR metrics referenced by the post immediately before production.",
            "Generate a 6–10 minute video outline with hook, thesis, evidence, demo and CTA.",
            "Generate title, description, chapters, thumbnail brief and 3 short-form cutdowns.",
            "Human/editor validates claims and approves the final render.",
            "Upload through a configured YouTube publisher adapter; otherwise emit an upload-ready manifest.",
        ),
        outputs=("youtube_manifest", "video_script", "thumbnail_brief", "shorts", "x_post", "instagram_caption"),
    ),
    "network-event-to-post": Recipe(
        id="network-event-to-post",
        title="Network event → blog + social",
        description="Convert a material network/hashprice/difficulty event into a methodology-linked article and distribution package.",
        steps=(
            "Load the event and exact historical observations.",
            "Compute deltas with methodology IDs.",
            "Draft a concise article that links the terminal and raw API.",
            "Save as draft; editor or trusted internal agent publishes.",
            "Run blog-to-video if the event is sufficiently important.",
        ),
        outputs=("blog_draft", "x_post", "shorts"),
    ),
}


def list_recipes() -> list[dict[str, Any]]:
    return [recipe.__dict__ for recipe in RECIPES.values()]


def get_recipe(recipe_id: str) -> dict[str, Any] | None:
    recipe = RECIPES.get(recipe_id)
    return recipe.__dict__ if recipe else None


def package_from_blog(post: BlogPost, canonical_url: str) -> dict[str, Any]:
    url = f"{canonical_url}/blog/{post.slug}"
    body = post.body_md.strip()
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    key_points = []
    for p in paragraphs:
        clean = p.lstrip("#- ").strip()
        if clean and len(clean) > 24:
            key_points.append(clean[:280])
        if len(key_points) >= 6:
            break
    if not key_points:
        key_points = [post.dek or post.title]
    return {
        "recipe": "blog-to-video",
        "source_post": post.model_dump(mode="json"),
        "canonical_url": url,
        "youtube_manifest": {
            "title": post.title[:100],
            "description": f"{post.dek}\n\nRead the source-linked article and live data: {url}".strip(),
            "privacy_status": "private-until-editor-approval",
            "tags": ["Monero", "XMR", *post.tags][:20],
            "requires_oauth_upload_adapter": True,
        },
        "video_script": {
            "hook": post.dek or post.title,
            "sections": [
                {"name": "The question", "beats": [post.title]},
                {"name": "What the data says", "beats": key_points[:3]},
                {"name": "What it means", "beats": key_points[3:] or key_points[:2]},
                {"name": "Verify it yourself", "beats": [f"Open {url} and the linked XMRBot methodology/data endpoints."]},
            ],
            "cta": f"Run the live numbers at {canonical_url}",
        },
        "thumbnail_brief": {
            "style": "XMRBot legacy/technical: charcoal, warm white, Monero orange; one number or question; no neon gradients.",
            "headline": post.title[:52],
        },
        "shorts": [
            {"hook": post.title, "angle": "single strongest claim", "cta": url},
            {"hook": "One Monero chart explains this", "angle": "show the primary metric", "cta": url},
            {"hook": "Verify this yourself", "angle": "show API/methodology and live tool", "cta": url},
        ],
        "x_post": f"{post.title}\n\n{post.dek}\n\n{url}".strip(),
        "instagram_caption": f"{post.title}\n\n{post.dek}\n\nLive numbers + sources at xmrbot.com/blog/{post.slug}".strip(),
        "sources": post.source_refs,
    }
