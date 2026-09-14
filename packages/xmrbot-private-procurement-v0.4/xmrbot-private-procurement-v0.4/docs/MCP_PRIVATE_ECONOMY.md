# MCP private-economy surface

Primary tools:

- `xmr_provider_list`
- `xmr_provider_get`
- `xmr_procurement_route`
- `xmr_provider_propose`
- `xmr_provider_read`
- `qp_grant_request`
- `qp_gate_evaluate`
- `qp_receipt_verify`

Resources:

- `xmrbot://providers`
- `xmrbot://provider/{provider_id}`

`xmr_provider_read` refuses to directly invoke capabilities marked state-changing; it returns the deterministic proposal instead. This makes the generic MCP surface safe to expose to untrusted cognition. Provider-specific local/credentialed execution should live behind the QP execution controller, not in the general discovery MCP.
