CREATE TABLE IF NOT EXISTS blog_posts (
  id BIGSERIAL PRIMARY KEY,
  slug TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  dek TEXT NOT NULL DEFAULT '',
  body_md TEXT NOT NULL,
  author TEXT NOT NULL DEFAULT 'XMRBot',
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','published')),
  tags_json JSONB NOT NULL DEFAULT '[]'::jsonb,
  source_refs_json JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL,
  published_at TIMESTAMPTZ,
  content_version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_blog_status_published ON blog_posts(status, published_at DESC);
