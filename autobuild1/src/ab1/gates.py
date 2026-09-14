"""Gate registry: id -> pure predicate. Unknown = FAIL, raise = FAIL."""
import hashlib

REGISTRY = {}


def register(gid, source, fn):
    REGISTRY[gid] = {"source": source, "fn": fn}


def program_hash(gid):
    return hashlib.sha256(REGISTRY[gid]["source"].encode("utf-8")).hexdigest()


def execute(gid, inputs):
    g = REGISTRY.get(gid)
    if g is None:
        return {"id": gid, "inputs": inputs, "verdict": "FAIL",
                "proof": "unknown-gate"}
    try:
        ok, proof = g["fn"](inputs)
    except Exception as exc:  # noqa: BLE001 - fail closed by design
        return {"id": gid, "inputs": inputs, "verdict": "FAIL",
                "proof": "raised:%s" % type(exc).__name__}
    return {"id": gid, "inputs": inputs,
            "verdict": "PASS" if ok else "FAIL", "proof": proof}


def _specgate(inputs):
    v = inputs.get("spec_verdict", {})
    return bool(v.get("ok")), "errors=%d" % len(v.get("errors", []))


def _evidence_declared(inputs):
    bad = []
    for f in inputs.get("features", []):
        ev = f.get("evidence", [])
        if not [e for e in ev if isinstance(e, dict) and e.get("kind")
                and e.get("ref")]:
            bad.append(f.get("id", "?"))
    return (not bad), ("all-declared" if not bad else "missing:" + ",".join(bad))


def _two_sources(inputs):
    srcs = {s.get("id") for s in inputs.get("sources", [])
            if isinstance(s, dict) and s.get("id")}
    return len(srcs) >= 2, "distinct=%d" % len(srcs)


def _threshold(inputs):
    v = float(inputs.get("value", 0))
    m = float(inputs.get("min", 0))
    return v >= m, "value=%s min=%s" % (v, m)


def _no_duplicate(inputs):
    items = inputs.get("items", [])
    return len(items) == len(set(items)), "n=%d unique=%d" % (
        len(items), len(set(items)))


register("specgate-v1", "spec_verdict.ok", _specgate)
register("evidence-declared-v1", "every feature has kind+ref evidence",
         _evidence_declared)
register("two-sources-v1", ">=2 distinct source ids", _two_sources)
register("score-threshold-v1", "value >= min", _threshold)
register("no-duplicate-v1", "ids unique", _no_duplicate)
