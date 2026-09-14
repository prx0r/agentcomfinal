# Plugin Factory Integration

The previous plugin-factory work should become an **adapter/instrument**, not the moat.

Seesaw can consume plugin-factory observations:

```text
plugin_gap
routing_failure
tool_use
submission result
usage
revenue
```

But it should score the **backend capability**.

Suggested pipeline:

```text
Plugin candidate
    |
    v
Seesaw
    |
    +-- external-state strong? -> proceed
    +-- pure wrapper?          -> skip/reuse
    |
    v
Plugin factory
    |
    v
distribution adapter
    |
    v
real usage/outcomes
    |
    v
Seesaw trajectory store
```

Long-term:

```text
Seesaw decides WHAT scarce capability to own.
Plugin factory decides HOW to expose it.
```

If OpenAI makes pluginization one-click, delete the plugin-factory implementation layer without harming Seesaw.
