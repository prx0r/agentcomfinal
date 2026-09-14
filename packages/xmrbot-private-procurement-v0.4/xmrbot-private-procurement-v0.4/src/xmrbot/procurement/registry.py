from __future__ import annotations
from typing import Iterable
from xmrbot.procurement.models import CapabilityClass as C, IntegrationMode as M, ProviderCapability as Cap, ProviderDescriptor as P
from xmrbot.procurement.adapters import (
    BasicSwapAdapter, HavenoAdapter, KYCnotAdapter, ManualBridgeAdapter, MoneroWalletRPCAdapter,
    OneGweiAdapter, OrbitSwapAdapter, TrocadorAnonPayAdapter, XMRCheckoutAdapter,
)


def cap(name, klass, mode, desc, *, state=False, grant=False, endpoint=None):
    return Cap(name=name, capability_class=klass, mode=mode, state_changing=state, requires_grant=grant, description=desc, endpoint_hint=endpoint)

PROVIDERS: list[P] = [
    P(id="kycnot", name="KYCnot.me", category=["registry","privacy","discovery"], canonical_url="https://kycnot.me/", agentability=.90,
      privacy_notes=["Returns KYC level and verification metadata; verification is evidence, not a safety guarantee."],
      capabilities=[cap("service_get",C.DISCOVER,M.NATIVE_API,"Fetch structured service metadata by id/slug/url."), cap("service_search",C.DISCOVER,M.MANUAL_BRIDGE,"Search/browse service registry; exact API search contract may change.")],
      source_urls=["https://kycnot.me/docs/api"]),
    P(id="xmrbazaar", name="XMRBazaar", category=["marketplace","goods","services","escrow","wanted"], canonical_url="https://xmrbazaar.com/", agentability=.72,
      privacy_notes=["Non-custodial direct XMR and client-side 2-of-3 multisig escrow are available on supported listings.","Physical delivery can reveal delivery information to the seller."],
      capabilities=[cap("search",C.DISCOVER,M.READ_ONLY_WEB,"Discover public listings."), cap("purchase_proposal",C.PROPOSE,M.MANUAL_BRIDGE,"Create a bounded order/offer proposal without spending.",state=True,grant=True), cap("wanted_proposal",C.PROPOSE,M.MANUAL_BRIDGE,"Prepare a Wanted listing for human/API submission.",state=True,grant=True), cap("order_status",C.STATUS,M.MANUAL_BRIDGE,"Attach order state as evidence."), cap("api_future",C.EXECUTE,M.UPCOMING_API,"JSON automation API announced May 2026; adapter seam reserved.",state=True,grant=True)],
      source_urls=["https://xmrbazaar.com/changelog/","https://xmrbazaar.com/faq/","https://xmrbazaar.com/escrow-guide/"], caveats=["Transactional JSON API is announced but not launched as of the 2026-08-16 changelog."]),
    P(id="monerojobs", name="Monero.Jobs", category=["labor","jobs","freelance"], canonical_url="https://monero.jobs/", agentability=.58,
      privacy_notes=["Platform advertises no KYC, anonymous proposals and zero platform fees."],
      capabilities=[cap("browse_jobs",C.DISCOVER,M.READ_ONLY_WEB,"Browse current XMR-denominated jobs."), cap("hire_proposal",C.PROPOSE,M.MANUAL_BRIDGE,"Prepare a job post or freelancer contact proposal.",state=True,grant=True), cap("work_proposal",C.PROPOSE,M.MANUAL_BRIDGE,"Prepare an application/bid proposal.",state=True,grant=True)], source_urls=["https://monero.jobs/","https://monero.jobs/jobs"]),
    P(id="haveno", name="Haveno", category=["exchange","p2p","fiat"], canonical_url="https://haveno.exchange/", agentability=.95,
      privacy_notes=["Local non-custodial daemon connects over Tor; API grants wallet/trade control and must remain local/firewalled."],
      capabilities=[cap("market",C.DISCOVER,M.LOCAL_API,"Read prices and offers from a local Haveno daemon."), cap("offer_proposal",C.PROPOSE,M.LOCAL_API,"Prepare create/take-offer parameters.",state=True,grant=True), cap("trade_status",C.STATUS,M.LOCAL_API,"Read trade state."), cap("trade_execute",C.EXECUTE,M.LOCAL_API,"Execute a pre-authorized offer/trade via local Haveno bridge.",state=True,grant=True)], source_urls=["https://docs.haveno.exchange/users/haveno-api/"]),
    P(id="orbitswap", name="OrbitSwap", category=["swap","exchange"], canonical_url="https://orbitswap.io/", agentability=.96,
      capabilities=[cap("currencies",C.DISCOVER,M.NATIVE_API,"List supported assets."),cap("rate",C.QUOTE,M.NATIVE_API,"Get public swap quote/limits."),cap("create_transaction",C.EXECUTE,M.NATIVE_API,"Create a swap transaction with an API key.",state=True,grant=True),cap("transaction_status",C.STATUS,M.NATIVE_API,"Read transaction status.")], source_urls=["https://orbitswap.io/api-docs"]),
    P(id="trocador", name="Trocador AnonPay", category=["swap","payment_router","merchant"], canonical_url="https://trocador.app/", agentability=.92,
      capabilities=[cap("create_invoice",C.PROPOSE,M.NATIVE_API,"Create an indirect AnonPay transaction bound to receiver/amount.",state=True,grant=True), cap("status",C.STATUS,M.NATIVE_API,"Check AnonPay status by ID.")], source_urls=["https://trocador.app/anonpaydocumentation"]),
    P(id="1gwei", name="1gwei.dev", category=["gas","evm","bridge"], canonical_url="https://1gwei.dev/", agentability=.99,
      privacy_notes=["XMR can fund native EVM gas; the destination EVM payout remains public on the destination chain."],
      capabilities=[cap("quote",C.QUOTE,M.NATIVE_API,"Quote native gas top-up."),cap("create_order",C.EXECUTE,M.NATIVE_API,"Create gas order using XMR/LN/x402 payment method.",state=True,grant=True),cap("order_status",C.STATUS,M.NATIVE_API,"Poll gas order status.")], source_urls=["https://1gwei.dev/guides/agent-api-scripted-gas-top-ups"]),
    P(id="basicswap", name="BasicSwap", category=["swap","atomic_swap","dex"], canonical_url="https://basicswapdex.com/", agentability=.86,
      privacy_notes=["Local, non-custodial atomic swap protocol; protect local JSON API with client authentication."],
      capabilities=[cap("wallets",C.DISCOVER,M.LOCAL_API,"Inspect local BasicSwap wallets via JSON API."),cap("swap_proposal",C.PROPOSE,M.LOCAL_API,"Prepare atomic-swap offer/take parameters.",state=True,grant=True)], source_urls=["https://docs.basicswapdex.com/docs/user-guides/web-ui-authentication/","https://basicswapdex.com/protocol.html"]),
    P(id="wallet_rpc", name="monero-wallet-rpc", category=["wallet","settlement"], canonical_url="https://www.getmonero.org/", agentability=1.0,
      privacy_notes=["Run locally; XMRBot never accepts/export seed phrases or private spend keys through MCP."],
      capabilities=[cap("balance",C.DISCOVER,M.LOCAL_API,"Read wallet balance."),cap("create_address",C.PROPOSE,M.LOCAL_API,"Create a subaddress locally.",state=True,grant=False),cap("validate_address",C.VERIFY,M.LOCAL_API,"Validate Monero address."),cap("transfer",C.EXECUTE,M.LOCAL_API,"Transfer XMR only under exact QP grant.",state=True,grant=True)], source_urls=["https://docs.getmonero.org/rpc-library/wallet-rpc/"]),
    P(id="xmrcheckout", name="XMR Checkout", category=["merchant","checkout","webhooks"], canonical_url="https://xmrcheckout.com/", agentability=.94,
      privacy_notes=["Self-hostable non-custodial checkout; wallet receives XMR while checkout observes invoice state."],
      capabilities=[cap("server_info",C.DISCOVER,M.LOCAL_API,"Check self-hosted checkout server."),cap("list_webhooks",C.DISCOVER,M.LOCAL_API,"List store webhooks.")], source_urls=["https://xmrcheckout.com/docs","https://xmrcheckout.com/guides"]),
    P(id="kuno", name="Kuno", category=["fundraising","crowdfunding"], canonical_url="https://kuno.anne.media/", agentability=.48,
      privacy_notes=["Fundraisers can be pseudonymous and funds go to the fundraiser wallet; creation requires primary address and private view key on provider flow."],
      capabilities=[cap("browse",C.DISCOVER,M.READ_ONLY_WEB,"Discover public fundraisers/RSS."),cap("fundraiser_proposal",C.PROPOSE,M.MANUAL_BRIDGE,"Prepare fundraiser content and wallet boundary plan; do not send view key through XMRBot cloud.",state=True,grant=True)], source_urls=["https://kuno.anne.media/faq/"]),
    P(id="njalla", name="Njalla", category=["domains","vps","vpn","infrastructure"], canonical_url="https://njal.la/", agentability=.62,
      capabilities=[cap("catalog",C.DISCOVER,M.READ_ONLY_WEB,"Discover domains/VPS/VPN offerings."),cap("purchase_proposal",C.PROPOSE,M.MANUAL_BRIDGE,"Prepare bounded infrastructure purchase.",state=True,grant=True)], source_urls=["https://njal.la/"]),
    P(id="hosting1984", name="1984 Hosting", category=["vps","hosting","domains","infrastructure"], canonical_url="https://1984.hosting/", agentability=.55,
      capabilities=[cap("catalog",C.DISCOVER,M.READ_ONLY_WEB,"Discover VPS/hosting/domain offerings."),cap("purchase_proposal",C.PROPOSE,M.MANUAL_BRIDGE,"Prepare bounded hosting purchase.",state=True,grant=True)], source_urls=["https://1984.hosting/"]),
    P(id="serversguru", name="Servers Guru", category=["vps","infrastructure","compute"], canonical_url="https://servers.guru/", agentability=.62,
      capabilities=[cap("catalog",C.DISCOVER,M.READ_ONLY_WEB,"Discover XMR-paid VPS plans."),cap("purchase_proposal",C.PROPOSE,M.MANUAL_BRIDGE,"Prepare bounded VPS purchase.",state=True,grant=True)], source_urls=["https://servers.guru/monero-vps/"]),
    P(id="silentlink", name="Silent Link", category=["esim","connectivity"], canonical_url="https://silent.link/", agentability=.58,
      privacy_notes=["No KYC/email required according to provider; eSIM/network usage has its own telecom metadata considerations."],
      capabilities=[cap("catalog",C.DISCOVER,M.READ_ONLY_WEB,"Discover eSIM plans and coverage."),cap("purchase_proposal",C.PROPOSE,M.MANUAL_BRIDGE,"Prepare plan purchase and funding proposal.",state=True,grant=True)], source_urls=["https://silent.link/"]),
    P(id="anonymouslabels", name="AnonymousLabels", category=["shipping","logistics"], canonical_url="https://anonymouslabels.com/", agentability=.64,
      privacy_notes=["Shipping necessarily involves recipient/sender logistics data even when payment is private."],
      capabilities=[cap("quote_proposal",C.PROPOSE,M.MANUAL_BRIDGE,"Prepare dimensions/route for carrier quote."),cap("label_purchase_proposal",C.PROPOSE,M.MANUAL_BRIDGE,"Prepare shipping label purchase.",state=True,grant=True)], source_urls=["https://anonymouslabels.com/","https://anonymouslabels.com/pay-with-monero"]),
    P(id="xmrcards", name="XMR.CARDS", category=["gift_cards","retail_router"], canonical_url="https://xmr.cards/", agentability=.64,
      capabilities=[cap("catalog",C.DISCOVER,M.READ_ONLY_WEB,"Discover current gift-card catalog/limits."),cap("purchase_proposal",C.PROPOSE,M.MANUAL_BRIDGE,"Prepare card purchase without exposing wallet authority.",state=True,grant=True)], source_urls=["https://xmr.cards/"]),
    P(id="coinsbee", name="CoinsBee", category=["gift_cards","mobile_topup","retail_router"], canonical_url="https://www.coinsbee.com/", agentability=.55,
      capabilities=[cap("catalog",C.DISCOVER,M.READ_ONLY_WEB,"Discover gift cards/mobile topups."),cap("purchase_proposal",C.PROPOSE,M.MANUAL_BRIDGE,"Prepare card/top-up purchase.",state=True,grant=True)], source_urls=["https://www.coinsbee.com/"]),
    P(id="shopinbit", name="ShopinBit Concierge", category=["concierge","goods","services","procurement"], canonical_url="https://shopinbit.com/concierge/", agentability=.62,
      privacy_notes=["Human concierge; provider says requests may cover legal products/services and encrypted communication. Physical fulfillment can reveal delivery details."],
      capabilities=[cap("request_proposal",C.PROPOSE,M.MANUAL_BRIDGE,"Prepare a concise legal procurement request.",state=True,grant=True),cap("offer_evidence",C.VERIFY,M.MANUAL_BRIDGE,"Normalize returned concierge offer into QP evidence.")], source_urls=["https://shopinbit.com/concierge/"]),
    P(id="btcpay", name="BTCPay Server + Monero integration", category=["merchant","checkout"], canonical_url="https://btcpayserver.org/", agentability=.65,
      capabilities=[cap("merchant_plan",C.PROPOSE,M.MANUAL_BRIDGE,"Plan self-hosted merchant integration through BTCPay-compatible surfaces."),], source_urls=["https://docs.btcpayserver.org/"]),
]

ADAPTER_CLASSES = {
    "kycnot": KYCnotAdapter,
    "orbitswap": OrbitSwapAdapter,
    "1gwei": OneGweiAdapter,
    "trocador": TrocadorAnonPayAdapter,
    "xmrcheckout": XMRCheckoutAdapter,
    "wallet_rpc": MoneroWalletRPCAdapter,
    "basicswap": BasicSwapAdapter,
    "haveno": HavenoAdapter,
}


class ProviderRegistry:
    def __init__(self, http=None):
        self.http=http
        self._descriptors={p.id:p for p in PROVIDERS}

    def all(self) -> list[P]: return list(self._descriptors.values())
    def get(self, provider_id: str) -> P:
        if provider_id not in self._descriptors: raise KeyError(provider_id)
        return self._descriptors[provider_id]
    def search(self, query: str="") -> list[P]:
        q=query.lower().strip()
        if not q: return self.all()
        return [p for p in self.all() if q in " ".join([p.id,p.name,*p.category,*[c.name+" "+c.description for c in p.capabilities]]).lower()]
    def adapter(self, provider_id: str):
        p=self.get(provider_id)
        cls=ADAPTER_CLASSES.get(provider_id, ManualBridgeAdapter)
        a=cls(self.http); a.descriptor=p; return a

registry = ProviderRegistry()
