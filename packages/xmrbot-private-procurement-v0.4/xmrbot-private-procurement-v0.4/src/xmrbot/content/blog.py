from __future__ import annotations
from datetime import datetime, timezone
import json
import re
from typing import Literal
from pydantic import BaseModel, Field, field_validator

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = _SLUG_RE.sub("-", value).strip("-")
    return value[:96] or "post"


class BlogPostInput(BaseModel):
    title: str = Field(min_length=3, max_length=180)
    body_md: str = Field(min_length=1, max_length=200_000)
    slug: str | None = Field(default=None, max_length=96)
    dek: str = Field(default="", max_length=320)
    author: str = Field(default="XMRBot", max_length=80)
    tags: list[str] = Field(default_factory=list, max_length=24)
    source_refs: list[dict] = Field(default_factory=list, max_length=100)

    @field_validator("slug")
    @classmethod
    def normalize_slug(cls, value):
        return slugify(value) if value else value

    @field_validator("tags")
    @classmethod
    def normalize_tags(cls, value):
        out=[]
        for tag in value:
            t=tag.strip().lower()[:40]
            if t and t not in out:
                out.append(t)
        return out


class BlogPost(BlogPostInput):
    slug: str
    status: Literal["draft", "published"]
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None = None
    content_version: int = 1


def row_to_blog(row) -> BlogPost:
    return BlogPost(
        slug=row["slug"], title=row["title"], dek=row["dek"], body_md=row["body_md"],
        author=row["author"], status=row["status"], tags=json.loads(row["tags_json"]),
        source_refs=json.loads(row["source_refs_json"]), created_at=row["created_at"],
        updated_at=row["updated_at"], published_at=row["published_at"],
        content_version=row["content_version"],
    )


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
