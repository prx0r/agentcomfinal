# 0. Seesaw Thesis

## 0.1 Original form

Seesaw models technological change as a sequence of changing constraints:

\[
Innovation
\rightarrow
\Delta Constraint
\rightarrow
\Delta ShadowPrice
\rightarrow
CapitalAllocation
\rightarrow
SupplyResponse
\rightarrow
ConstraintRelaxation
\rightarrow \cdots
\]

The practical source of alpha is **lower causal-discovery latency** than other actors.

Do not predict every downstream consequence of a breakthrough. Instead:

1. detect the capability delta;
2. identify which constraints changed sign or magnitude;
3. inspect prices/behavior/outcomes for confirmation;
4. allocate before the repricing is complete.

## 0.2 Project form

For a project:

\[
Innovation
\rightarrow
\Delta CommoditySoftware
\rightarrow
\Delta ProjectMoat
\rightarrow
\Delta FeaturePriority
\rightarrow
EngineeringAllocation
\]

The question is not:

> Is this feature useful?

It is:

> **Will this feature remain scarce relative to the capability frontier, and does building it cause us to own the scarcity?**

## 0.3 The "lab attack" thought experiment

For every feature \(f\), imagine:

> Tomorrow OpenAI/Anthropic/DeepSeek/Muse ships the best plausible generic implementation of this software capability for free.

Then ask:

- Does our feature still matter?
- Do users still need *our* state/data/permissions/supply?
- Does the better model make our asset more useful?
- Can we swap in the new model and preserve the moat?

This creates a high-value filter:

```text
LAB ATTACK DESTROYS FEATURE
  -> implementation was the moat
  -> weak

LAB ATTACK IMPROVES FEATURE
  -> external scarcity was the moat
  -> strong
```

## 0.4 Positive-AI-beta

For asset \(x\):

\[
\beta_{AI}(x)=\frac{\partial V_x}{\partial M}
\]

where \(M\) is frontier model capability.

Prefer:

\[
\beta_{AI} > 0
\]

Examples:

- authoritative external data;
- permissions;
- real-world action;
- trajectory datasets;
- compute/energy;
- marketplace liquidity;
- trusted execution;
- regulated access.

Avoid making a moat out of anything where:

\[
\beta_{AI} < 0
\]

such as generic writing, summarization, generic code generation, basic wrappers, generic RAG, generic search orchestration.

## 0.5 External-state theorem

A model can improve its reasoning without gaining arbitrary access to reality.

Therefore the durable strategic question is:

\[
\boxed{\text{What consequential state exists outside the model's weights and context?}}
\]

Durable categories:

### Observation rights
Who may observe live/private reality?

### Action rights
Who may alter consequential state?

### Supply ownership
Who owns the scarce physical/economic resource?

### Outcome history
Who has the state-action-outcome trajectories?

### Trust / liability
Who is believed, licensed, insured, accountable?

### Network state
Where are the buyers, sellers, workers, agents, or counterparties?

### Physical state
What exists in the world and can actually be manipulated?

## 0.6 Software becomes adapter, not asset

In the target regime:

```text
owned scarce state
      |
      v
thin software adapter
      |
      v
whatever agent interface wins
```

The adapter should be replaceable.

If the adapter is the company, Seesaw should treat the project as fragile.

