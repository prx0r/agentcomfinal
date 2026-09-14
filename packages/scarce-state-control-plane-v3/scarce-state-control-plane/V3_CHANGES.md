# v3 changes — autonomous economic discovery

v3 keeps every v2 invariant and adds the operating layer discussed after the v2 freeze.

## 1. Feedback worlds are first-class

Every business hypothesis now chooses an external world before feature expansion:

- **A_TRUTH** — paper trading / frozen forecasts. Does the causal claim predict reality?
- **B_DEMAND** — ChatGPT app / free tool. Will anyone voluntarily use it?
- **C_ECONOMIC** — Etsy / marketplace / paid pilot. Will anyone exchange money?
- **D_SCARCE_STATE** — permission, transaction history, physical observation, network participant. Can we acquire durable consequential state?

`WORLD_SELECT` chooses the cheapest world capable of changing the decision. `internal_simulation` can rank worlds but has a proof ceiling of `replay`.

## 2. ChatGPT apps are probes, not the moat

The app/compiler stack remains. Its strategic role is now explicit: cheaply test intent and workflows, then route successful hypotheses toward an economic/scarce-state experiment. A platform vendor copying the UI does not invalidate the experiment if it already taught us which state to acquire.

## 3. Seesaw Market Lab

A 13th campaign/lab is included. It preregisters constraint → shadow-price → asset hypotheses, paper positions, horizons, benchmarks and falsifiers before resolution. It learns calibration from external market outcomes without risking capital. Paper success is explicitly not a claim of live execution alpha.

## 4. Resource bottlenecks are real objects

Stores, accounts, KYC, human attention, platform slots, permissions and cash are capacity constraints. The current planning assumptions include one primary Etsy store and one primary ChatGPT app account. The Etsy setup cost is stored as the user's current £14 planning assumption, not as platform truth.

`PORTFOLIO Scheduler` cannot allocate the same single-capacity resource twice.

## 5. Strategic H-task desk

The human is no longer the default debugger/project manager. Valid escalations are restricted to:

- strategic direction;
- physical access;
- identity/KYC;
- spend/irreversible approval;
- relationship/trust work;
- genuine taste/value judgement.

A worker being uncertain is not sufficient reason to escalate if an external or deterministic test can answer the question.

## 6. Multi-horizon autonomous portfolio

The scheduler can keep independent lanes running:

- FAST_TRUTH
- FAST_DEMAND
- ECONOMIC
- DEEP_SCARCE_STATE

Cheap simulations can run ahead of each lane. External resource capacity controls what goes live.

## 7. Strategy-family replication

Repeated mechanisms are tracked separately from projects. Real outcomes update empirical strategy-family evidence. Simulation results are counted separately and never promote a family.

Examples:

- `personalized_identity_product`
- `photo_to_money`
- `free_workflow_to_authority`
- `agent_authored_play`
- `physical_truth_to_decision`

## 8. BreadUp dogfooding

The control plane now uses the same loop we want BreadUp to offer:

`demand signal → hypothesis → frozen prediction → simulation/backtest → live offer/action → actual outcome → normalized dataset row → strategy update`.

The resulting cross-experiment outcome dataset is potentially useful product substrate for BreadUp itself.
