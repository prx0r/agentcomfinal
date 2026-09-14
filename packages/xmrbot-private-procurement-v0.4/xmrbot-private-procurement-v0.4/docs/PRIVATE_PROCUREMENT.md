# Private procurement architecture

XMRBot 0.4 treats privacy as an optimization dimension and QP as the deterministic authority boundary.

```text
NORMAL AGENT / MCP CLIENT
          |
          v
      XMRBOT ROUTER
          |
   +------+-------+
   |              |
 discovery      proposal
   |              |
   v              v
provider data   exact action hash
                  |
                  v
               QP GRANT
          provider/action/payload
          budget/expiry/predicates
                  |
                  v
                GATE
                  |
      +-----------+-----------+
      |                       |
 local/credentialed API    manual bridge
      |                       |
      v                       v
  execution               evidence attach
      |                       |
      +-----------+-----------+
                  v
              RECEIPT
```

## Non-goals

- No custody.
- No claim of guaranteed anonymity.
- No cloud seed/private-spend-key collection.
- No generic `send_money(destination, amount)` MCP tool.
- No pretending a web form is a stable API.
- No bypass of provider KYC/policy/legal requirements.

For physical goods, private payment does not hide the delivery data a seller/carrier legitimately needs. For EVM gas, XMR can hide the source payment graph while the destination EVM payout remains public.
