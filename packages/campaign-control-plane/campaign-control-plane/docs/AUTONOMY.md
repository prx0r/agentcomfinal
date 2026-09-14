
# Autonomy frontier

Do not maximize autonomous task count. Optimize:

`VerifiedProgress / (HumanMinutes + λ·Cost + μ·Risk + ν·Latency)`

Task classes:
- **M-task:** deterministic policy permits autonomous execution.
- **H-task:** real human action/judgment is required; agent cannot bypass it.
- **A-task:** consequential machine action requiring explicit authority/grant.

Agent confidence is an input to routing, never a substitute for validation. A high-confidence worker may be allowed to attempt more cheaply, but the same gate decides success.

The human’s strategic job is to eliminate recurring blocker classes. If five projects repeatedly need the same OAuth/KYC/social-publishing intervention, that becomes a meta-bottleneck campaign rather than five manual chores.
