# Architecture

## 1. Candidate Scout
Sources: official MCP Registry, GitHub, owned MCP inventory, maintainer submissions.

For each candidate score 0-5:
- intent frequency
- user value
- externality
- authoritative/live state
- actionability
- verifiability
- chat-native fit
- AI complementarity
- existing MCP quality
- rights clarity
- auth friction (negative)
- safety/liability (negative)
- internalization risk (negative)

The key question is not “is this MCP cool?” but “what user intent inside ChatGPT becomes materially better because this external capability exists?”

## 2. Characterizer
Normalize transport, auth, tools, schemas, annotations, resources, outputs, UI metadata, latency, errors, idempotence and side effects. Prefer existing inspectors/probes rather than new protocol code.

## 3. Gap Mapper
Map each tool to:
```text
capability -> user jobs -> natural utterances -> nearby non-jobs -> native ChatGPT overlap -> plugin gap
```
Use Seesaw reasoning: what changed, what external constraint remains, and can a future model internalize this?

## 4. Pluginizer
Prefer adaptation over rewrite. Starting-point order:
1. official OpenAI Apps SDK example when close;
2. `@modelcontextprotocol/ext-apps` for portable MCP Apps UI;
3. Skybridge or mcp-use when migration/full-stack abstractions help;
4. MCPJam templates for minimal deployment/testing;
5. custom code only for missing delta.

## 5. Routing Lab
Generate: direct positives, indirect positives, paraphrases, underspecified requests, follow-ups, cross-tool cases, cross-app cases, near negatives, native-ChatGPT negatives and adversarial/boundary cases.

Primary metrics:
```text
activation recall
false activation rate
tool precision
argument accuracy
completion rate
clarification quality
retry/idempotency failures
unsafe action rate
latency/widget success
```

## 6. Metadata Hill-Climber
Experiment with app/plugin name, subtitle, tool names, tool descriptions, parameter descriptions and examples. Freeze the eval corpus before comparing variants.

Tool descriptions should express literal behavior and clear “use this when” cues. One user job per tool. Avoid exposing model-visible helper tools.

## 7. Host truth
Evidence ladder:
```text
L0 static schema
L1 MCP conformance
L2 generic agent eval
L3 MCPJam multi-model eval
L4 actual ChatGPT Developer Mode
L5 published-plugin usage
```
Do not call routing “proven” below L4.

## 8. Submission Compiler
Do not recreate OpenAI submission plumbing. Handoff to the official `chatgpt-app-submission` skill/flow after the app is already routing-proven.

## 9. Telemetry
Every production false-negative, false-positive, argument failure, latency issue or host regression becomes a new fixture.
