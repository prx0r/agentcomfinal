# Adding a provider

1. Research only the provider's official/current documentation.
2. Add a `ProviderDescriptor` in `xmrbot.procurement.registry` with source URLs and honest integration mode.
3. If a stable API exists, implement a dedicated adapter subclass. If not, use `ManualBridgeAdapter`; do not simulate a transactional API with brittle scraping.
4. Mark every state-changing capability `state_changing=True` and `requires_grant=True`.
5. Add mock-transport contract tests that assert method/path/auth/payload semantics.
6. Add a fixture/normalizer test for provider responses.
7. Expose no seed/private-spend-key inputs.
8. Regenerate `docs/PROVIDER_MATRIX.md` and provider sheet.
9. Run `scripts/validate.sh`.

## State-changing execution rule

The generic public MCP does not expose a provider `execute` method. An execution controller should construct an exact `ProviderAction`, obtain an approved `QPGrant`, evaluate it deterministically, invoke the credentialed/local adapter, and append an `ActionReceipt`.
