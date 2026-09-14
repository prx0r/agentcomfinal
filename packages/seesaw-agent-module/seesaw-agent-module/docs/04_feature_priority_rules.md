# 4. Feature Priority Rules

## 4.1 Fast classifier

Ask these questions for every proposed feature.

### Q1. Does it create/own external state?

Yes strongly → `OWN`

### Q2. Does it control permission to change consequential state?

Yes strongly → `OWN`

### Q3. Does every use generate useful outcome data we can retain?

Yes → likely `OWN` or `BUILD`

### Q4. Is it simply implementing intelligence the model will soon provide?

Yes → `REUSE` or `DROP`

### Q5. Is there a maintained OSS/API implementation?

Yes + low moat → `REUSE`

### Q6. Is the economic thesis uncertain but cheap to test?

Yes → `VALIDATE`

### Q7. Is it strategically interesting but timing uncertain?

Yes → `WATCH`

## 4.2 Examples

| Feature | Action | Why |
|---|---|---|
| Generic email drafting | REUSE | foundation-model commodity |
| Verified domain identity | OWN | authoritative external state |
| Send-as-company authority | OWN | permission boundary |
| Generic call summarization | REUSE | commodity cognition |
| Phone number + call authority | OWN | real communication right |
| Successful-call trajectory store | OWN | proprietary outcomes |
| Generic Shopify listing copy | REUSE | commodity generation |
| Listing/purchase action adapter | BUILD/OWN | action surface |
| Seller conversion history | OWN | proprietary trajectory |
| Generic security scanner UI | REUSE | wrapper |
| Attack/defense outcome corpus | OWN | adversarial proprietary state |
| MCP-to-plugin converter | DROP/REUSE | platform likely commoditizes |
| Real-host plugin routing tests | WATCH/REUSE | useful transitional infra, weak long-term moat |
| Physical installed-base dataset | OWN | hard external observation |
| Generic company enrichment | REUSE | public replicability |
| Verified changing company state | OWN | live authoritative data |

## 4.3 Priority formula

For feature \(f\):

\[
Priority_f =
0.20 ExternalState
+0.18 Authority
+0.18 Trajectories
+0.12 AIComplementarity
+0.10 PhysicalOrNetworkScarcity
+0.08 Trust
+0.08 Verifiability
+0.06 StrategicNecessity
-0.18 LabAttackRisk
-0.12 PublicReplicability
-0.10 MaintenanceCost
\]

Use score to rank, but the action classifier still governs.

## 4.4 Kill condition

Immediately challenge any feature whose rationale contains phrases like:

- "our proprietary prompt";
- "better UI";
- "we use GPT-X";
- "we combine APIs";
- "we have an agent";
- "we route to the right model";
- "our RAG is better";

unless there is a second-order owned scarcity behind it.

