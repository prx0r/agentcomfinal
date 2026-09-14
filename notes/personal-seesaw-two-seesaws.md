---
original_r2_key: "seesawww"
sha12: 1cd25250ffd8
size_bytes: 6967
description: "Personal Seesaw: two seesaws, future-adjusted personal value"
---

I built it as a small research repo rather than a single essay.

[Download `personal-seesaw-v0.1.zip`](sandbox:/mnt/data/personal-seesaw-v0.1.zip)

The central result is stronger than our original “future-adjusted career” formula. **There are really two Seesaws running simultaneously:**

$$
\boxed{
Innovation
\rightarrow
\begin{cases}
\Delta Industry\ Constraints \rightarrow \Delta Shadow\ Prices \rightarrow Capital\\[3pt]
\Delta Human\ Task\ Scarcity \rightarrow \Delta Personal\ Returns \rightarrow Time
\end{cases}}
$$

But the personal branch then splits again:

$$
\text{activity}
=
\text{economic output}
+
\text{instrumental utility}
+
\text{mastery}
+
\text{play}
+
\text{identity}
+
\text{sociality}
+
\text{status}
+
\text{communication}
+
\text{witness}
+
\text{embodiment}
+
\text{meaning}.
$$

That distinction fixes a huge forecasting error. **AI can make something economically obsolete without making the activity humanly obsolete.** Chess is already an almost perfect example: machines annihilated the scarcity of optimal chess calculation while human chess remained valuable as sport, mastery, identity and spectacle. Likewise, industrial machinery devastated the economics of handloom commodity production—the historical evidence Acemoglu reviews shows real handloom-weaver wages more than halved between 1806 and 1820—without making weaving cease to exist as craft. ([National Bureau of Economic Research][1])

The package contains:

* a formal **Future-Adjusted Personal Value** equation incorporating income, intrinsic practice value, human-source premium, AI complementarity, optionality, compounding assets, acquisition cost and opportunity cost;
* a **skill half-life / acquisition-time** test for deciding whether a multi-year learning investment is likely to decay before you harvest it;
* the **positive-AI-beta** criterion, \(\partial V_x/\partial AI>0\), for finding things whose value *increases* as AI improves;
* 10 historical analogues covering handloom weaving, photography, human computers, secretarial work, ATMs, chess, GPS, desktop publishing, arithmetic and media;
* a correction to the Navier–Stokes intuition: it did not supersede mathematicians; the interesting pattern is **epistemic compression**, where a formal representation makes an old layer of heuristic knowledge callable and pushes scarce value upward into new abstractions;
* a Seesaw-compatible JSON event format with explicit `industry` and `person` branches;
* a runnable scoring script and CSV datasets;
* a complete creativity theory and proposed training curriculum;
* falsifiers and experiments, so this can become an actual research program rather than an ideology.

The art point turned out to have unusually strong support. Experiments find that people often appraise the same/controlled artwork more positively when they believe it was human-created, and a 2025 set of three studies found higher purchase intent for human-designed art products, with **perceived emotional involvement statistically mediating that effect**. ([link.springer.com][2]) That doesn't prove a permanent human-art moat—AI-written poetry can already fool people—but it means provenance is demonstrably part of the utility function today.

The model I ended up proposing for creativity is:

$$
\boxed{
Predict
\rightarrow
Observe
\rightarrow
Divergence
\rightarrow
World\ Model\ Update
\rightarrow
Compression
\rightarrow
Transmission
}
$$

More formally, you have some model of yourself/world, predict \(\hat o_t\), encounter \(o_t\), and obtain:

$$
\delta_t=o_t-\hat o_t.
$$

But randomness is not creativity, so weight that divergence:

$$
Salience_t=
|\delta_t|
\times Precision
\times Affect
\times SelfRelevance
\times ExplanatoryReach.
$$

Then the creative act is the compression of a meaningful private update \(\Delta W_c\) into an artifact \(A\) such that another mind can reconstruct some related update:

$$
\Delta W_c
\xrightarrow{Encode}
A
\xrightarrow{Decode}
\widehat{\Delta W_c}.
$$

That gives a surprisingly clean account of your “you are listening for a message” intuition. When you know a song came from a person, it can function partly as **evidence about another finite organism's trajectory through the world**. A machine can synthesize an acoustically superior breakup song, but it is not evidence that the machine had its heart broken. If that evidential/communicative relationship is part of what the listener values, then the two products aren't perfect substitutes.

Predictive-processing researchers have already explored creativity and aesthetics in closely related terms: agents maintain generative world models, predictions meet observations, errors trigger updates, and artistic experiences can involve manipulated expectations and prediction error. ([PubMed Central (PMC)][3]) What I added is the explicit **personal-capital + creativity + Seesaw** synthesis.

The logical extreme is particularly interesting:

$$
AI\ execution \rightarrow \infty
$$

doesn't imply

$$
human\ value \rightarrow 0.
$$

It implies the shadow price migrates.

Generic execution ↓
Novel observation ↑
Real-world ground truth ↑
Human provenance ↑ potentially
Trusted relationships ↑
Physical access ↑
Authority ↑
Taste/selection ↑
Shared cultural events ↑
Unique biography ↑

And this creates a very different theory of education. If AI supplies answers and artifacts cheaply, the thing worth teaching becomes:

$$
\boxed{\text{how to notice what reality does to your model}}
$$

rather than how to reproduce an already-known output.

That is why the creativity tutor in the package **doesn't start with “generate a song.”** It starts with a prediction journal, observations, discrepancy detection, recurring-divergence graph, analogical transfer and audience decoding. A JEPA-like system could eventually learn a person's longitudinal world-model trajectory and surface places where reality repeatedly violates their expectations—without replacing the human as the source of the experience.

And the strongest Personal Seesaw rule I got from the whole exercise is:

$$
\boxed{
\text{Do not become better at an output that is becoming abundant.}
}
$$

unless you consciously value the practice itself.

For economic effort:

$$
\boxed{
\text{Own or become the new bottleneck created when the old bottleneck disappears.}
}
$$

That is the same causal logic as Seesaw, applied to the allocation of a human lifetime.

[1]: https://www.nber.org/system/files/working_papers/w32416/w32416.pdf?utm_source=chatgpt.com "Learning from Ricardo and Thompson"
[2]: https://link.springer.com/article/10.1186/s41235-023-00499-6 "Humans versus AI: whether and why we prefer human-created compared to AI-created artwork | Cognitive Research: Principles and Implications | Springer Nature Link"
[3]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10725762/ "Cultivating creativity: predictive brains and the enlightened room problem - PMC"
