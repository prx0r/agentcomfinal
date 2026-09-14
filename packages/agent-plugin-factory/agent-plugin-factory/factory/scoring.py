POS=["intent_frequency","user_value","externality","authoritative_state","actionability","verifiability","chat_fit","ai_complementarity","existing_mcp_quality","rights_clarity"]
NEG=["auth_friction","safety_liability","internalization_risk","distribution_ambiguity"]
W={"intent_frequency":1.1,"user_value":1.3,"externality":1.5,"authoritative_state":1.0,"actionability":0.8,"verifiability":0.9,"chat_fit":1.3,"ai_complementarity":1.2,"existing_mcp_quality":1.0,"rights_clarity":1.5,"auth_friction":0.8,"safety_liability":1.2,"internalization_risk":1.5,"distribution_ambiguity":0.6}
def c(v): return max(0,min(5,float(v)))
def score_candidate(x):
 s=x.get("scores",{}); p=sum(W[k]*c(s.get(k,0)) for k in POS)/sum(W[k]*5 for k in POS); n=sum(W[k]*c(s.get(k,0)) for k in NEG)/sum(W[k]*5 for k in NEG); raw=100*max(0,min(1,p*(1-.65*n))); rights=x.get("rights_status","unknown"); gate="BLOCK" if rights=="restricted" else "RIGHTS_REVIEW" if rights=="unknown" else "PLUGINIZE" if raw>=75 else "EVAL_FIRST" if raw>=55 else "SKIP"; return {"score_0_100":round(raw,1),"gate":gate,"positive_normalized":round(p,3),"risk_normalized":round(n,3),"rights_status":rights}
