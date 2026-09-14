# Portfolio scheduler

The scheduler exists because autonomous build capacity is cheap but external experiment capacity is not.

## Lanes

- `FAST_TRUTH` — many preregistered market hypotheses can resolve in parallel.
- `FAST_DEMAND` — cheap app/tool probes, constrained by primary distribution surfaces.
- `ECONOMIC` — money/sell-through tests, constrained by stores/accounts/budget.
- `DEEP_SCARCE_STATE` — business permissions, physical data, network formation.

## Resource model

Resources are explicit records with capacity and parallelism. Examples:
- one Etsy store;
- one primary ChatGPT app account;
- one initial business-permission slot;
- human sales/relationship attention;
- physical observation capacity.

The system may run unlimited-looking software simulations only where actual compute capacity permits. It may not infer that external accounts/permissions are equally parallel.

## Scheduling rule

1. generate live experiment proposals from projects;
2. score each project's scarce-state priority and selected world's information value;
3. allocate higher-value proposals first;
4. refuse resource collisions;
5. run simulation preflight in parallel;
6. after real outcomes, update strategy evidence and reschedule.

Infrastructure is never granted a roadmap simply because it is useful. Selected experiments pull only the infrastructure they require.
