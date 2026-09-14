# 1. Personal Seesaw Theory

## 1.1 From industrial capital to personal capital

Traditional Seesaw:

\[
Innovation
\rightarrow \Delta Constraint
\rightarrow \Delta ShadowPrice
\rightarrow CapitalAllocation
\rightarrow SupplyResponse
\rightarrow ConstraintRelaxation.
\]

Personal Seesaw:

\[
Innovation
\rightarrow \Delta MachineCapability
\rightarrow \Delta TaskFeasibility
\rightarrow \Delta HumanScarcity
\rightarrow \Delta PersonalReturn
\rightarrow TimeAllocation
\rightarrow Skill/AssetSupply.
\]

A person's scarce resource is not merely money. It is **remaining high-quality attention over a finite lifetime**.

A skill can still be useful and nevertheless be a bad investment if it requires years to acquire while its scarcity collapses faster than the learner can capture the return. The relevant comparison is not useful vs useless. It is **future-adjusted opportunity cost**.

---

## 1.2 Activity is not output

Let an activity \(x\) produce output \(y\).

A narrow economic model assumes:

\[
U(x)\approx V(y).
\]

For humans:

\[
U(x)=
U_{economic}
+U_{instrumental}
+U_{mastery}
+U_{play}
+U_{identity}
+U_{social}
+U_{status}
+U_{communication}
+U_{witness}
+U_{embodiment}
+U_{autonomy}
+U_{care}
+U_{transcendence}.
\]

Technology can annihilate \(U_{economic}\) while barely affecting several other terms.

A car dominates a runner as transport. Running survives because transport was not the only motive.

A chess engine dominates humans at move selection. Chess survives because optimal move generation was not the entire product.

A camera dominates cheap literal visual capture. Portrait painting survives because literal capture was not the entire value of portraiture.

This yields four distinct notions:

### Economic obsolescence
A human is no longer cost-effective as producer of a commodity output.

### Instrumental obsolescence
The activity is no longer the efficient way to achieve a practical goal.

### Cultural obsolescence
The social practice substantially disappears.

### Existential obsolescence
Humans no longer obtain meaningful utility from doing it.

These happen at different times. The final one is much rarer.

---

## 1.3 The motive-residual test

For any threatened activity ask:

> If the output became perfect and free tomorrow, which reasons for doing this would remain?

Define motive vector:

\[
m_x=[e,i,ma,p,id,soc,st,com,wit,emb,aut,care,tr].
\]

Technology applies a substitution vector \(q_t\), not one scalar.

\[
R_x(t)=\sum_j w_jm_{x,j}(1-q_{t,j}).
\]

This is the **motive residual**.

Commodity portrait production can be heavily substituted while identity, communication, provenance, ritual, status and mastery remain.

---

## 1.4 Skill capital vs asset capital

A dangerous strategy is accumulating **skill without ownership** in an area where machine supply rises rapidly.

### Skill capital
What you can personally do.

### Asset capital
What persists and compounds even when someone or something else can do the work.

Examples:
- audience/distribution,
- reputation,
- proprietary data,
- accumulated observations,
- relationships,
- legal rights,
- physical access,
- capital,
- brand,
- standards/protocol position,
- provenance,
- recurring cash flow,
- verified history.

If AI makes a skill cheap but the activity simultaneously builds a scarce asset, continuing can still be rational.

Generic SEO writing builds little durable scarcity.

A field journal based on unique direct observations builds an archive whose value may rise as agents gain more reading capacity.

---

## 1.5 Positive-AI-beta assets

Let \(M\) denote machine capability.

\[
\beta_{AI}(a)=\frac{\partial V(a)}{\partial M}.
\]

Three classes:

\[
\beta_{AI}<0 \quad substitute
\]

\[
\beta_{AI}\approx0 \quad neutral
\]

\[
\beta_{AI}>0 \quad complement.
\]

Potential positive-beta assets include:

- **Ground truth:** more reasoning can increase demand for observations the system cannot infer.
- **Authority:** more agents can increase demand for permission to transact, deploy, sign, own or act.
- **Trust/reputation:** more generated content can increase the value of reliable filters and identities.
- **Distribution/attention:** more supply can make trusted access to audiences scarcer.
- **Physical access:** digital abundance does not create scarce locations, samples or permissions.
- **Human provenance:** if audiences value evidence of another person's lived trajectory, provenance becomes differentiating.
- **Evaluation/taste:** as generation becomes cheap, selection can become the bottleneck.

The rule is not merely "learn AI."

> Stand where improved AI increases demand for what you uniquely control.

---

## 1.6 Task-chain closure

Represent a workflow as graph \(G=(V,E)\).

Each node is a production step. An economically autonomous system must execute a **closed chain** from input to valuable output, including exceptions, verification and deployment.

Let \(p_v(t)\) be machine feasibility for step \(v\).

A naive automation measure:

\[
\bar p=\frac{1}{|V|}\sum p_v.
\]

For a strict serial chain:

\[
P(\text{closed automation})\approx\prod_v p_v.
\]

This is why a modest improvement at the final bottleneck can matter more than a large improvement on an already-automated step.

Personal implication:

> Learn where the unclosed edge is likely to remain — or own the interface that closes it.

---

## 1.7 Human-source premium

Some outputs carry utility conditional on source.

\[
HSP_x=
E[WTP\mid y,\ human\ provenance]
-
E[WTP\mid y,\ machine\ provenance].
\]

It can arise because the artifact functions as:
- evidence about another person's state,
- costly effort,
- testimony,
- social connection,
- membership in a lineage,
- authenticity/status,
- a trace of a finite life.

A synthetic recording can sound better than a live singer and still fail to fully substitute for attending that person's performance.

**Source can be a feature of the product.**

This is an empirical question, not a metaphysical assumption. Existing experiments already show that human vs AI source labels can alter appraisal and purchase intent.

---

## 1.8 Scarcity gradients

For capability/activity \(x\):

\[
S_x(t)=\frac{D_x(t)}
{H_x(t)+\lambda M_x(t)}
\]

with:
- \(D_x\): demand,
- \(H_x\): effective human supply,
- \(M_x\): effective machine supply,
- \(\lambda\): substitutability.

Define:

\[
G_x=\frac{d\log S_x}{dt}.
\]

Interpretation:
- \(G_x\ll0\): rapidly commoditizing.
- \(G_x\approx0\): stable.
- \(G_x\gg0\): tightening bottleneck.

This is Personal Seesaw's equivalent of tracking changing shadow prices.

---

## 1.9 Skill half-life

Let \(h_x(t)\) be the hazard that a skill's current economic advantage is halved.

\[
H_x\approx\frac{\ln2}{\bar h_x}.
\]

Let acquisition time be \(L_x\).

\[
Q_x=\frac{H_x}{L_x}.
\]

If \(Q_x<1\), the advantage may decay before the learner finishes acquiring it.

But this applies to the **economic component**, not to mastery/play/identity.

The key question becomes:

> Am I learning this because I expect economic scarcity, or because I value the practice?

---

## 1.10 Robustness across futures

Do not optimize against one AGI date.

Let scenario \(s\) have probability \(p_s\):

\[
E[V_x]=\sum_s p_sV(x\mid s).
\]

Useful scenarios:
- S0: progress slows.
- S1: strong copilots, weak autonomy.
- S2: reliable digital agents.
- S3: strong world models + robotics.
- S4: broadly superhuman cognitive systems.

Robust personal capital has decent value across most scenarios and exceptional value in several.

---

## 1.11 The Personal Seesaw loop

For every disruptive signal:

1. **Capability delta** — what became newly possible, cheaper, faster or reliable?
2. **Chain closure** — which formerly human workflow can now execute end-to-end?
3. **Industry map** — what constraints loosen/tighten? Which shadow prices move?
4. **Motive map** — why are humans doing the affected activities?
5. **Scarcity split** — which outputs become abundant? Which human residuals remain scarce?
6. **Personal capital map** — which skills are substitutes, complements, options or dead-end transition skills?
7. **Time trade** — given acquisition times and half-lives, what should a person stop, start, own, or continue purely for nonmarket reasons?
8. **Falsifiers** — what would make the forecast wrong?

This makes Seesaw dual-use:

\[
new\ information
\rightarrow
\begin{cases}
industry\ impact\\
person\ impact
\end{cases}
\]

---

## 1.12 Living in the future

Bad version:

> Pretend one vivid future is certain.

Good version:

> Internalize high-confidence capability trajectories early enough that you stop spending scarce years defending rents whose causal basis is disappearing.

The best futurist identifies:
- irreversible curves,
- closing chains,
- emerging bottlenecks,
- lagging institutions,
- durable human motives,

then moves capital before consensus reprices them.
