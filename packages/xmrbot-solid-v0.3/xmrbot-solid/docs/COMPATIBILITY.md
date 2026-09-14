# xmr.computer compatibility

The source of the prior `xmr-computer-mvp` is copied unchanged to `src/xmrcomputer`.

XMRBot imports the prior public models directly:

- `MachineProfile`
- `RandomXNetwork`
- `RandomXAdapter`
- `Scheduler`
- `Policy`

The bridge is `xmrbot.integrations.xmrcomputer.opportunities`.

Compatibility tests verify that XMRBot's direct RandomX production math equals the original xmr.computer formula for the same network and worker hashrate.
