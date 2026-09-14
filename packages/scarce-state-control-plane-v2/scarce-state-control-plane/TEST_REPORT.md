# Test report — 2026-09-14

Validated before packaging:

- 18/18 Python unit tests pass.
- Campaign checkpoint graph is acyclic.
- 12 projects × 12 capability checkpoints = 144 contracts.
- 144/144 fixture validator contracts pass while remaining fixture-only.
- Raw self-reported live events cannot become `PROVEN`.
- Properly attested live evidence can become `PROVEN` only at/above the checkpoint evidence class.
- Declared scarce assets do not increment the canonical ledger.
- Every asset campaign's UNDERENGINEER first moat event maps to a declared scarce-asset acquisition event.
- Feature triage defaults nonessential work to `NOT_NOW`.
- Python compiles; JSON files parse; browser JavaScript passes `node --check` where Node is available.
- Dashboard/API smoke-tested: health, order, UNDERENGINEER, assets, project detail and root page.
- Current default UNDERENGINEER order resolves to BreadUp and does not pull the generic plugin layer into the first live path.
