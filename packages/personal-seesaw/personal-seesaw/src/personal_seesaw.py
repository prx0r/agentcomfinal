#!/usr/bin/env python3
"""Personal Seesaw heuristic scorer. Scores are assumption-forcing, not empirical truth."""
import argparse, json

FIELDS=["future_demand","machine_substitution","chain_closure","human_source_premium","intrinsic_practice_value","ai_complementarity","optionality","asset_compounding","deployment_friction","scenario_robustness","acquisition_cost"]

def clamp(x): return max(0.0,min(5.0,float(x)))

def score(d):
    x={k:clamp(d.get(k,2.5)) for k in FIELDS}
    market=(.24*x["future_demand"]+.18*x["human_source_premium"]+.18*x["ai_complementarity"]+.16*x["asset_compounding"]+.12*x["deployment_friction"]+.12*x["optionality"]-.24*x["machine_substitution"]-.16*x["chain_closure"])
    human=.55*x["intrinsic_practice_value"]+.30*x["human_source_premium"]+.15*x["optionality"]
    future=.55*market+.20*human+.15*x["scenario_robustness"]+.10*x["optionality"]-.20*x["acquisition_cost"]
    score100=max(0,min(100,50+12*future))
    if x["machine_substitution"]>=4 and x["chain_closure"]>=4 and x["asset_compounding"]<=2:
        economic="STOP/WATCH"
    elif x["ai_complementarity"]>=4 and x["asset_compounding"]>=3:
        economic="START/OWN"
    elif x["human_source_premium"]>=4:
        economic="OWN/DIFFERENTIATE"
    else:
        economic="WATCH"
    human_label="PRACTICE" if x["intrinsic_practice_value"]>=4 else "OPTIONAL"
    return {"score_0_100":round(score100,1),"economic_label":economic,"human_label":human_label,"inputs":x}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json")
    a=ap.parse_args()
    if a.json:
        d=json.load(open(a.json))
    else:
        print("Score each field 0..5")
        d={k:float(input(k+": ")) for k in FIELDS}
    print(json.dumps(score(d),indent=2))
if __name__=="__main__": main()
