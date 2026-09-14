# Monero.Jobs

- ID: `monerojobs`
- Canonical URL: https://monero.jobs/
- Categories: labor, jobs, freelance
- Agentability: 0.58
- Status: active

## Capabilities

### `browse_jobs`
- class: `discover`
- mode: `read_only_web`
- state-changing: `false`
- requires grant: `false`
- description: Browse current XMR-denominated jobs.

### `hire_proposal`
- class: `propose`
- mode: `manual_bridge`
- state-changing: `true`
- requires grant: `true`
- description: Prepare a job post or freelancer contact proposal.

### `work_proposal`
- class: `propose`
- mode: `manual_bridge`
- state-changing: `true`
- requires grant: `true`
- description: Prepare an application/bid proposal.

## Privacy notes

- Platform advertises no KYC, anonymous proposals and zero platform fees.

## Sources

- https://monero.jobs/
- https://monero.jobs/jobs
