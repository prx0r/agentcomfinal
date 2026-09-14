# Known limitations

1. No natural-language PlanSpec compiler is canonical yet.
2. Real `/gitgoblin` adapter not executed end-to-end in this build environment.
3. Real `/qp` gate registration/receipt settlement not executed end-to-end here.
4. Real `/atask` queue creation/stoplight not executed end-to-end here.
5. QP economic circuit is emitted, not canonically evaluated by Autobuild.
6. Underengineer is deterministic greedy heuristic, not exact global optimization.
7. Legacy shell command evidence should migrate to structured executable/argv/cwd/timeout.
8. Accreted run observations are explicitly UNVERIFIED until an authoritative verifier promotes them.
9. Information-yield scoring is diagnostic only and must never grant authority.
10. Compiler provider should remain replaceable because requirement compilation is already commoditizing.

11. The current generic compiler is a reference implementation; frontier tools such as `agent-spec`, ARC-like compilers, or future lab-native spec compilers should be swappable providers.
12. `command:` evidence is still inherited as a string for A-Task compatibility; canonical future execution specs should prefer executable + argv + cwd + timeout and compile a safe A-Task wrapper.
