# UNDERENGINEER/1.0

UNDERENGINEER is the high-level project manager for the portfolio.

It does **not** mean "make the smallest MVP" and it does not reward low line count. It asks:

> What is the earliest real-world event that would increase controlled scarce state or strongly falsify the business thesis?

Then it permits only work that is:

1. required for that event;
2. required for safety;
3. required for independent verification; or
4. an empirically demonstrated blocker on that path.

Everything else is `NOT_NOW`.

## Loop

```text
software substitution test
        ↓
name scarce external asset
        ↓
choose first real moat event
        ↓
minimal live product
        ↓
minimum prerequisite steps
        ↓
ATask execution
        ↓
independent attestation / QP consequence
        ↓
scarce asset ledger delta
        ↓
STOP FEATURE EXPANSION
        ↓
observe users/outcomes
        ↓
update thesis and choose next event
```

## Why this is different from an MVP

An MVP can still be mostly reproducible software. UNDERENGINEER optimizes for `time-to-real-moat-evidence`.

Example: a beautiful BreadUp photo-to-listing demo is not enough. The minimum useful experiment reaches a real listing and later a sale/no-sale outcome because that is where proprietary sell-through state begins.

Example: Pogtown does not need AR, VR or a 3D town to test its strongest network thesis. It needs a safe game-pack protocol, an agent that can create a game, humans who can actually play it, and outcome/replay signal.

## Portfolio scheduling

Scarce-asset campaigns rank first. Infrastructure is never self-prioritized. A campaign may pull QP, Cmail, security, Astra or the control plane into its minimum path. If no live campaign needs an infrastructure feature, it waits.

The ranking score in `runtime/underengineer.py` is intentionally coarse and non-canonical. It proposes attention; it does not establish truth.
