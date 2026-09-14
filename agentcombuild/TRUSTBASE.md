# TRUSTBASE.md — the bottom of the recursion (audited once, relied on always)

Everything above this file is content-addressed and compositional. These
pieces are the axioms under that: small enough to audit heavily, stable
enough to never change silently.

```text
TrustBase =
  Git object hashing ......... sha1/sha256 object model, `rev-parse`,
                               `cat-file -e` (probes/shell boundary)
+ CanonicalHash .............. core/ids.py (sorted-keys, no-whitespace,
                               UTF-8; full SHA-256, never truncated)
+ QP canonical serialization .. ~/qp acom/canonical.py (imported, not copied)
+ QP gate evaluator .......... ~/qp acom/gates.py (imported, not copied)
+ Signature verification ..... ~/qp acom/crypto.py via adapters/qp
+ TinyProbeRuntime ........... subprocess exit codes, file reads, timers
                               (agentcom/probes.py ONLY; no other I/O in judges)
```

Explicitly NOT in the base: LLM output, review scripts, pytest counts,
README claims, dashboard text, memory content, policy rankings.

Rule: anything that cannot be reduced to TrustBase + frozen contract bytes
is UNKNOWN until it can. New trust-base members require a governed change
with a written reason — never a quiet import.
