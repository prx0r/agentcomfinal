from __future__ import annotations
from datetime import datetime, timezone
import json
import sqlite3
from xmrbot.core.types import NetworkSnapshot
from xmrbot.content.blog import BlogPost, BlogPostInput, now_iso, row_to_blog, slugify


class Repository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add_network(self, snap: NetworkSnapshot) -> None:
        self.conn.execute(
            """INSERT INTO network_observations
            (timestamp,height,difficulty,target_seconds,estimated_hashrate_hs,reward_xmr,xmr_usd,mempool_transactions,fee_per_byte_atomic,source,confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (snap.timestamp.isoformat(), snap.height, snap.difficulty, snap.target_seconds,
             snap.estimated_hashrate_hs, snap.reward_xmr, snap.xmr_usd, snap.mempool_transactions,
             snap.fee_per_byte_atomic, snap.source, snap.confidence),
        )
        self.conn.commit()

    def latest_network(self) -> NetworkSnapshot | None:
        row = self.conn.execute("SELECT * FROM network_observations ORDER BY timestamp DESC, id DESC LIMIT 1").fetchone()
        return self._network(row) if row else None

    def network_history(self, limit: int = 500) -> list[NetworkSnapshot]:
        rows = self.conn.execute(
            "SELECT * FROM network_observations ORDER BY timestamp DESC, id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [self._network(r) for r in reversed(rows)]

    def add_event(self, event_type: str, importance: float, novelty: float, payload: dict) -> None:
        self.conn.execute(
            "INSERT INTO content_events(created_at,event_type,importance,novelty,payload_json) VALUES (?,?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(), event_type, importance, novelty, json.dumps(payload)),
        )
        self.conn.commit()

    def upsert_blog_draft(self, post: BlogPostInput) -> BlogPost:
        slug = post.slug or slugify(post.title)
        now = now_iso()
        existing = self.conn.execute("SELECT * FROM blog_posts WHERE slug=?", (slug,)).fetchone()
        if existing:
            version = int(existing["content_version"]) + 1
            self.conn.execute(
                """UPDATE blog_posts SET title=?,dek=?,body_md=?,author=?,tags_json=?,source_refs_json=?,
                updated_at=?,content_version=? WHERE slug=?""",
                (post.title, post.dek, post.body_md, post.author, json.dumps(post.tags),
                 json.dumps(post.source_refs), now, version, slug),
            )
        else:
            self.conn.execute(
                """INSERT INTO blog_posts(slug,title,dek,body_md,author,status,tags_json,source_refs_json,created_at,updated_at)
                VALUES (?,?,?,?,?,'draft',?,?,?,?)""",
                (slug, post.title, post.dek, post.body_md, post.author, json.dumps(post.tags),
                 json.dumps(post.source_refs), now, now),
            )
        self.conn.commit()
        return self.get_blog(slug, include_drafts=True)

    def publish_blog(self, slug: str) -> BlogPost:
        now = now_iso()
        row = self.conn.execute("SELECT * FROM blog_posts WHERE slug=?", (slug,)).fetchone()
        if not row:
            raise KeyError(slug)
        published_at = row["published_at"] or now
        self.conn.execute(
            "UPDATE blog_posts SET status='published',published_at=?,updated_at=? WHERE slug=?",
            (published_at, now, slug),
        )
        self.conn.commit()
        return self.get_blog(slug, include_drafts=True)

    def get_blog(self, slug: str, include_drafts: bool = False) -> BlogPost | None:
        sql = "SELECT * FROM blog_posts WHERE slug=?" + ("" if include_drafts else " AND status='published'")
        row = self.conn.execute(sql, (slug,)).fetchone()
        return row_to_blog(row) if row else None

    def list_blog(self, limit: int = 50, include_drafts: bool = False) -> list[BlogPost]:
        where = "" if include_drafts else "WHERE status='published'"
        rows = self.conn.execute(
            f"SELECT * FROM blog_posts {where} ORDER BY COALESCE(published_at,updated_at) DESC,id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [row_to_blog(row) for row in rows]

    @staticmethod
    def _network(row: sqlite3.Row) -> NetworkSnapshot:
        return NetworkSnapshot(
            timestamp=row["timestamp"], height=row["height"], difficulty=row["difficulty"],
            target_seconds=row["target_seconds"], estimated_hashrate_hs=row["estimated_hashrate_hs"],
            reward_xmr=row["reward_xmr"], xmr_usd=row["xmr_usd"],
            mempool_transactions=row["mempool_transactions"], fee_per_byte_atomic=row["fee_per_byte_atomic"],
            source=row["source"], confidence=row["confidence"],
        )
