"""Policy -> OpenAI Skill: WorkerPolicy versions as deployable objects.

Compiles agent_policy.json (+ rendered AGENTS.md) into a Skill bundle
{SKILL.md, policy.json, resources.json} installable into an agent
environment. Versions compete experimentally (policy-v1 vs v2 vs v3 on
identical ContractRoots) — the Skill is the deployment artifact.
"""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_LOOP = os.path.normpath(os.path.join(_HERE, "..", "..", "..", "..",
                                      "agentcombuild", "agentloop", "src"))
if _LOOP not in sys.path:
    sys.path.insert(0, _LOOP)

from loop import policy as _policy


def build_skill(policy_path=None, domain="business-operator"):
    """Returns {SKILL.md, policy.json, resources.json} strings/dicts."""
    policy_path = policy_path or os.path.normpath(os.path.join(
        _LOOP, "..", "agent_policy.json"))
    with open(policy_path, encoding="utf-8") as fh:
        policy = json.load(fh)
    skill_md = "\n".join([
        "# Skill: %s (%s)" % (domain, policy.get("policy_id", "?")),
        "",
        "Deployable worker policy. Installed into the agent environment;",
        "the agent follows it, QP judges the outcomes.",
        "",
        _policy.render_agents_md(policy),
    ])
    return {"SKILL.md": skill_md, "policy.json": policy,
            "resources.json": {"domain": domain,
                               "escalation": policy.get("research", {}).get(
                                   "escalation", [])}}


def write(skill, root):
    import os as _os
    out = []
    for name, content in skill.items():
        fp = _os.path.join(root, name)
        _os.makedirs(_os.path.dirname(fp) or root, exist_ok=True)
        if isinstance(content, str):
            open(fp, "w").write(content)
        else:
            json.dump(content, open(fp, "w"), indent=2)
        out.append(fp)
    return out
