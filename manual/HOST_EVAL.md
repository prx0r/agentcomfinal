# HOST EVAL — manual evidence slots (DO NOT fabricate)

These two leaves can only be established by a human with a real ChatGPT
workspace. A local process MUST leave them UNKNOWN. When performed, paste
the evidence (date, workspace id, screenshots hashes, quoted tool call)
below and re-run the DAG evaluation with `--manual evidence.json`.

## host-install (UNKNOWN)

- [ ] Import `dist/plugins/agentcom-uk/catalog.json` as a workspace marketplace
- [ ] Install the `agentcom-uk-business-profile` plugin
- Evidence: ...

## host-invocation (UNKNOWN)

- [ ] Ask: "Show me this UK business." (acme-plumbing-leeds)
- [ ] Confirm ChatGPT called `business.lookup` (not a confabulated answer)
- [ ] Confirm the rendered result matches the fixture profile
- Evidence: ...
