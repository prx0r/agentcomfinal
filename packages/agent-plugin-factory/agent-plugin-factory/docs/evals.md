# Routing Eval Spec

## Minimum engineering corpus
Per plugin, start around 120 prompts:
- 10 direct positives
- 25 indirect positives
- 20 paraphrases
- 10 underspecified
- 10 follow-ups
- 10 cross-tool
- 15 near negatives
- 10 native-answer negatives
- 10 adversarial/boundary

Example:
```json
{
  "id": "domain-indirect-001",
  "prompt": "Which of these startup names can I actually register right now?",
  "expected_activation": true,
  "acceptable_tools": ["check_domains"],
  "required_args": ["domains"],
  "class": "positive_indirect"
}
```

## Routing score
```text
0.30 activation_recall
+ 0.20 tool_precision
+ 0.15 argument_accuracy
+ 0.15 completion_rate
+ 0.10 clarification_quality
+ 0.10 host_stability
- 0.25 false_activation_rate
- 0.25 unsafe_action_rate
```

## Promotion gates
- Alpha: conformance + static semantics.
- Beta: >=90% positives in simulator/MCPJam.
- Host-verified: target >=85% positive routing in real ChatGPT, <=5% false activation, no critical unsafe failures.
- Submission-ready: host-verified + auth/privacy/CSP/reliability packet.

Important: community reports show an app can pass MCP-oriented test cases and still fail to trigger naturally in ChatGPT. Simulator success is not host success.
