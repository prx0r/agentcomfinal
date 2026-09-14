# Upstream component map

## Official / normative
- openai/openai-apps-sdk-examples — canonical ChatGPT example patterns
- openai/skills `chatgpt-apps` — docs-first build workflow
- openai/plugins `chatgpt-app-submission` — submission import JSON + review tests
- modelcontextprotocol/ext-apps — portable MCP Apps UI spec/SDK
- modelcontextprotocol/registry — official public MCP candidate feed

## Frameworks / conversion
- alpic-ai/skybridge — full-stack MCP/ChatGPT Apps framework; migration skills
- mcp-use/mcp-use — framework, views, inspector, tunnel, deploy/eval tooling
- basementstudio/xmcp — TypeScript MCP framework

## Test / eval / conformance
- MCPJam/inspector — ChatGPT/MCP app emulator, traces, OAuth, evals, CLI, CI
- Roee-Tsur/mcp-spec-check — black-box MCP readiness/conformance
- lastmile-ai/mcp-eval — end-to-end MCP agent evals
- deeppavlov/mcp-evals — code-first objective tool-use evals
- eval-sys/mcpmark — realistic MCP benchmark design

## Templates
- MCPJam/chatgpt-app-template
- MCPJam/mcp-app-workers-template
- MCPJam/apps-sdk-everything

## Telemetry
- Roee-Tsur/mcp-signal — widget analytics/telemetry across sandbox constraints

## Principle
Integrate healthy upstream components; pin versions and write adapters. Build only the scoring ontology, normalized evidence store, routing corpus generator, metadata experiment loop, real-host result importer and longitudinal outcome dataset.
