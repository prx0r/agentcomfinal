# PROVENANCE — vendored OpenAI Agents SDK docs

- Source repo: `/home/ubuntu/openai-agents-python` (upstream
  openai/openai-agents-python docs).
- Files: `tracing.md` + `ref/tracing/*` (API reference for the tracing
  subsystem: traces, spans, processors, setup, scope, span data).
- SDK under test: `openai-agents==0.22.2` installed at
  `/home/ubuntu/.venvs/agentcom` (matches `~/acom-openai/requirements.txt`
  pin). System python intentionally does NOT have it: the factory kernel
  stays stdlib-only; the SDK is a live-run dependency only.
- Reference, not fork: implementation adapters live in
  `agentloop/src/loop/tracing.py`. If the SDK moves, re-verify the surface
  (`trace`, `custom_span`, `add_trace_processor`, `TracingProcessor`,
  `BatchTraceProcessor` no-key skip) and update this note.
- Date vendored: 2026-09-14.
