"""Static validation for the QP/killfeed circuit data dialect.
Autobuild does not evaluate economic circuits canonically; /qp does."""
BOOL_OPS={"AND","OR","NOT","IF","EQ","GT","GTE","LT","LTE","IS_UNKNOWN"}
ARITH_OPS={"MUL","ADD","SUB","DIV"}
SPECIAL_OPS={"LOW","HIGH","COUNT","FRESH","TREND_UP","TREND_DOWN","CHANGED_BY","CHANGED_WITHIN","TRUE_FOR"}
OPS=BOOL_OPS|ARITH_OPS|SPECIAL_OPS


def validate(node,path="$",failures=None):
    failures=[] if failures is None else failures
    if not isinstance(node,dict):
        failures.append(f"{path}: node must be object"); return failures
    leaves=[k for k in ("const","metric","claim","param") if k in node]
    if leaves:
        if len(leaves)!=1 or "op" in node:
            failures.append(f"{path}: leaf must have exactly one of const/metric/claim/param and no op")
        return failures
    op=node.get("op")
    if op not in OPS:
        failures.append(f"{path}: unknown QP circuit op {op!r}"); return failures
    if op in {"AND","OR"}:
        args=node.get("args")
        if not isinstance(args,list) or not args: failures.append(f"{path}: {op} requires non-empty args")
        else:
            for i,a in enumerate(args):validate(a,f"{path}.args[{i}]",failures)
    elif op in {"NOT","IS_UNKNOWN"}:
        args=node.get("args")
        if not isinstance(args,list) or len(args)!=1: failures.append(f"{path}: {op} requires exactly 1 arg")
        else:validate(args[0],f"{path}.args[0]",failures)
    elif op=="IF":
        args=node.get("args")
        if not isinstance(args,list) or len(args)!=3: failures.append(f"{path}: IF requires exactly 3 args")
        else:
            for i,a in enumerate(args):validate(a,f"{path}.args[{i}]",failures)
    elif op in {"EQ","GT","GTE","LT","LTE","MUL","ADD","SUB","DIV"}:
        args=node.get("args")
        if not isinstance(args,list) or len(args)!=2: failures.append(f"{path}: {op} requires exactly 2 args")
        else:
            for i,a in enumerate(args):validate(a,f"{path}.args[{i}]",failures)
    elif op in {"LOW","HIGH","TREND_UP","TREND_DOWN","CHANGED_BY"}:
        if not isinstance(node.get("metric"),str) or not node.get("metric"):failures.append(f"{path}: {op} requires metric")
    elif op=="COUNT":
        if not isinstance(node.get("metrics"),list) or not node.get("metrics"):failures.append(f"{path}: COUNT requires metrics")
    elif op=="FRESH":
        if not (node.get("metric") or node.get("metrics")):failures.append(f"{path}: FRESH requires metric or metrics")
    elif op in {"CHANGED_WITHIN","TRUE_FOR"}:
        if not isinstance(node.get("predicate"),str) or not node.get("predicate"):failures.append(f"{path}: {op} requires predicate")
    return failures


def metric_refs(node):
    if not isinstance(node,dict):return set()
    out=set()
    if isinstance(node.get("metric"),str):out.add(node["metric"])
    if isinstance(node.get("metrics"),list):out|={x for x in node["metrics"] if isinstance(x,str)}
    for a in node.get("args",[]) if isinstance(node.get("args"),list) else []:out|=metric_refs(a)
    return out
