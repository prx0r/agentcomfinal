from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class PublishCapability:
    provider: str
    configured: bool
    can_upload: bool
    reason: str


class YouTubePublisher:
    """Boundary for a future YouTube Data API/OAuth adapter.

    The core repository deliberately does not pretend a video can be uploaded
    without channel OAuth credentials. The content recipe emits the exact
    upload manifest; an adapter can implement upload(manifest, video_path).
    """

    def capability(self) -> PublishCapability:
        return PublishCapability(
            provider="youtube",
            configured=False,
            can_upload=False,
            reason="OAuth upload adapter is intentionally not bundled; provide a credentialed publisher implementation.",
        )
