"""BusinessBundle compiler: BusinessSpec -> deployment bundle (pure data).

Not Plan->Python. A bundle is the compiled deployment target an Agents API
session boots from: lineage-bound agent instructions, skills, MCP wiring,
voice/security/telemetry/evals. Writing files is the caller's choice;
build() returns the tree so tests never touch disk.
"""
import copy

LAYOUT = ("strategic.json", "contract.json", "actuality.json",
          "agent/instructions.md", "agent/agent.json",
          "agent/environment.json", "mcp/company-state.json",
          "mcp/gitgoblin.json", "mcp/qp-gateway.json",
          "plugin/app.json", "plugin/directory.json",
          "voice/persona.json", "voice/call-policy.json",
          "voice/escalation.json", "security/tool-policy.json",
          "security/data-policy.json", "security/grants.json",
          "telemetry/events.schema.json", "telemetry/retention.json",
          "evals/actuality.json")


def _instructions(spec):
    return "\n".join([
        "You are executing ContractRoot %s." % spec.get("contract_root", "?"),
        "",
        "Project: %s. Campaign: %s." % (spec.get("project", "?"),
                                        spec.get("campaign", "?")),
        "",
        "Work only on READY requirements.",
        "",
        "Use available skills/tools.",
        "",
        "When blocked, research and try alternate routes.",
        "",
        "You cannot decide whether a requirement is complete.",
        "Completion is external.",
        "",
    ])


def build(spec):
    """spec: BusinessSpec dict (see examples/lead_business.json). Returns
    {path: content-str}. Raises ValueError on missing contract lineage."""
    spec = copy.deepcopy(spec or {})
    for k in ("project", "campaign", "contract_root", "capabilities"):
        if not spec.get(k):
            raise ValueError("spec missing:%s" % k)
    tree = {
        "strategic.json": {"project": spec["project"],
                           "goals": spec.get("goals", [])},
        "contract.json": {"contract_root": spec["contract_root"],
                          "claim": spec.get("claim", ""),
                          "leaves": spec.get("actuality_leaves", [])},
        "actuality.json": {"leaves": spec.get("actuality_leaves", []),
                           "proof_class": "external_readback"},
        "agent/instructions.md": _instructions(spec),
        "agent/agent.json": {"model": spec.get("model", "gpt-6-astra"),
                             "policy": spec.get("policy_id",
                                                "autobuild-worker-v1")},
        "agent/environment.json": {"template": spec.get("environment", {}),
                                   "metadata": {
                                       "project": spec.get("project"),
                                       "campaign": spec.get("campaign"),
                                       "contract": spec.get("contract_root"),
                                       "plan": spec.get("plan_root", ""),
                                       "policy": spec.get("policy_id",
                                                          "autobuild-worker-v1")}},
        "mcp/company-state.json": {"server": "company-mcp",
                                   "tools": ["company.lookup"]},
        "mcp/gitgoblin.json": {"server": "gitgoblin-mcp",
                               "tools": ["search_entities"]},
        "mcp/qp-gateway.json": {"server": "qp-gateway",
                                "tools": ["qp.authorize", "qp.verify"],
                                "enforces": "independent"},
        "plugin/app.json": {"surfaces": ["chatgpt", "codex"],
                            "from_mcp": True},
        "plugin/directory.json": {"listing": spec.get("project")},
        "voice/persona.json": spec.get("voice", {}).get("persona", {}),
        "voice/call-policy.json": spec.get("voice", {}).get("call_policy",
                                                             {}),
        "voice/escalation.json": spec.get("voice", {}).get("escalation",
                                                            {"human": True}),
        "security/tool-policy.json": {"approval": "first-belt",
                                      "authority": "qp-only"},
        "security/data-policy.json": {"raw_audio": "OFF",
                                      "sensitive_text": "OFF",
                                      "store": "policy-dependent"},
        "security/grants.json": spec.get("authority", {}),
        "telemetry/events.schema.json": {"source": "openai.agents",
                                         "normalized": True},
        "telemetry/retention.json": spec.get("retention",
                                             {"default_days": 90}),
        "evals/actuality.json": {"leaves": spec.get("actuality_leaves", [])},
    }
    skills = {"business-operator": {"from": "agent_policy.json"}}
    for name in spec.get("skills", []):
        skills[name] = {"domain": name}
    tree["skills"] = skills
    return tree


def write(tree, root):
    """Materialize a built tree under root/. Returns [paths]."""
    import json as _json
    import os as _os
    out = []
    for path, content in tree.items():
        if path == "skills":
            for name, sk in content.items():
                fp = _os.path.join(root, "skills", name, "skill.json")
                _os.makedirs(_os.path.dirname(fp), exist_ok=True)
                _json.dump(sk, open(fp, "w"), indent=2)
                out.append(fp)
            continue
        fp = _os.path.join(root, path)
        _os.makedirs(_os.path.dirname(fp) or root, exist_ok=True)
        if isinstance(content, str):
            open(fp, "w").write(content)
        else:
            _json.dump(content, open(fp, "w"), indent=2)
        out.append(fp)
    return out
