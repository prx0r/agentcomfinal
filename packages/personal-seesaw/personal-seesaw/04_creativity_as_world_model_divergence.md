# 4. Creativity as World-Model Divergence

## 4.1 Core hypothesis

A useful operational theory is:

> **Creativity is the selective compression and communication of divergences between an agent's world model and what it actually encounters — including divergences inside its own self-model.**

This is a research hypothesis, not a settled scientific definition.

It combines ideas from:
- predictive processing,
- active inference,
- memory and simulation research,
- creative cognition,
- aesthetics,
- artistic communication,
- lived experience.

It explains why:
- attention matters to creativity,
- unusual lives can generate unusual art without guaranteeing good art,
- imitation can be technically excellent but feel empty,
- mistakes can be fertile,
- a person can become more creative by becoming a better observer of their own predictions,
- AI can teach creativity without generating the artifact for you.

---

## 4.2 World model and divergence

Let the creator maintain an internal model:

\[
p_\theta(s,o)
\]

over hidden world states \(s\) and observations \(o\).

Before observation \(o_t\), the model predicts:

\[
\hat o_t=E[o_t\mid history].
\]

Reality yields:

\[
o_t.
\]

Prediction error:

\[
\delta_t=o_t-\hat o_t.
\]

But most prediction error is noise. Creative salience should weight divergence by confidence, affect, self-relevance, recurrence and explanatory reach:

\[
Salience_t=
|\delta_t|
\times Precision_t
\times Affect_t
\times SelfRelevance_t
\times Reach_t.
\]

A highly creative observer notices high-salience divergences other people:
- did not predict,
- did not observe,
- discarded,
- or could not articulate.

---

## 4.3 Creativity is not surprise alone

Randomness is surprising but usually not creative.

A useful artifact reconnects surprise to structure.

A simple objective:

\[
CreativeValue(A)=
Novelty(A)
\times Coherence(A)
\times ExperientialTruth(A)
\times Transmission(A)
\times Compression(A).
\]

A multiplicative intuition is useful: arbitrary novelty is not rescued by being very surprising if coherence is near zero.

### Novelty
Does it depart from the receiver's prior?

### Coherence
Can the receiver build a model in which the departure makes sense?

### Experiential truth
Does it faithfully encode something the creator actually encountered, inferred or discovered?

Fiction can satisfy this. The events may be invented while the work truthfully encodes grief, jealousy, desire, alienation, awe or social structure.

### Transmission
Can another mind reconstruct some relevant part of the update?

### Compression
How much lived/model change is packed into the artifact relative to its complexity?

---

## 4.4 Art as posterior transmission

Suppose experience \(e\) changes a creator's beliefs:

\[
p_{before}(z)\rightarrow p_{after}(z\mid e).
\]

Define private update:

\[
\Delta W_c.
\]

The creator produces artifact \(A\).

The audience encounters it:

\[
W_a\rightarrow W'_a.
\]

Art succeeds communicatively when meaningful structure of the creator's update is reconstructable:

\[
A\approx Encode(\Delta W_c)
\]

\[
Decode(A,W_a)\rightarrow\widehat{\Delta W_c}.
\]

Art is not a database dump. Ambiguity allows the receiver's own model to participate.

A richer objective:

\[
A^*=\arg\max_A[
I(A;\Delta W_c)
+\lambda I(\Delta W_a;\Delta W_c)
+\mu Novelty
-\rho LiteralRedundancy
].
\]

Plain English:

> Preserve enough of the creator's internal change that another person can undergo a related change, without reducing the work to an explicit explanation.

This gives a rigorous version of the intuition that an imperfect human song can matter more than a flawless synthetic one.

The listener may be consuming **evidence that another finite conscious organism encountered something and chose to transmit it this way**.

---

## 4.5 Human provenance as Bayesian evidence

When a work is credibly human-made, the receiver can infer:

\[
P(lived\ state\mid artifact,human\ source)
\]

that does not have the same interpretation under:

\[
P(lived\ state\mid artifact,synthetic\ source).
\]

This does not mean AI artifacts cannot move people.

It means source changes *what the artifact is evidence of*.

A breakup song by a person can be heard partly as testimony. A generated breakup song can reproduce acoustic and semantic patterns without being evidence that the generator lived through a breakup.

If testimony is part of utility, the goods are not identical.

This matches empirical findings that human labels can increase art appraisal and that perceived emotional involvement can mediate higher purchase intent for human-designed art-infused products.

---

## 4.6 "You can tell when it's lived" — split the claim

Strong claim:

> People can reliably detect lived experience from content alone.

This may be false in many domains. AI-generated poetry and other media can fool people.

Better claim:

> Credible lived provenance can alter interpretation and value even when content alone is hard to classify.

Two channels:

### Content channel
Can the artifact statistically resemble lived expression?

AI may become excellent here.

### Provenance channel
Did the artifact causally descend from a real person's experience and choices?

That remains a distinct variable even if content is indistinguishable.

Future art markets may care increasingly about provenance precisely because content quality becomes abundant.

---

## 4.7 Why imperfection can gain value

When technical perfection is scarce, perfection is impressive.

When technical perfection is free, imperfection can become informative.

A cracked voice, timing variation, odd metaphor or rough brush mark can signal:
- physical constraint,
- decision history,
- risk,
- effort,
- individuality,
- unoptimized intention.

This does **not** mean bad art becomes good.

It means optimal smoothness loses signaling power.

Scarcity can shift from:

\[
technical\ execution
\]

to:

\[
credible\ trajectory.
\]

---

## 4.8 Can creativity be taught?

Not as a deterministic recipe for genius, but many component processes can be trained.

### The loop

1. **Predict** — before an event, write what you expect.
2. **Observe** — record external/internal observations with minimal interpretation.
3. **Compute divergence** — what violated expectation?
4. **Weight** — noise, personal bias, recurring pattern, anomaly with reach, emotional contradiction?
5. **Update** — what changed in your world model?
6. **Transfer** — where else would this imply something surprising?
7. **Encode** — story, image, melody, model, joke, theorem, product, experiment.
8. **Decode-test** — ask another person what changed for them, not merely whether they liked it.
9. **Compare** — did they reconstruct the intended structure? Did they find a better one?
10. **Re-update** — audience response becomes new evidence.

This is a closed creative learning loop.

---

## 4.9 The Divergence Journal

| field | question |
|---|---|
| prior | What did I expect? |
| observation | What actually happened? |
| divergence | What differed? |
| confidence | How strong was my prior? |
| affect | Why did this matter emotionally? |
| self_model | What did this reveal about me? |
| world_model | What did this reveal about the world? |
| recurrence | Have I seen this structure elsewhere? |
| analogy | What distant domain has the same shape? |
| compression | Express the update in one sentence/image/riff. |
| artifact | What could transmit it? |
| audience_decode | What did another person receive? |
| update | What do I believe now? |

Over months, the important object is not one entry. It is the **graph of recurring divergences**.

That graph may be a person's creative signature.

---

## 4.10 Creativity as non-consensus calibration

A creator has an edge when their posterior differs usefully from consensus:

\[
Edge=
D_{KL}(P_{creator}\|P_{consensus})
\times Calibration
\times Relevance.
\]

High divergence + low calibration = delusion.

High calibration + no divergence = consensus competence.

Creativity lives in:

> meaningfully non-consensus + reality-linked.

This is structurally similar to investment alpha.

---

## 4.11 Seesaw, science, entrepreneurship and art share a primitive

Seesaw:

\[
new\ information\rightarrow model\ update\rightarrow constraint\ delta\rightarrow action.
\]

Creativity:

\[
new\ experience\rightarrow model\ update\rightarrow salient\ divergence\rightarrow artifact.
\]

Science:

\[
anomaly\rightarrow model\ update\rightarrow hypothesis\rightarrow experiment.
\]

Entrepreneurship:

\[
unpriced\ change\rightarrow model\ update\rightarrow opportunity\rightarrow company.
\]

Different interfaces over one metacognitive primitive:

\[
\boxed{
Predict\rightarrow Observe\rightarrow Detect\ Divergence\rightarrow Update\rightarrow Externalize
}
\]

Outputs differ:
- trader: position,
- scientist: hypothesis,
- artist: artifact,
- entrepreneur: organization,
- philosopher: distinction.

---

## 4.12 A JEPA-compatible creativity tutor

Do not ask the model to "be creative for you."

Let:

\[
z_t=Encoder(person\ history,current\ worldmodel).
\]

Person makes prediction \(p_t\).

Observation \(o_{t+1}\) arrives.

Encode future state:

\[
z_{t+1}=TargetEncoder(o_{t+1},reflection_{t+1}).
\]

Train predictor:

\[
\hat z_{t+1}=F(z_t,context_t).
\]

Divergence:

\[
d_t=d(\hat z_{t+1},z_{t+1}).
\]

The tutor surfaces high-value divergences and asks the human to interpret them.

A second action-conditioned model could learn:

\[
F(z_t,creative\ operation)\rightarrow \hat z_{audience}
\]

with operations such as:
- invert,
- exaggerate,
- compress,
- juxtapose,
- analogize,
- concretize,
- personify,
- remove explanation,
- change viewpoint,
- change temporal scale.

The AI becomes:
- prediction recorder,
- anomaly detector,
- memory,
- analogy engine,
- audience simulator,
- editor.

The **human remains the primary sensor and source of lived updates**.

This is a more interesting creativity system than prompt → artifact.

---

## 4.13 A pedagogy of creativity

### Level 1 — Prediction awareness
Make explicit forecasts about ordinary events.

### Level 2 — Sensory precision
Describe without immediately interpreting.

### Level 3 — Internal observation
Notice affect, desire, avoidance, bodily state and narrative formation.

### Level 4 — Error discrimination
Separate randomness from meaningful violations.

### Level 5 — Model revision
Update beliefs rather than collecting anomalies.

### Level 6 — Analogy
Find similar structures in distant domains.

### Level 7 — Medium translation
Encode the same update in prose, diagram, story, image, rhythm.

### Level 8 — Audience modeling
Predict how different receivers will decode it.

### Level 9 — Deliberate divergence
Seek environments likely to falsify your own model.

### Level 10 — Signature
Identify recurring private questions/divergences across years.

The curriculum becomes:

> Become a better calibrated observer of what reality does to your model, then learn to transmit the update.

---

## 4.14 Failure modes

### Surprise addiction
Optimizing novelty creates weirdness without truth.

### Trauma mining
Treating suffering as content can reward self-exploitation.

### Performative authenticity
A human-provenance premium creates incentives to manufacture signs of struggle.

### AI homogenization
If everyone uses the same assistant to interpret their divergences, the tutor can erase individuality.

### Model narcissism
Excessive self-observation can turn creativity into endless autobiography.

### Audience overfitting
Optimizing decoder response can reduce art to engagement engineering.

### False-world-model reinforcement
Rewarding coherent divergence without reality checks can intensify delusion.

A good tutor should reward:
- calibration,
- evidence contact,
- uncertainty,
- multiple interpretations,
- long-term correction.

---

## 4.15 Deep implication

If AI becomes better than humans at artifact execution, creativity education becomes **more important**, not less.

Execution stops being the bottleneck.

The bottleneck becomes:

> What have you actually noticed that is worth encoding?

Creative status shifts toward:
- perception,
- lived experience,
- taste,
- courage,
- model revision,
- selection,
- transmission.

The future artist may be someone with an unusually rich, well-observed causal history who uses machines to transmit it without laundering away its provenance.
