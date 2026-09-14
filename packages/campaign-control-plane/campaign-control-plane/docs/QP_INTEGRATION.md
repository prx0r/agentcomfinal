
# QP / A-COM integration

Each checkpoint maps naturally onto QP core objects:
- checkpoint claim → CLAIM
- run observations → EVIDENCE
- desired improvement → TASK
- worker attempt → RUN
- validator → GATE
- consequential authority → GRANT
- accepted state change → TransitionReceipt

A checkpoint marked `A` must never directly call the external provider from the worker context. The worker proposes the action; the runtime verifies the grant, injects credential references internally, executes, sanitizes the result and appends evidence. H checkpoints cannot be made autonomous by prompt instruction.
