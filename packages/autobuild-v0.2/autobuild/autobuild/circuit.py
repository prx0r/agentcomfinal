"""Small bool3 target-circuit evaluator.

This is a specification-side evaluator, not a replacement for QP's canonical
circuit runtime. It lets autobuild deterministically validate completion
expressions before emitting a QP bridge.
"""
from .tristate import TRUE,FALSE,UNKNOWN,tri_and,tri_or

OPS={"AND","OR","NOT","REF","CONST"}

def evaluate(node,states):
    op=node.get("op")
    if op=="CONST":
        v=node.get("value"); return v if v in {TRUE,FALSE,UNKNOWN} else UNKNOWN
    if op=="REF":return states.get(node.get("id"),UNKNOWN)
    if op=="AND":return tri_and(evaluate(x,states) for x in node.get("args",[]))
    if op=="OR":return tri_or(evaluate(x,states) for x in node.get("args",[]))
    if op=="NOT":
        v=evaluate(node.get("arg",{}),states)
        return FALSE if v==TRUE else TRUE if v==FALSE else UNKNOWN
    raise ValueError(f"unknown circuit op: {op}")

def refs(node):
    op=node.get("op")
    if op=="REF":return {node.get("id")}
    if op in {"AND","OR"}:
        out=set()
        for x in node.get("args",[]):out |= refs(x)
        return out
    if op=="NOT":return refs(node.get("arg",{}))
    if op=="CONST":return set()
    raise ValueError(f"unknown circuit op: {op}")

def all_of(ids):
    return {"op":"AND","args":[{"op":"REF","id":x} for x in ids]}
