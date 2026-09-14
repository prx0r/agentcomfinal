
def score(receipt, cost=None, duration=None):
    if receipt.get('result')!='PASS': return 0.0
    base=1.0
    # Cost/time only rank successful variants; they can never compensate for failure.
    penalty=0.0
    if cost is not None: penalty += min(float(cost),1.0)*0.05
    if duration is not None: penalty += min(float(duration)/3600.0,1.0)*0.05
    return max(0.9, base-penalty)
