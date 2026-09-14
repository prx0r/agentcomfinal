---
original_r2_key: "goated thesis"
sha12: d7723ad9dca2
size_bytes: 53643
description: "Core scarcity-migration thesis (canonical, dupe of 'insane theis')"
---

Yes. After pushing the thesis through the other project threads and the newest 2026 research, I think the kernel is still **one abstraction too shallow**.

The useful object is not merely:

$$
\text{future world} - \text{current world}
$$

It is:

$$
\boxed{
\text{What does increasing abundance make newly scarce?}
}
$$

AGI makes cognition, search, design, coding, simulation and hypothesis generation abundant. That abundance creates **induced demand for their complements**. Those complements then become bottlenecks, attract rents, trigger investment, eventually get relieved, and push scarcity somewhere else.

So what we actually want to model is a **moving scarcity surface**.

---

# 1. The upgraded thesis: invest in scarcity migration

Think about the sequence we have gradually converged on across the project:

```text
INTELLIGENCE BECOMES ABUNDANT
          ↓
hypotheses/designs/code become abundant
          ↓
VERIFICATION becomes scarce
          ↓
verification gets automated
          ↓
PHYSICAL EXPERIMENTS become scarce
          ↓
experiments scale
          ↓
INSTRUMENTS / LAB CAPACITY / MATERIALS become scarce
          ↓
manufacturing scales
          ↓
ENERGY / GRID / PERMISSIONS become scarce
          ↓
those expand
          ↓
new physical / legal / geological / biological bottleneck
```

That is much stronger than "AI → buy semiconductors."

The Davidson/Halperin/Houlden/Korinek 2026 innovation-network model gives this idea serious theoretical backing: research automation in one sector raises research productivity in other sectors, creating technological and economic feedback loops. Progress therefore cannot be represented as independent industry forecasts. **The hazard rate of a breakthrough in B changes when A gets automated.** ([National Bureau of Economic Research][1])

So our graph needs catalytic edges:

$$
A \rightarrow B
$$

shouldn't merely mean:

> A causes demand for B.

It can mean:

> A increases the *rate at which B itself improves*.

That makes the whole graph dynamic.

---

# 2. The single most interesting alpha I think we were missing: **Jevons paradox for science**

This one now looks extremely important.

Suppose AI reduces the cost of generating a plausible drug molecule by 10,000×.

You do **not** necessarily make biological experimentation 10,000× less valuable.

You may make it vastly **more valuable**, because now there are a million things worth testing.

Likewise:

```text
cheap theorem generation
→ scarce formal verification / expert checking

cheap chip design
→ scarce tape-outs / test / metrology

cheap materials design
→ scarce synthesis + characterization

cheap protein design
→ scarce assays + experimental characterization

cheap quantum-device design
→ scarce cryogenic testing

cheap robot policies
→ scarce physical robot-hours / world interaction
```

The scientific literature is practically screaming this now.

The July 2026 Nature Reviews Chemistry review of self-driving laboratories says the field has advanced from narrow automation toward general discovery platforms, but the next phase depends on **scalability, generalizability and provenance-complete experimentation**. ([Nature][2])

A March 2026 paper describes AI agents actually operating advanced scientific instruments and highlights the operational complexity generated as experimental facilities support more sophisticated workflows. ([Nature][3])

And Nature's new review on AI-designed physics experiments shows AI moving beyond tuning parameters into searching huge spaces of entirely new physical experimental configurations. ([Nature][4])

The implication is:

$$
\boxed{
\frac{\partial \text{demand for physical validation}}
{\partial \text{AI capability}}
>0
}
$$

possibly very strongly.

### This changes our stock search.

Instead of asking:

> Which drug will AI discover?

ask:

> What apparatus must every one of the 50 competing AI-discovered drugs pass through?

Instead of:

> Which quantum modality wins?

ask:

> What test/control/measurement infrastructure gets used by several modalities?

Instead of:

> Which photonic architecture wins?

ask:

> What metrology/testing/alignment/packaging capabilities become unavoidable as photonics gets more complicated?

That is a far better strategy under technological uncertainty.

---

# 3. I would call these **cross-world monopolies**

This deserves to become a formal concept in the kernel.

Imagine ten plausible quantum futures:

```text
superconducting
neutral atom
ion trap
silicon spin
photonic
topological
hybrids...
```

Most investments are conditional:

$$
P(\text{payoff}|\text{one architecture wins})
$$

But there are companies whose demand rises under six or eight futures.

For example, Keysight currently sells both cryogenic/quantum characterization and control infrastructure, while also selling photonic and 224G interconnect validation for AI infrastructure. ([Keysight Technologies][5])

Oxford Instruments supplies cryogenic measurement, magnets and quantum transport instrumentation independently of who ultimately owns the highest-value QPU. ([Oxford Instruments][6])

These are not necessarily cheap stocks today. That's a separate valuation question.

But structurally:

$$
\boxed{
\text{Cross-world exposure}
=
\sum_s P(s)\times \mathbf{1}[\text{needed in state }s]
}
$$

is a fantastic variable.

We should explicitly search for businesses with high **cross-world necessity** and low present-market narrative exposure.

---

# 4. Top alpha extensions I would add to the thesis

Here's my ranking after this research.

| Rank   | Missing alpha                         | Why it is interesting                                                                                     | What the kernel should detect                                                                                      |
| ------ | ------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **1**  | **Experimental scarcity**             | AI generates far more hypotheses/designs than physical systems can validate                               | assay queues, instrument utilization, characterization throughput, lab automation, scientific-equipment lead times |
| **2**  | **Permission scarcity**               | Being technically possible does not mean you can deploy it                                                | grid connections, site control, certifications, permits, spectrum, clinical access, export approvals               |
| **3**  | **Bottleneck migration velocity**     | Consensus discovers today's shortage; alpha lies in tomorrow's shortage                                   | \(d\,scarcity/dt\), capacity additions, substitution rate, lead-time changes                                       |
| **4**  | **Technical-half-life mismatch**      | Assets/accounting assume years of useful economic life while AGI can make architectures obsolete abruptly | depreciation schedules vs predicted technology survival                                                            |
| **5**  | **Cross-world necessities**           | Avoid picking technological winner                                                                        | suppliers necessary across many mutually exclusive scenarios                                                       |
| **6**  | **Real AI usage telemetry**           | Announcements are noise; actual model usage reveals where substitution is occurring                       | tokens/$/agents/tool calls by task mapped to public-company cash flows                                             |
| **7**  | **Three-clock arbitrage**             | capability ≠ adoption ≠ cash flow                                                                         | capability_time, deployment_time, cashflow_time                                                                    |
| **8**  | **Verification economy**              | Generating intelligence becomes cheap; trusted permission to act does not                                 | test, audit, certification, provenance, formal verification                                                        |
| **9**  | **Negative-data moat**                | AI can synthesize text but not recreate every expensive failed physical experiment                        | proprietary failure data, instrument logs, process windows, longitudinal outcomes                                  |
| **10** | **Research-automation multiplier**    | One discovery changes probabilities of other discoveries                                                  | catalytic edges changing downstream breakthrough hazards                                                           |
| **11** | **Market reaction graph**             | Price is itself causal: investors react, then firms react to investors                                    | predictable fund flows, analyst revisions, management capex responses                                              |
| **12** | **Benchmark-to-reality gap**          | AI benchmarks increasingly influence capital but can be optimized/gameable                                | independently replicated real-world capability vs benchmark score                                                  |
| **13** | **Idea-space expansion**              | Convergence catches recombination but not genuinely new technological islands                             | novelty/distance from historical patent/research clusters                                                          |
| **14** | **Threshold cliffs**                  | Demand changes discontinuously when cost/performance crosses an economic threshold                        | robot $/hour, inference $/task, assay $/sample, energy $/MW                                                        |
| **15** | **Capital-cycle inversion**           | Today's bottleneck supplier becomes tomorrow's commodity                                                  | supply response, order cancellation, new capacity, lead-time collapse                                              |
| **16** | **Geographic capability constraints** | AGI is digital but manufacturing, energy and regulation remain local                                      | company × geography × capability × permission                                                                      |
| **17** | **AI-generated cannibalization**      | Firms can benefit from AI while their total revenue pool contracts                                        | productivity growth vs seat count/pricing power                                                                    |
| **18** | **Supply-chain substitutability**     | Centrality alone is useless if alternatives exist                                                         | centrality × indispensability × replacement time × inventory × permissions                                         |

I would concentrate perhaps **80% of our research effort on the first eight**.

---

# 5. Permission scarcity may be even more underpriced than physical scarcity

This surprised me.

Consider AI data centres.

People obsess over:

* GPUs
* HBM
* cooling
* power generation

But something even more primitive exists:

> **permission to connect the load.**

The IEA now estimates more than **2,500 GW** of generation, storage and large-load projects are sitting in grid connection queues globally. Data centres can take around 1–3 years to construct while new grids can take roughly **5–15 years**. ([IEA][7])

The IEA estimates grid constraints could delay roughly **20% of planned global data-centre capacity through 2030**. ([IEA][8])

Transformer and cable procurement has also deteriorated sharply: large transformers can take up to four years and some DC cables beyond five years. ([IEA][9])

But here's the particularly useful alpha.

FERC is now explicitly complaining that speculative data-centre interconnection requests are clogging queues and recommends objective readiness criteria such as **physical site control**. ([Federal Energy Regulatory Commission][10])

So announced:

> "5 GW data-centre pipeline"

is a terrible variable.

We instead want:

$$
\boxed{
\text{Deliverable MW}
=
\text{announced MW}
\times
P(\text{site})
\times
P(\text{interconnect})
\times
P(\text{transformer})
\times
P(\text{generation})
\times
P(\text{permit})
}
$$

That sounds mundane.

It's potentially extremely valuable.

---

# 6. This generalizes far beyond electricity

**Right-to-deploy** might become one of the most important post-AGI assets.

Once intelligence can invent things faster than institutions can validate them:

```text
ability to invent drug           → abundant
FDA/clinical validation          → scarce

ability to design nuclear system → abundant
licensed deployment site         → scarce

AI driving capability            → abundant
certified safe deployment        → scarce

chip designs                     → abundant
fab allocation / export license  → scarce

new data-centre architecture     → abundant
grid connection                  → scarce

autonomous industrial AI         → abundant
safety certification             → scarce
```

And this is already starting in AI itself.

UL Solutions issued its first UL 3115 AI-product certifications in March 2026, evaluating AI-enabled products for robustness, reliability, transparency and other safety properties. ([UL Solutions][11])

UL describes the certification as applicable across software, industrial systems, medical devices, building systems and other AI-enabled physical products. ([UL Solutions][12])

So **UL Solutions itself** is now an interesting post-AGI research candidate—not because it makes AI, but because increasing AI deployment may increase demand for independent permission/trust infrastructure.

This cluster should include things like:

**UL Solutions / Intertek / SGS / Bureau Veritas → AI + robotics + cyber + electrical + autonomous-system certification.**

That's substantially less obvious than "buy Nvidia."

---

# 7. We should distinguish **scarcity** from **scarcity acceleration**

Markets tend to notice a bottleneck once management teams start talking about it.

At that point:

```text
"HBM shortage"
"CoWoS shortage"
"transformer shortage"
```

is already narrative.

What we actually need is:

$$
\boxed{
\frac{dB_i}{dt}
}
$$

where \(B_i\) is bottleneck severity.

And ideally:

$$
\frac{d^2B_i}{dt^2}
$$

because the most interesting moment is when something *starts becoming constrained*.

That means Feedify shouldn't merely ingest mentions.

It should detect:

```text
lead time  8w → 13w → 21w

utilization 61% → 74% → 88%

job vacancies ↑

used-equipment prices ↑

supplier quotes ↑

expedite fees appear

minimum-order quantities ↑

conference researchers complain about access

delivery promises slip

new entrants raise money

customers dual-source

capacity announcements begin
```

That's the fingerprint of a bottleneck **before CNBC calls it one**.

---

# 8. And then the reverse: knowing when to leave the bottleneck

This is equally important.

Bottleneck investing is inherently temporary.

AI demand:

$$
\rightarrow HBM
$$

then Samsung/Micron/SK Hynix invest.

Eventually HBM ceases being marginal.

Scarcity migrates:

$$
HBM
\rightarrow
advanced packaging
\rightarrow
metrology
\rightarrow
CPO
\rightarrow
optical testing
\rightarrow
grid
\rightarrow \ldots
$$

So:

$$
\boxed{
\text{Bottleneck alpha}
=
\text{identify bottleneck}
-
\text{identify supply response}
}
$$

Otherwise we become the people buying shipping stocks at the peak of container rates.

This **bottleneck-release probability** is absent from our current kernel.

It needs:

```text
current_capacity
planned_capacity
time_to_build
supplier_count
substitutability
technological_substitution
customer_inventory
lead_time
backlog
capex_announcements
```

---

# 9. This produces a fascinating hardware concept: the **bottleneck derivative**

Rather than buying "memory" or "photonics," find:

> what becomes constrained **if the currently constrained item succeeds in scaling?**

Example:

```text
HBM shortage solved
↓
more giant AI packages possible
↓
package complexity rises
↓
yield becomes harder
↓
inspection/metrology/test becomes increasingly important
```

That makes metrology a derivative on HBM success.

This is why your prior rabbit holes around **LPKF / Chroma / photonics / packaging** are more interesting to me after this research, not less.

The hidden node is often:

$$
\boxed{
\text{the complement required to unlock the currently obvious bottleneck}
}
$$

rather than the obvious bottleneck itself.

---

# 10. LPKF is a near-perfect example of the *kind* of thing to hunt

Not saying it is necessarily cheap or will win.

But structurally it is beautiful.

LPKF's LIDE technology makes high-aspect-ratio microstructures and through-glass vias in glass for advanced semiconductor packaging, including AI/HPC/chiplet applications. The company says the technology is currently being evaluated by numerous semiconductor customers and it has been discussing initial production systems; it also highlights applications around glass stacks and co-packaged optics. ([LPKF LIDE][13])

Meanwhile LPKF itself remains tiny enough financially that a transition from:

```text
R&D equipment
```

to:

```text
production-critical process equipment
```

could matter enormously to cash flow.

Its 2025 revenue was only about €115 million and adjusted EBIT was barely positive. ([LPKF][14])

That's the shape we want:

$$
\text{small current cashflows}
+
\text{potential critical future node}
$$

rather than:

$$
\text{already \$3T company}
+
\text{obvious AI exposure}
$$

This should become an automated screen.

---

# 11. The analogous "hidden last mile" now exists in co-packaged optics

There is already evidence of this exact bottleneck migration.

As CPO approaches volume deployment, industry reporting increasingly identifies **testing** as a last-mile constraint because electrical and optical components must be characterized together and standards/processes remain immature. ([TrendForce][15])

Keysight is now demonstrating wafer/die-level photonic IC testing and unified electro-optical validation specifically for AI-scale infrastructure. ([Keysight Technologies][16])

So the sequence may be:

```text
electrical links hit power/bandwidth wall
               ↓
CPO becomes attractive
               ↓
CPO integration gets complicated
               ↓
yield/test/alignment becomes bottleneck
               ↓
test-equipment demand explodes
```

Again:

> don't predict whether Broadcom or Nvidia wins CPO.

Find the machine everybody needs when either succeeds.

---

# 12. Quantum has exactly the same structure

We've spent time looking at IONQ / Infleqtion / IQM / QRL.

But the higher-confidence investment abstraction may be **below** them.

Every QPU architecture faces some mix of:

```text
measurement
control
cryogenics
lasers
RF
wafer characterization
packaging
interconnection
error characterization
```

Current research explicitly identifies cryogenic electronics, control wiring and physical integration as significant scaling constraints for several quantum architectures.

Keysight is demonstrating superconducting-qubit control, cryogenic device characterization and quantum EDA. ([Keysight Technologies][5])

Oxford Instruments sells the cryogenic environments and quantum transport measurement infrastructure. ([Oxford Instruments][6])

So I would add a kernel metric:

$$
\boxed{
\text{Architecture-independent quantum exposure}
}
$$

The amazing investment is potentially not:

> the Nvidia of quantum.

It is:

> the ASML / Keysight / Thermo Fisher of *every* plausible quantum computer.

---

# 13. Biology gives us the deepest version of this thesis

This is where the Levin / synthetic cognition work really becomes economically useful.

AI doesn't merely improve prediction.

If biology becomes increasingly **programmable**, the productive substrate itself changes.

The rough progression is:

```text
biology as thing we observe
        ↓
biology as thing we engineer
        ↓
biology as self-assembling factory
        ↓
biology as adaptive controller
        ↓
biology as computational / cognitive substrate
```

Recent synthetic-biology work is already combining AI, automation and closed-loop design-build-test-learn workflows, compressing iteration cycles dramatically. ([Nature][17])

And AI-assisted experimental systems are already discovering gene-editing machinery by combining computational search with high-throughput physical screening. ([Nature][18])

This suggests a major economic inversion.

Today's valuable thing:

> knowing what biological design might work.

Future valuable thing:

> being able to **test, grow, measure, control and manufacture living systems reproducibly**.

So our near-term public-company alpha is probably less:

> bet on "organoid intelligence company X"

and more:

> who owns the increasingly automated biological **I/O layer**?

Liquid handling.

Mass spectrometry.

Sequencing.

Microscopy.

Assays.

Single-cell measurements.

Bioreactors.

Sensors.

Lab robotics.

Sample preparation.

Those are the devices connecting digital intelligence to living matter.

That is an enormous theme.

---

# 14. We should formally call this the **AI-to-atoms interface**

This is one of the cleanest ways I now see to organize your whole post-AGI worldview.

There are three regimes:

```text
DIGITAL
software
models
reasoning
simulation
design

       ↓

INTERFACE
measurement
verification
robotics
instrumentation
controls
sensors
metrology

       ↓

PHYSICAL
atoms
cells
energy
manufacturing
land
materials
biology
```

AGI drives the marginal cost of the top layer toward zero much faster than the bottom.

Therefore the **interface layer** becomes extraordinarily important.

It's where:

$$
\text{bits become atoms}
$$

and:

$$
\text{atoms become trustworthy bits}
$$

Companies living there deserve a whole independent universe in our system.

---

# 15. Real usage telemetry could give us a second completely independent alpha engine

This might be the most directly tradable new data source.

The July 2026 **AI Premium** paper uses **380 trillion actual OpenRouter tokens across 400+ models** and finds a strong relationship between realized AI usage and asset returns. Its value-weighted high-versus-low AI-beta portfolio returned 64.1 bps/week in the studied sample; importantly, the effect was associated more with intensive frontier usage—paying/seasoned users, closed models and long prompts—than casual use. ([National Bureau of Economic Research][19])

This suggests something much richer than their factor.

Don't build one:

```text
AI_usage_factor
```

Build hundreds:

```text
coding_usage
legal_usage
finance_usage
science_usage
customer_support_usage
image_generation_usage
agent_tool_calls
research_usage
browser_agents
data_analysis_usage
voice_agent_usage
```

Then map:

$$
\text{task AI consumption}
\rightarrow
\text{occupational tasks}
\rightarrow
\text{company cost structure}
\rightarrow
\text{competitor substitution}
$$

For example:

```text
agentic coding usage ↑↑↑
        ↓
software engineer productivity ↑
        ↓
outsourced development hours ↓
        ↓
EPAM / Globant-type business-model exposure
```

versus:

```text
scientific AI usage ↑↑↑
        ↓
candidate designs ↑↑↑
        ↓
experimental throughput demand ↑
        ↓
instrument / assay / automation demand
```

Now we have one dataset predicting both **victims and induced bottlenecks**.

That's very strong.

---

# 16. But we must use **actual usage**, not LLM guesses about exposure

Recent work cautions exactly against naïvely asking a model "which jobs are exposed."

Different AI-platform datasets can produce materially different employment exposure estimates; one 2026 study finds platform choice alone can change the estimated post-ChatGPT employment coefficient substantially, and workforce reweighting can shrink estimates dramatically. ([arXiv][20])

Another paper specifically argues that occupational AI exposure should be grounded in external evidence of current capabilities rather than model priors. ([arXiv][21])

And firm-level payments data now show actual substitution: firms more exposed to online contract labor increased AI spending while reducing spending on human marketplaces following ChatGPT's arrival. ([arXiv][22])

So Feedify's role becomes obvious:

$$
\boxed{
\text{observe reality}
>
\text{ask model what reality probably is}
}
$$

The LLM performs inference over the evidence.

It must not *be* the evidence.

---

# 17. The graph needs **three clocks**

This may dramatically improve our forecasts.

Every event should carry:

$$
t_c=\text{capability time}
$$

$$
t_d=\text{deployment time}
$$

$$
t_f=\text{cash-flow time}
$$

Example:

```text
AI can do task            2026
↓
enterprise validates it   2027
↓
workflow redesigned       2028
↓
headcount reduced         2028/29
↓
vendor seat counts fall   2029
```

Financial markets may incorrectly collapse all of those into one date.

Firm data support the distinction. A 2026 NBER study finds AI adoption is increasingly broad, but many adopters still use it in only a handful of business functions and augmentation substantially exceeds outright employment reduction. ([National Bureau of Economic Research][23])

And another 2026 study finds managers **systematically underestimate competitors' AI/robotics adoption**; informing them of competitor adoption raises their own intended robotics investment. ([National Bureau of Economic Research][24])

That's potentially exploitable.

There can be a hidden:

$$
\text{capability} \rightarrow \text{competitive panic} \rightarrow \text{capex}
$$

lag.

---

# 18. Better still: **markets themselves cause the future**

This is a major correction to our original graph.

We had:

```text
world
→ company
→ cashflow
→ stock price
```

But the real system has a feedback edge:

```text
world
→ expectations
→ stock price
→ managerial decision
→ investment
→ future world
```

A new NBER study finds firms actually adjust AI and green-technology investment in response to how the market reacts to their technology announcements, with evidence consistent with managers learning from market prices. ([National Bureau of Economic Research][25])

Therefore:

$$
P(W_{t+1})
=
f(W_t,\mathbf{market\ prices}_t)
$$

Prices aren't merely measurements.

They're causal variables.

That's real Soros-style reflexivity with empirical support.

---

# 19. Which means we need an **actor/reaction graph**

Not everybody sees information simultaneously or reacts identically.

Imagine Astra launches.

```text
frontier researchers understand capability
       ↓ hours

AI-native hedge funds understand economic implication
       ↓ hours/days

sell-side analysts revise models
       ↓ days/weeks

fund managers rebalance
       ↓

company CEOs observe valuation/competitors
       ↓

budgets/capex change
       ↓ quarters

employees/jobs change
       ↓

customer behavior changes
```

Now add a remarkable 2026 result: researchers can predict around **71% of mutual-fund managers' trade directions from their prior behavior**, with some managers approaching near-complete predictability. ([National Bureau of Economic Research][26])

Therefore our system could predict:

$$
\boxed{
\text{not just what information means,
but who will be forced to react next}
}
$$

That's a completely different type of alpha.

---

# 20. AI may accelerate this reaction chain—but not erase it

Evidence from AI hedge funds is illuminating.

AI-driven hedge funds apparently enjoyed material early outperformance, but that advantage declined over time as the technology diffused. ([National Bureau of Economic Research][27])

Meanwhile the Bank of England now explicitly worries that increasingly autonomous AI trading could alter the speed and nature of market adjustments and create correlated behavior; it is building simulated LLM portfolio markets with the BIS through Project Logos. ([Bank of England][28])

So your intuition about reflexivity should become:

$$
\boxed{
\text{AI removes easy informational inefficiencies,
but can create new behavioural/systemic inefficiencies.}
}
$$

It doesn't necessarily produce perfect markets.

It produces different markets.

---

# 21. Another huge thing: **purge predictable news**

Our current Feedify approach asks:

> Is this information high signal?

The new finance literature suggests an even better question:

> **How surprising is this information given everything already known?**

The 2026 NBER paper *The Inefficient Pricing of News* removes the component of news predictable from prevailing company characteristics.

The residual—"pure news"—more than doubles the return-predictive power of raw news and continues predicting returns as far as 18 months in their sample. Negative and quantitative information tends to be underreacted to, while high-attention/ambiguous information can be overreacted to. ([National Bureau of Economic Research][29])

That fits our framework perfectly.

For every new evidence node \(e_t\), calculate:

$$
Surprise(e_t)
=
e_t-E[e_t|W_{t-1}]
$$

Then:

$$
\Delta P(W)
\propto Surprise(e_t)\times Credibility(e_t)
$$

Not:

$$
\Delta P(W)\propto\text{how impressive headline sounds}
$$

This should be a core Feedify/kernel primitive.

---

# 22. Benchmarks should actually get **less** weight now

Another brand-new August 2026 NBER paper, *Benchmark Mineability and the Financing of AI Innovation*, makes an extremely relevant argument: public benchmarks allocate capital, which creates incentives to optimize specifically for them, degrading their information content. ([National Bureau of Economic Research][30])

That's exactly what we need to solve.

Our evidence hierarchy should look approximately:

```text
benchmark score                         low/moderate
private eval reproduced by third party ↑
real economic workflow                  ↑
unstructured novel task                ↑
hours of autonomous operation          ↑
real physical experiment               ↑
customer willingness to pay            ↑
production deployment                  ↑
verified cash-flow impact               highest
```

Call it:

$$
\boxed{\text{Economic Transfer Score}}
$$

A model gaining +12 MMLU-equivalent points matters much less than:

> model ran a laboratory unattended for 48 hours.

Or:

> removed 70% of a department's labor.

Or:

> produced a mathematical result independently verified as correct.

---

# 23. **Negative experimental data** may become an extraordinary moat

Here's another implication I don't think we've emphasized enough.

Suppose all public scientific literature is available to every model.

Then:

$$
\text{published knowledge}
\rightarrow commoditized
$$

But laboratories produce enormous amounts of:

```text
failed conditions
bad parameter combinations
broken reactions
machine drift
weird edge cases
contamination
manufacturing tolerances
process windows
instrument artifacts
```

Most never appears in papers.

Autonomous labs naturally generate this data with perfect provenance.

As experimentation scales, proprietary **failure surfaces** may be far more valuable than successful published experiments.

Thus:

$$
\boxed{
\text{moat} =
\text{unique interaction with reality}
}
$$

rather than:

$$
\text{moat} = \text{documents}
$$

This fits extraordinarily well with the biological cognition / Levin direction: the scarce information is increasingly information generated by interacting with complex physical adaptive systems, not static human text. The self-driving-lab literature's emphasis on provenance-complete experimentation strongly reinforces this. ([Nature][31])

---

# 24. This yields a broader law: **synthetic information loses value; irreducible observations gain value**

AGI can cheaply create:

* prose
* code
* hypotheses
* simulations
* images
* synthetic data
* likely explanations

It cannot cheaply invent a trustworthy measurement of:

* a new material under pressure
* a patient's clinical outcome
* how a turbine actually failed
* a qubit's noise at 20 mK
* an industrial reactor after 40,000 hours
* a newly synthesized organism
* geological structure underground

Thus a useful post-AGI scarcity measure could be:

$$
\boxed{
Irreducibility(x)
=
Cost(\text{obtain genuine observation})
-
Cost(\text{synthetically approximate it})
}
$$

High-irreducibility datasets should become increasingly valuable.

This could be one of the most general laws in the entire thesis.

---

# 25. We should model **technical half-life** just like bond duration

This one could uncover exceptional shorts.

Companies capitalize physical/intangible assets based on assumptions about useful lives.

But suppose AGI-assisted engineering changes architectures so quickly that the *economic* useful life shrinks.

Example:

```text
accounting useful life of data-centre equipment = 5–6 years
predicted technological half-life = 2 years
```

Or:

```text
customer acquisition model assumes SaaS workflow lasts 10 years
agent reproduces workflow next year
```

Define:

$$
H_i^{tech}
=
E[\text{time until productive asset/economic moat becomes obsolete}]
$$

and compare it with:

$$
H_i^{valuation}
$$

Then:

$$
\boxed{
DurationMismatch_i
=
H_i^{valuation}-H_i^{tech}
}
$$

Large positive mismatches are short candidates.

This is **technological-duration arbitrage**.

It may be far richer than simply "which company is obsolete?"

---

# 26. And the AI capex boom creates a giant laboratory for this

Five major US technology companies spent roughly **$380 billion** on capex in 2025 and, according to the June 2026 NBER analysis, were forecast to roughly double that in 2026. ([National Bureau of Economic Research][32])

The Bank of England also notes that AI infrastructure financing has increasingly moved from internal cash flow into debt markets, with hyperscalers becoming major investment-grade issuers. ([Bank of England][28])

So another question becomes:

> **Which assets being financed today have a technological half-life shorter than their financing life?**

That's where technological disruption becomes financial fragility.

This is a very interesting potential short engine.

---

# 27. This is more sophisticated than "AI bubble"

We don't need the AI thesis to be wrong.

The dangerous situation is actually:

$$
\boxed{
AI capability exceeds expectations
}
$$

while:

$$
\boxed{
today's infrastructure architecture becomes obsolete faster than expected
}
$$

You can simultaneously be:

**extremely bullish AGI**

and

**bearish a particular generation of AGI infrastructure.**

That distinction is important.

---

# 28. We should add **threshold cliffs**

Most technological forecasts implicitly assume smooth consequences.

But economics often behaves discontinuously.

For autonomous driving:

$$
Capability = 96\%\rightarrow97\%
$$

might matter little.

Then:

$$
99.999\%
$$

crosses regulatory/safety thresholds and suddenly a driver disappears.

Similarly:

```text
robot cost = $40/hour → niche
robot cost = $18/hour → adoption
robot cost = $4/hour  → enormous substitution

inference = $2/task → human still cheaper
inference = $0.03/task → workflow redesign

assay = $100/sample → scarce
assay = $1/sample → million-experiment biology
```

Therefore the kernel needs cost curves, not merely capability curves.

For every industry:

$$
\boxed{
P(\text{economic threshold crossed by }t)
}
$$

could be more valuable than generic "AI exposure."

---

# 29. This produces a new kind of short: **revenue-per-friction businesses**

A lot of firms make money because something is currently difficult.

Think:

```text
outsourcing
consulting
brokers
manual compliance
document preparation
simple analytics
translation
customer support
routine software configuration
repetitive creative work
```

Their revenue is partly:

$$
Revenue
\approx
Volume\times
\text{friction price}
$$

AGI attacks the friction price.

Even if demand for the underlying activity rises, revenue can collapse.

That's why:

$$
\text{"AI increases usage"}
$$

doesn't automatically mean:

$$
\text{"software revenues rise"}
$$

A system producing 10× more output at 1/100 the cost can annihilate TAM.

This is particularly relevant to per-seat SaaS and human-hour-based services.

---

# 30. The counterintuitive long is **output-priced scarcity**

The mirror image is businesses whose price depends on actual scarce outputs:

* MW delivered
* wafers tested
* samples characterized
* qualified products certified
* transmission connected
* physical goods moved
* assays run
* scarce minerals processed

rather than:

* human hours
* seats
* API abstractions
* information access

This deserves its own factor:

$$
\boxed{PhysicalOutputPricing}
$$

The more the company's economics attach to physically scarce output rather than cognitively scarce labor, the better the structural AGI hedge.

---

# 31. There is also a massive **geographical** layer missing

Post-AGI won't flatten geography.

It may make geography more important.

If intelligence is cheap everywhere, then differences increasingly come from:

```text
energy
land
water
ports
mineral deposits
grid capacity
permitting
regulation
political stability
fabs
labs
logistics
local biological/ecological assets
```

So nodes should no longer merely be:

```text
TSMC
```

They need to become:

```text
TSMC × Taiwan × electricity × water × export policy × fabs × supplier graph
```

Same with data centres:

```text
company × county × substation × queue position × water × fiber
```

Same with biotech:

```text
company × biofoundry × jurisdiction × regulator × trial network
```

The physical world is spatial.

Our graph isn't yet spatial enough.

---

# 32. This gets particularly valuable because supply networks rewire quickly

Firm-level work on supply-chain dynamics finds enormous link turnover; one large VAT-based network study reports roughly 55% of links disappearing annually and a link half-life around 13 months. ([arXiv][33])

So a static "supplier X supplies Y" database is dangerous.

The correct object is:

$$
P(edge_{ij,t+1}|W_t)
$$

And scarcity should incorporate substitution:

$$
Bottleneck_i
=
\frac{
DemandShock_i
\times Centrality_i
\times Indispensability_i
\times TimeToReplace_i
}{
Inventory_i
+
AlternativeCapacity_i
+
Substitutability_i
}
$$

This improves our existing supply-chain kernel considerably.

---

# 33. There is another beautiful consequence: **idea divergence matters as much as convergence**

TechToken focuses on technologies approaching one another.

That's valuable.

But the patent literature also finds the total "idea space" expanding and inventions spreading farther apart.

Therefore there are two different alpha regimes:

### Convergence

```text
AI + biology
silicon + photonics
AI + robotics
quantum + CMOS
```

creates combinations.

### Frontier expansion

Something appears that doesn't fit existing clusters at all.

Those weird new islands can be much more interesting because:

$$
\text{competition}\approx0
$$

initially.

So Feedify should detect:

$$
\boxed{
\text{high semantic novelty}
+
\text{accelerating funding}
+
\text{accelerating experimental evidence}
}
$$

Not merely convergence.

This is where your obsession with obscure researchers with 300 followers is actually structurally useful: early new islands don't yet have the social graph of established disciplines.

---

# 34. We can now define what “high-signal unknown researcher” actually means mathematically

Instead of searching for "smart people," rank:

$$
ResearcherAlpha =
\frac{
Novelty
\times
FutureCentrality
\times
EmpiricalGrounding
\times
LeadTime
}{
AudienceSize^\alpha
}
$$

where:

**Novelty** = semantic distance from consensus.

**FutureCentrality** = whether their idea later becomes connected to many other breakthroughs.

**EmpiricalGrounding** = experiments/data > speculation.

**LeadTime** = how many months/years they precede mainstream recognition.

Then train on history.

Someone repeatedly posting an idea 18 months before patents/citations/funding explode is genuinely useful.

This would be a much better Feedify ranking system than follower count or engagement.

---

# 35. The market-belief side of the kernel also needs expansion

Currently we mostly infer:

$$
P_{\text{market}}(W)
$$

from equity prices.

That's not enough.

We should triangulate world beliefs from:

```text
equities
options
credit
Treasuries/TIPS
prediction markets
capex
VC valuations
commodity forwards
electricity forwards
analyst forecasts
hiring
supplier backlogs
```

Different markets contain different marginal investors.

For AI specifically, frontier-model releases appear to move long-term Treasury/TIPS yields, suggesting even bond markets contain information about transformative-AI expectations.

Prediction markets provide explicit probability distributions.

Options provide distributions under financially consequential positioning.

Capex tells us revealed corporate belief.

Together:

$$
P_{market}(W)
=
Ensemble(
P_{equity},
P_{options},
P_{rates},
P_{prediction},
P_{capex}
)
$$

Disagreement **between markets themselves** may be alpha.

---

# 36. The best signal could be **belief inconsistency**

Suppose:

```text
AI equity valuations imply:
very fast AI progress

hyperscaler capex implies:
very fast AI progress

rates imply:
large productivity acceleration

BUT

Accenture valuation implies:
human consulting cashflows remain intact

Salesforce valuation implies:
seat-based workflow structure remains intact

a specific education stock implies:
human-produced educational scarcity persists
```

There is an internal contradiction.

You don't actually need to decide whether AI equities are correctly priced.

You ask:

$$
\boxed{
\text{Can all these asset prices simultaneously be right?}
}
$$

That's brilliant for the graph.

Call it:

# **World-State Consistency Arbitrage**

Find combinations of securities embedding mutually incompatible futures.

---

# 37. That may be the purest version of your original idea

Instead of asking the LLM:

> predict 2030.

Ask:

> infer the world that each market price requires.

So for each stock:

```text
CRM price requires world W₁
NVDA requires W₂
ACN requires W₃
VRT requires W₄
ULS requires W₅
```

Then test:

$$
W_1\land W_2\land W_3\ldots
$$

for consistency.

If:

> Nvidia's expected earnings require immense autonomous-AI adoption

while:

> a BPO/consulting firm's expected earnings require roughly unchanged human labor demand

then perhaps:

$$
P(W_{NVDA}\cap W_{BPO}) \ll
P_{\text{market implied}}
$$

This doesn't even require us to know the precise future.

We exploit **logical contradictions in market-implied futures**.

I think that is one of the strongest additions from this exercise.

---

# 38. My top five research programs now

If I were deciding what we should actually build next into the system, I would order it:

### **#1 — Scarcity Migration Engine**

For every capability shock:

$$
\text{What becomes abundant?}
\rightarrow
\text{What complement receives induced demand?}
\rightarrow
\text{Can supply respond?}
\rightarrow
\text{What's the next constraint?}
$$

This is the master model.

### **#2 — AI→Atoms Index**

Build a universe specifically around:

**test + measurement + characterization + automation + control + verification + certification.**

Initial names worth deep-diving rather than buying blindly:

**LPKF, Chroma ATE, FormFactor, Keysight, Oxford Instruments, Tecan, KLA, Nova, Camtek, Advantest, Bruker, UL Solutions.**

There will be much smaller weird companies underneath these.

Those are probably where we should go next.

### **#3 — World-State Consistency Arbitrage**

Reverse-DCF thousands of companies.

Extract assumptions about:

* wage growth
* seat counts
* AI usage
* energy
* compute
* productivity
* pricing
* margins
* technological survival

Then find **pairs/clusters whose valuations require contradictory worlds**.

### **#4 — Real Usage → Economic Destruction Graph**

OpenRouter + model/API usage + enterprise app data + job postings + procurement + expense data.

Infer:

```text
actual task automation
→ affected labor pools
→ affected companies
→ induced complement demand
```

The *AI Premium* paper strongly validates real usage as a financially meaningful primitive. ([National Bureau of Economic Research][19])

### **#5 — Technical Half-Life / Obsolescence Short Engine**

Estimate the expected survival of:

```text
business models
physical equipment
software categories
skills
patent portfolios
data assets
```

and compare it with how much duration current valuations embed.

This is directly downstream from the Song Ma result that started us down this path.

---

# 39. And I think Feedify fits underneath all of it

Feedify becomes less like:

> better Twitter/RSS.

And much more like the **sensory nervous system** of the world-state model.

It should maintain feeds such as:

```text
/bottlenecks/experimental-characterization
/bottlenecks/cpo-testing
/bottlenecks/quantum-control
/bottlenecks/grid-permissions
/bottlenecks/transformers

/capabilities/robotics
/capabilities/biological-programming
/capabilities/formal-math

/obsolescence/it-services
/obsolescence/seat-saas
/obsolescence/human-bpo

/worldstate/ai-to-atoms
/worldstate/research-acceleration

/people/frontier-hidden-nodes
```

And every observation becomes a Bayesian update rather than another post in a feed.

That unifies a remarkable amount of what we've been building in the other chats.

---

# 40. The new master equation

I'd now replace the previous simple score with:

$$
\boxed{
Alpha_i=
\sum_{s,t}
\underbrace{
(P_{ours}(s,t)-P_{market}(s,t))
}_{belief\ gap}
\times
\underbrace{
\Delta CF_i(s,t)
}_{cashflow\ effect}
\times
\underbrace{
X_i(s)
}_{cross-world\ exposure}
\times
\underbrace{
B_i(s,t)
}_{scarcity}
\times
\underbrace{
R_i(t)
}_{irreducibility}
-
\underbrace{
C_i(t)
}_{crowdedness}
}
$$

but make bottleneck severity itself endogenous:

$$
B_i
=
\frac{
\text{induced demand}
\times
\text{indispensability}
\times
\text{replacement time}
\times
\text{permission friction}
}{
\text{available capacity}
+
\text{substitutes}
+
\text{inventory}
}
$$

and model:

$$
\frac{dB_i}{dt}
$$

rather than only \(B_i\).

---

## Where I think the genuinely weird alpha lies

The obvious market is still arguing:

> Nvidia vs AMD, OpenAI vs Anthropic, SaaS winner vs loser.

Our better hunting ground is several causal edges away:

> **What obscure physical test, measurement, permission, dataset, process, material or machine becomes indispensable precisely because AI succeeds faster than expected?**

The highest-signal candidate theme from this research is therefore **not "AI stocks."**

It is:

$$
\boxed{
\textbf{the interfaces through which unlimited intelligence collides with limited reality}
}
$$

And within that, I would currently put **experimental validation / metrology / scientific instrumentation first, deployment permissions second, and technical-half-life mismatch third**.

Those three look sufficiently promising that the next research pass should go all the way down to perhaps **100–200 obscure public companies globally under $10B, then score them for cross-world necessity, bottleneck acceleration, valuation convexity and current narrative saturation**. That is where I expect the LPKF-like discoveries to emerge rather than from another screen of conventional AI beneficiaries.

[1]: https://www.nber.org/papers/w35155?utm_source=chatgpt.com "When Does Automating AI Research Produce Explosive Growth? Feedback Loops in Innovation Networks | NBER"
[2]: https://www.nature.com/articles/s41570-026-00847-2?utm_source=chatgpt.com "The past, present and future of self-driving laboratories | Nature Reviews Chemistry"
[3]: https://www.nature.com/articles/s41524-026-02005-0?utm_source=chatgpt.com "Operating advanced scientific instruments with AI agents that learn on the job | npj Computational Materials"
[4]: https://www.nature.com/articles/s41586-026-10898-6?utm_source=chatgpt.com "Designing physics experiments with artificial intelligence | Nature"
[5]: https://www.keysight.com/gb/en/lib/events/seminars/keysight-at-aps-global-physics-summit.html?utm_source=chatgpt.com "Keysight at APS Global Physics Summit 2026 | Keysight"
[6]: https://www.oxinst.com/applications/quantum-measurement?utm_source=chatgpt.com "Quantum Measurement - Oxford Instruments"
[7]: https://www.iea.org/reports/electricity-2026/grids?utm_source=chatgpt.com "Grids – Electricity 2026 – Analysis - IEA"
[8]: https://www.iea.org/reports/energy-and-ai/ai-and-energy-security?utm_source=chatgpt.com "AI and energy security – Energy and AI – Analysis - IEA"
[9]: https://www.iea.org/reports/building-the-future-transmission-grid/executive-summary?utm_source=chatgpt.com "Executive summary – Building the Future Transmission Grid – Analysis - IEA"
[10]: https://www.ferc.gov/news-events/news/commissioner-rosners-remarks-large-load-show-cause-orders-e-7-e-12-june-18-2026?utm_source=chatgpt.com "Commissioner Rosner's Remarks on the Large Load Show Cause Orders, E-7 to E-12 | June 18, 2026 Open Meeting | Federal Energy Regulatory Commission"
[11]: https://www.ul.com/news/ul-solutions-issues-first-certifications-under-ai-safety-testing-service-ai-enabled-products?trk=article-ssr-frontend-pulse_little-text-block&utm_source=chatgpt.com "UL Solutions Issues First Certifications Under AI Safety Testing Service for AI-Enabled Products | UL Solutions"
[12]: https://www.ul.com/services/ul-3115-ai-safety-certification-services-ai-enabled-products?utm_source=chatgpt.com "UL 3115 AI Safety Certification Services for AI-Enabled Products | UL Solutions"
[13]: https://lide.lpkf.com/en/applications/glass-core-substrates?utm_source=chatgpt.com "Glass Core Substrates: TGV Formation & Panel-Level Processing | LPKF"
[14]: https://www.lpkf.com/en/news-press/press-releases-teaser/lpkf-reports-slight-improvement-in-earnings-in-2025-and-initiates-group-realignment?utm_source=chatgpt.com "LPKF reports slight improvement in earnings in 2025 and initiates Group realignment"
[15]: https://www.trendforce.com/presscenter/news/20260727-13151.html?utm_source=chatgpt.com "NVIDIA and Broadcom Begin Volume Ramp of CPO Switches, with Optical Engine Yield and Advanced Packaging Capacity Emerging as Key Expansion Bottlenecks, Says TrendForce"
[16]: https://www.keysight.com/au/en/about/newsroom/catalog/news-release.2026.0309_pr26-045-keysight-showcases-solutions-accelerating-ai-infrastructure-at-ofc-2026.html?utm_source=chatgpt.com "Keysight Showcases Solutions Accelerating AI Infrastructure at OFC 2026 | Keysight"
[17]: https://www.nature.com/articles/s41467-026-77338-x?utm_source=chatgpt.com "Navigating regulatory fragmentation in the convergence of synthetic biology, artificial intelligence, and automation | Nature Communications"
[18]: https://www.nature.com/articles/s41587-026-03273-3?utm_source=chatgpt.com "AI-assisted design of synthetic gene editors | Nature Biotechnology"
[19]: https://www.nber.org/papers/w35451?utm_source=chatgpt.com "AI Premium | NBER"
[20]: https://arxiv.org/abs/2605.21743?utm_source=chatgpt.com "Who Uses AI? Platforms, Workforce, and AI Exposure"
[21]: https://arxiv.org/abs/2605.15474?utm_source=chatgpt.com "Jobs' AI Exposure Should Be Measured from Evidence, Not Model Priors"
[22]: https://arxiv.org/abs/2602.00139?utm_source=chatgpt.com "Payrolls to Prompts: Firm-Level Evidence on the Substitution of Labor for AI"
[23]: https://www.nber.org/papers/w35141?utm_source=chatgpt.com "The Microstructure of AI Diffusion: Evidence from Firms, Business Functions, and Worker Tasks | NBER"
[24]: https://www.nber.org/papers/w34532?utm_source=chatgpt.com "The Innovation Race: Experimental Evidence on Advanced Technologies | NBER"
[25]: https://www.nber.org/papers/w34940?utm_source=chatgpt.com "Market Feedback about Emerging Technologies | NBER"
[26]: https://www.nber.org/papers/w34849?utm_source=chatgpt.com "Mimicking Finance | NBER"
[27]: https://www.nber.org/papers/w35273?utm_source=chatgpt.com "The Growth and Performance of Artificial Intelligence in Asset Management | NBER"
[28]: https://www.bankofengland.co.uk/financial-stability-report/2026/july-2026?utm_source=chatgpt.com "Financial Stability Report - July 2026 | Bank of England – the UK's central bank"
[29]: https://www.nber.org/papers/w35093?utm_source=chatgpt.com "The Inefficient Pricing of News | NBER"
[30]: https://www.nber.org/papers/w35641?utm_source=chatgpt.com "Benchmark Mineability and the Financing of AI Innovation | NBER"
[31]: https://www.nature.com/articles/s44160-026-01120-6?utm_source=chatgpt.com "Self-driving laboratories need an autonomy safety harness | Nature Synthesis"
[32]: https://www.nber.org/papers/w35290?utm_source=chatgpt.com "What Investment Data Implies about the AI Transition | NBER"
[33]: https://arxiv.org/abs/2503.20594?utm_source=chatgpt.com "Supply chain network rewiring dynamics at the firm-level"
