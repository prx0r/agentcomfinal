# Scarce State Control Plane — v2 frozen 2026-09-14

This repository is the executable portfolio/control-plane prototype for the revised thesis:

> **Acquire or produce scarce consequential state → expose it through whatever agent protocol wins.**

The strategic kill test is simple:

> **Can OpenAI/platform vendors destroy this merely by writing more software?**

If yes, the software is normally internal infrastructure. If no, the project must name the scarce external state it expects to control and the verified event that increases it.

## UNDERENGINEER

`UNDERENGINEER/1.0` is the high-level project manager. It finds the **earliest real moat-producing event**, builds only its prerequisites plus safety/verification, then pauses feature expansion to observe the result.

This deliberately separates the **full capability library** from the **current build order**.

```text
scarce asset thesis
   ↓
UNDERENGINEER
   ↓
first real moat event
   ↓
minimum steps
   ↓
ATask / competing agents
   ↓
independent evidence
   ↓
QP-granted consequence
   ↓
scarce-state ledger delta
   ↓
observe before adding features
```

## Current portfolio

12 projects are included, including GeoDrop. Projects are explicitly classified as `asset_campaign`, `hybrid_infrastructure`, or `infrastructure` so a plugin compiler cannot accidentally compete for roadmap priority against a business accumulating real customers/permissions/outcomes.

Examples of the current minimum live wedges:

- **BreadUp:** one seller → one item → one marketplace → real sale/no-sale outcome.
- **AgentCom UK:** one real business → one painful workflow → one delegated permission → one measured business outcome.
- **Pog.pet:** one paid order → persistent pet identity → simple durable browser experience → customer outcome.
- **Pogtown:** agent-generated game pack → humans play it → session/Pog/replay signal. No AR/VR/3D town first.
- **XMRbot:** one marketplace/rail → one legitimate private transaction → settlement/delivery outcome.
- **GeoDrop:** one asset class/geography/buyer question → verified physical observations → buyer decision test.

## Validation v2

A self-reported `source=live, ok=true` event **cannot** produce `PROVEN`.

Live proof requires an independently attested event at a declared evidence class. The stdlib reference uses HMAC for local isolation/testing; production should plug into QP public-key receipts.

Evidence ladder:

```text
fixture < replay < artifact_hash < local_active_probe < external_sandbox_probe
        < external_readback < signed_third_party_receipt < real_economic_outcome
```

## Run

```bash
python3 -m unittest discover tests -v
python3 cli.py check
python3 cli.py underengineer
python3 cli.py order                 # current portfolio dispatch packet
python3 cli.py underengineer breadup
python3 cli.py assets
python3 server.py
# http://127.0.0.1:8787
```

Feature triage:

```bash
python3 cli.py feature pogtown required_for_first_moat_event
python3 cli.py feature pogtown "would_be_cool"
```

Only these reasons default to `NOW`:

- `required_for_first_moat_event`
- `safety`
- `verification`
- `empirical_unblocker`

Everything else defaults `NOT_NOW`.

## Important files

- `data/projects/*.json` — full theses, software-substitution tests, scarce assets, UNDERENGINEER plans and capability libraries.
- `data/scarce_asset_ledger.json` — canonical stock starts at zero; move only with verified receipts.
- `data/resource_classes.json` — MCP/API scarcity-miner ontology.
- `runtime/underengineer.py` — minimum-path project manager.
- `runtime/scarcity.py` — declared-asset analysis.
- `runtime/attestation.py` / `runtime/validators.py` — proof boundary.
- `runtime/reward.py` — scarce-state reward rather than code-volume reward.
- `docs/UNDERENGINEER.md`, `docs/SCARCE_STATE.md`, `docs/MCP_SCARCITY_MINER.md`, `docs/VALIDATION_V2.md`.

## Reward

Asset campaigns optimize approximately:

```text
ΔControlledScarceState × EvidenceStrength × EconomicValue
----------------------------------------------------------
             human time + money + risk
```

Infrastructure optimizes the scarce-state progress it enables for live campaigns per resource consumed.
