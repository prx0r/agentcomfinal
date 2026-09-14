from __future__ import annotations
from .base import ProviderAdapter
from xmrbot.procurement.models import IntegrationMode, ProviderResult

class ManualBridgeAdapter(ProviderAdapter):
    async def invoke(self, action, payload):
        cap=self.capability(action)
        return ProviderResult(
            provider_id=self.descriptor.id,
            action=action,
            data={"status":"manual_bridge","payload":payload,"next":"Use provider human/web flow; retain the QP proposal hash and attach provider response as evidence before settlement.","endpoint_hint":cap.endpoint_hint},
            source=self.descriptor.source_urls[0] if self.descriptor.source_urls else self.descriptor.canonical_url,
            mode=cap.mode,
            live=False,
        )
