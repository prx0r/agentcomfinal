"""ab3 gates: chain integrity + stoplight + actuality + readback."""
from ab1 import gates

from . import actuality, alog, readback
from . import stoplight


def _chain(inputs):
    ok = alog.verify_chain(inputs.get("logdir", ""), inputs.get("task", ""))
    return ok, ("chain-ok" if ok else "chain-broken")


def _green(inputs):
    v = inputs.get("judgment", {})
    ok = isinstance(v, dict) and v.get("verdict") == "GO"
    return ok, ("GO" if ok else "NOGO:%s" % ";".join(v.get("reasons", [])))


def _coverage(inputs):
    want = inputs.get("acceptance_n", 0)
    got = sorted(inputs.get("green_idx", []))
    ok = got == list(range(want))
    return ok, ("covered=%s" % got if ok else "uncovered")


def _dag(inputs):
    v = actuality.evaluate_dag(inputs.get("dag", {}))
    ok = v["value"] == "TRUE"
    return ok, ("actuality=%s progress=%d" % (v["value"], v["progress"]))


def _readback(inputs):
    v, detail = readback.check_readback(inputs.get("action", {}),
                                        inputs.get("readback", {}),
                                        inputs.get("key", "created_id"))
    return v == "TRUE", "%s:%s" % (v, detail)


gates.register("alog-chain-intact-v1", "hash chain recomputes", _chain)
gates.register("stoplight-green-v1", "judgment.verdict == GO", _green)
gates.register("alog-coverage-v1", "every acceptance idx green", _coverage)
gates.register("actuality-dag-v1", "AND of leaves, UNKNOWN blocks", _dag)
gates.register("independent-readback-v1", "channels agree, else UNKNOWN",
               _readback)
