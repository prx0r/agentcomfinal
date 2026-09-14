"""Judges L0/L1: structure check + CEL-subset predicates. Pure, total, boring.

A probe may emit anything; only the judge decides. Judge outputs live in
{TRUE, FALSE, UNKNOWN} — never Boolean. Inadmissible evidence (not an
object, schema-malformed, missing fields, type errors) yields UNKNOWN:
the judge cannot decide, and refusal to decide is never a pass.

L0 (schema-subset): {type, required[], properties{...}, items} over
object/array/string/number/integer/boolean.
L1 (cel-subset): identifiers (dotted paths from `e`), numbers, quoted
strings, true/false, == != < <= > >=, && || !, parens. No arithmetic, no
calls, no assignment: non-Turing-complete by construction, always terminates.
"""
import re

TRUE, FALSE, UNKNOWN = "TRUE", "FALSE", "UNKNOWN"

_TYPES = {"object": dict, "array": list, "string": str, "boolean": bool,
          "number": (int, float), "integer": int}


def check_shape(evidence, schema):
    """L0. Returns (ok, reasons). Non-object evidence is inadmissible."""
    reasons = []

    def walk(ev, sch, path):
        t = sch.get("type")
        if t and t in _TYPES:
            if t == "number":
                good = isinstance(ev, (int, float)) and not isinstance(ev, bool)
            elif t == "integer":
                good = isinstance(ev, int) and not isinstance(ev, bool)
            else:
                good = isinstance(ev, _TYPES[t])
            if not good:
                reasons.append("%s: want %s" % (path or "root", t))
                return
        if isinstance(ev, dict):
            for k in sch.get("required", []):
                if k not in ev:
                    reasons.append("%s: missing %s" % (path or "root", k))
            for k, sub in sch.get("properties", {}).items():
                if k in ev and isinstance(sub, dict):
                    walk(ev[k], sub, "%s.%s" % (path, k) if path else k)
        if isinstance(ev, list) and isinstance(sch.get("items"), dict):
            for i, item in enumerate(ev):
                walk(item, sch["items"], "%s[%d]" % (path, i))

    if not isinstance(schema, dict):
        return False, ["bad-schema"]
    walk(evidence, schema, "")
    return (not reasons), reasons


_TOKEN = re.compile(r"""
    (?P<ws>\s+)
  | (?P<num>-?\d+(?:\.\d+)?)
  | (?P<str>'(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*")
  | (?P<op>&&|\|\||==|!=|<=|>=|<|>|!|\(|\)|\.)
  | (?P<bool>true|false)(?![A-Za-z0-9_])
  | (?P<ident>[A-Za-z_][A-Za-z0-9_]*)
""", re.VERBOSE)


class _CEL(object):
    def __init__(self, text):
        self.toks = []
        pos = 0
        while pos < len(text):
            m = _TOKEN.match(text, pos)
            if not m:
                raise ValueError("lex:%s" % text[pos:pos + 12])
            pos = m.end()
            kind = m.lastgroup
            if kind == "ws":
                continue
            self.toks.append((kind, m.group()))
        self.toks.append(("end", ""))
        self.i = 0

    def peek(self):
        return self.toks[self.i]

    def next(self):
        t = self.toks[self.i]
        self.i += 1
        return t

    def parse(self):
        node = self._or()
        if self.peek()[0] != "end":
            raise ValueError("trailing:%s" % (self.peek()[1],))
        return node

    def _or(self):
        node = self._and()
        while self.peek() == ("op", "||"):
            self.next()
            node = ("or", node, self._and())
        return node

    def _and(self):
        node = self._unary()
        while self.peek() == ("op", "&&"):
            self.next()
            node = ("and", node, self._unary())
        return node

    def _unary(self):
        if self.peek() == ("op", "!"):
            self.next()
            return ("not", self._unary())
        return self._cmp()

    def _cmp(self):
        node = self._operand()
        kind, val = self.peek()
        if kind == "op" and val in ("==", "!=", "<", "<=", ">", ">="):
            self.next()
            return ("cmp", val, node, self._operand())
        return node

    def _operand(self):
        kind, val = self.next()
        if kind == "num":
            return ("lit", float(val) if "." in val else int(val))
        if kind == "str":
            return ("lit", val[1:-1])
        if kind == "bool":
            return ("lit", val == "true")
        if kind == "op" and val == "(":
            node = self._or()
            if self.next() != ("op", ")"):
                raise ValueError("missing )")
            return node
        if kind == "ident":
            parts = [val]
            while self.peek() == ("op", "."):
                self.next()
                k, v = self.next()
                if k != "ident":
                    raise ValueError("path")
                parts.append(v)
            return ("path", parts)
        raise ValueError("operand:%s" % (val,))


class EvalError(Exception):
    pass


def _resolve(env, parts):
    cur = env
    for p in parts:
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            raise EvalError("missing:%s" % ".".join(parts))
    return cur


def _eval(node, env):
    tag = node[0]
    if tag == "lit":
        return node[1]
    if tag == "path":
        return _resolve(env, node[1])
    if tag == "not":
        v = _eval(node[1], env)
        if not isinstance(v, bool):
            raise EvalError("not-nonbool")
        return not v
    if tag in ("and", "or"):
        a = _eval(node[1], env)
        b = _eval(node[2], env)
        if not isinstance(a, bool) or not isinstance(b, bool):
            raise EvalError("logic-nonbool")
        return (a and b) if tag == "and" else (a or b)
    if tag == "cmp":
        _, op, l, r = node
        a, b = _eval(l, env), _eval(r, env)
        try:
            if op == "==":
                return a == b
            if op == "!=":
                return a != b
            if type(a) != type(b) and not (
                    isinstance(a, (int, float))
                    and isinstance(b, (int, float))):
                raise EvalError("cmp-type")
            if op == "<":
                return a < b
            if op == "<=":
                return a <= b
            if op == ">":
                return a > b
            return a >= b
        except TypeError:
            raise EvalError("cmp-type")
    raise EvalError("node")


def eval_cel(expression, evidence):
    """Evaluate a CEL-subset predicate. Returns (bool, None) or raises."""
    return bool(_eval(_CEL(expression).parse(), {"e": evidence}))


def judge_evidence(evidence, spec):
    """Judge one evidence object against a spec.

    spec: {engine: schema|cel, schema?: {...}, expression?: str}.
    Returns (TRUE|FALSE|UNKNOWN, detail). Malformed/failed-eval → UNKNOWN.
    Predicate-false on admissible evidence → FALSE. Nothing else decides.
    """
    if not isinstance(evidence, dict):
        return UNKNOWN, "inadmissible: not an object"
    engine = (spec or {}).get("engine")
    try:
        if engine == "schema":
            ok, reasons = check_shape(evidence, spec.get("schema", {}))
            if ok:
                return TRUE, "shape-ok"
            return UNKNOWN, "malformed:%s" % ";".join(reasons[:3])
        if engine == "cel":
            try:
                return (TRUE, "predicate-true") if eval_cel(
                    spec.get("expression", ""), evidence) else \
                    (FALSE, "predicate-false")
            except (EvalError, ValueError, TypeError, KeyError) as exc:
                return UNKNOWN, "eval-error:%s" % exc
        return UNKNOWN, "unknown-engine:%s" % (engine,)
    except Exception as exc:  # noqa: BLE001 - judges never raise
        return UNKNOWN, "judge-error:%s" % type(exc).__name__
