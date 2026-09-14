"""Promotion gate for turning local observations into reusable primitives.
Count alone is never sufficient."""

def assess_promotion(project_uses, replay_results, minimum_uses=3, min_pass_rate=0.90, max_regressions=0):
    uses=sorted(set(project_uses))
    total=len(replay_results)
    passes=sum(1 for r in replay_results if r.get("pass") is True)
    regressions=sum(1 for r in replay_results if r.get("regression") is True)
    pass_rate=passes/total if total else 0.0
    failures=[]
    if len(uses)<minimum_uses: failures.append(f"uses {len(uses)} < {minimum_uses}")
    if total==0: failures.append("no held-out replay results")
    if pass_rate<min_pass_rate: failures.append(f"held-out pass_rate {pass_rate:.3f} < {min_pass_rate:.3f}")
    if regressions>max_regressions: failures.append(f"regressions {regressions} > {max_regressions}")
    return {"gate_id":"primitive-promotion-v1","result":"PASS" if not failures else "FAIL","unique_project_uses":uses,"heldout_cases":total,"heldout_pass_rate":round(pass_rate,6),"regressions":regressions,"failures":failures}
