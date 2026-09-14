# 2. Formal Model

## 2.1 State variables

At time \(t\):

- \(M_t\): machine capability vector.
- \(A_x\): task graph for activity \(x\).
- \(D_x(t)\): demand.
- \(H_x(t)\): effective human supply.
- \(R_x(t)\): motive residual.
- \(P_x(t)\): human-source/provenance premium.
- \(C_x(t)\): AI complementarity.
- \(O_x(t)\): option value and transferability.
- \(K_x(t)\): compounding asset capital created by practice.
- \(L_x\): acquisition cost in time.
- \(F_x(t)\): deployment friction: law, trust, physical integration, liability, access.
- \(Z_s\): technological scenario.

## 2.2 Economic substitutability

For each workflow step \(v\):

\[
a_v(t)\in[0,1]
\]

is machine feasibility including quality, cost, reliability and integration.

For a serial chain:

\[
Chain_x(t)=\prod_{v\in V_x}a_v(t).
\]

For workflows with alternative paths \(p\):

\[
Chain_x(t)=\max_{p\in Paths(x)}\prod_{v\in p}a_v(t).
\]

Adjust for friction:

\[
Auto_x(t)=Chain_x(t)(1-F_x(t)).
\]

This allows discontinuity: improving the final bottleneck from .2 to .9 can matter far more than improving an already automated step from .95 to .99.

## 2.3 Economic scarcity

\[
Supply_x(t)=H_x(t)+\lambda_x(t)M_x(t)
\]

\[
Scarcity_x(t)=\frac{D_x(t)}{Supply_x(t)}
\]

\[
G_x(t)=\frac{d\ln Scarcity_x(t)}{dt}.
\]

## 2.4 Human-source premium

For matched observable quality \(q\):

\[
P_x(t)=
E[WTP_h\mid q]-
E[WTP_m\mid q].
\]

Potential determinants:

\[
P_x=f(
provenance,
relationship,
effort,
embodiment,
scarcity,
status,
ritual,
perceived\ emotional\ involvement,
creator\ biography,
credibility).
\]

Falsifier: if blinded/labeled experiments converge to \(P_x\to0\), do not assume a permanent authenticity moat.

## 2.5 Motive residual

Let motive weights for a person be \(w_j\), \(\sum w_j=1\).

Let activity \(x\) satisfy motive \(j\) by \(u_{xj}\).

Let technology substitute that pathway by \(q_{xj}(t)\).

\[
R_x(t)=\sum_j w_ju_{xj}(1-q_{xj}(t)).
\]

This is why "AI can do it better" is insufficient for personal decisions.

## 2.6 Complementarity

\[
C_x(t)=\frac{\partial V_x}{\partial M_t}.
\]

Practical finite difference:

\[
C_x\approx\frac{V_x(M+\Delta M)-V_x(M)}{\Delta M}.
\]

Positive is desirable.

## 2.7 Asset compounding

Suppose activity \(x\) produces durable asset \(K_x\):

\[
\frac{dK_x}{dt}=g_x(Effort_t,K_x,Network_t,Data_t).
\]

Two people can perform the same work while one builds no persistent asset and the other accumulates reputation, data and distribution.

## 2.8 Future-Adjusted Personal Value

For horizon \(T\), scenario \(s\):

\[
FAPV_x=
\sum_sp_s
\int_0^T e^{-rt}
[
Y_{x,s}
+\alpha R_{x,s}
+\beta P_{x,s}
+\gamma C_{x,s}
+\delta O_{x,s}
+\eta\dot K_{x,s}
]dt
-
Cost_x
-
OC_x.
\]

Where:
- \(Y\): economic return,
- \(R\): nonmarket motive residual,
- \(P\): source premium,
- \(C\): complementarity,
- \(O\): option value,
- \(\dot K\): durable asset creation,
- \(Cost\): direct cost,
- \(OC\): opportunity cost.

This deliberately refuses to reduce a human life to wages.

## 2.9 Economic skill half-life

Define automation hazard:

\[
h_x(t)=
\sigma(
b_0+
b_1Auto_x+
b_2CostAdvantage+
b_3QualityAdvantage+
b_4VerificationEase
-b_5Friction
-b_6HumanPremium
-b_7Complementarity).
\]

Then:

\[
H_x\approx\frac{\ln2}{\bar h_x}.
\]

Learning-risk ratio:

\[
Q_x=\frac{H_x}{L_x}.
\]

Interpretation:
- \(Q<1\): dangerous as economic specialization.
- \(1<Q<3\): transitional.
- \(Q\gg3\): potentially durable.

## 2.10 Compact heuristic score

Score 0–5:
- future demand,
- machine substitution,
- chain closure,
- human-source premium,
- intrinsic practice value,
- AI complementarity,
- optionality,
- asset compounding,
- deployment friction,
- scenario robustness,
- acquisition cost.

Example:

\[
Market=
.24D+.18H+.18C+.16K+.12F+.12O-.24S-.16Chain
\]

\[
Human=.55Intrinsic+.30H+.15O
\]

\[
Future=.55Market+.20Human+.15Robustness+.10O-.20Cost.
\]

Rescale to 0–100.

This is not empirical truth. Its purpose is to force assumptions into a form that can be backtested.

## 2.11 Information-chain confidence

For:

\[
A\rightarrow B\rightarrow C\rightarrow D
\]

\[
P(D)=P(A)P(B|A)P(C|B)P(D|C).
\]

Four 80% links yield:

\[
0.8^4=0.4096.
\]

Therefore aggressive action should require short causal chains or high reversibility.

## 2.12 Real-option rule

Let:
- \(V\): upside,
- \(p\): probability,
- \(c\): cost to establish position,
- \(r\): reversibility,
- \(l\): lead-time advantage.

Prefer early action when:

\[
pV+l>c+(1-r)\cdot downside.
\]

This is why a domain, prototype or 20-hour experiment can be rational under uncertainty while a seven-year credential may not be.

## 2.13 Stop / Start / Own / Practice

### STOP
Economic return is collapsing, human motive is weak, and little durable capital compounds.

### START
Future scarcity/complementarity is rising and lead-time matters.

### OWN
Execution will commoditize but ownership of data, distribution, access, identity, rights or infrastructure stays scarce.

### PRACTICE
Economic scarcity may collapse, but motive residual is high. Do it consciously as art, play, mastery, embodiment or community — not under a false earnings thesis.
