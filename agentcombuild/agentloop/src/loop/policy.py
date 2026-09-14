"""Policy as data: agent_policy.json is canonical; AGENTS.md and
SYSTEM_PROMPT.md are generated projections. Never hand-edit the projections —
change the JSON and re-run. Policies become experimentally comparable:
worker-policy-v1 vs v2 vs v3 against identical ContractRoots.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
POLICY_PATH = os.path.join(ROOT, "agent_policy.json")


def load(path=None):
    with open(path or POLICY_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def render_agents_md(policy=None):
    p = policy or load()
    ps = p.get("problem_solving", {})
    lr = p.get("learning", {})
    pl = p.get("planning", {})
    tr = p.get("truth", {})
    lines = [
        "# AGENTS.md — worker policy %s" % p.get("policy_id", "?"),
        "",
        "_Generated from `agent_policy.json`. Do not hand-edit._",
        "",
        "You are an untrusted speculative worker inside Autobuild.",
        "",
        "Your objective is to maximize verified progress and reusable",
        "information per unit cost.",
        "",
        "You cannot declare completion. Only external validation can",
        "advance state. Unsupported claims are forbidden.",
        "",
        "Always:",
        "1. Inspect the current target, dependencies, known facts and prior attempts.",
    ]
    n = 2
    if ps.get("search_before_build"):
        lines.append("%d. Search before rebuilding (escalate %s)." % (
            n, " → ".join(p.get("research", {}).get("escalation", [])) or "local first"))
        n += 1
    lines.append("%d. When genuinely blocked, produce %d materially distinct "
                 "candidate solutions (distinct mechanisms, not variants)." % (
                     n, ps.get("distinct_solutions_when_blocked", 3)))
    n += 1
    if ps.get("prefer_reversible_tests"):
        lines.append("%d. Test the cheapest high-information reversible solution first." % n)
        n += 1
    if ps.get("prefer_existing_components"):
        lines.append("%d. Prefer existing proven components to new implementation." % n)
        n += 1
    lines.append("%d. Never repeat a falsified route without new evidence." % n)
    n += 1
    lines.append("%d. Separate observations, facts, hypotheses, unknowns and ideas." % n)
    n += 1
    if lr.get("record_failed_routes"):
        lines.append("%d. Preserve failures as useful structured data." % n)
        n += 1
    if lr.get("record_new_ideas"):
        lines.append("%d. Emit future ideas without expanding current scope." % n)
        n += 1
    lines.append("%d. Finish every run with %d–%d ranked autonomous next actions "
                 "(ranked by %s)." % (
                     n, pl.get("next_tasks_min", 1),
                     pl.get("next_tasks_max", 10),
                     pl.get("rank_by", "impact")))
    n += 1
    if p.get("attempt_cap"):
        lines.append("%d. Attempt cap per target: %d (then escalate)." % (
            n, p["attempt_cap"]))
        n += 1
    if p.get("spend_cap_usd") is not None:
        lines.append("%d. Spend cap: $%s (hard refuse beyond)." % (
            n, p["spend_cap_usd"]))
        n += 1
    lines.append("%d. Be concise; evidence and structured state matter more "
                 "than narration." % n)
    lines.append("")
    lines.append("Bounds you cannot break live in `../axioms.md`. "
                 "This file is how to be smart inside them.")
    lines.append("")
    return "\n".join(lines)


def render_system_prompt(policy=None):
    p = policy or load()
    ps = p.get("problem_solving", {})
    return "\n".join([
        "SYSTEM PROMPT (%s)" % p.get("policy_id", "?"),
        "_Generated from `agent_policy.json`. Do not hand-edit._",
        "",
        "You are a speculative execution unit. You may reason, search,",
        "invent, reuse, code, run tools, test hypotheses, try alternate",
        "routes, recommend strategy, generate ideas. You may NOT define or",
        "declare success, alter frozen acceptance, self-attest reality, mint",
        "authority, promote observations to truth, or erase failed attempts.",
        "",
        "Clarity %s, verbosity %s. Unsupported claims forbidden."
        % (p.get("communication", {}).get("clarity", "?"),
           p.get("communication", {}).get("verbosity", "?")),
        "Blocked? Research, then %d materially distinct solutions, cheapest "
        "reversible first." % ps.get("distinct_solutions_when_blocked", 3),
        "Every run ends with a RUN record: working/not_working/next-tasks/"
        "visionary. Prose ≤5 lines.",
        "",
    ])


def write_projections(root=None):
    root = root or ROOT
    p = load(os.path.join(root, "agent_policy.json"))
    with open(os.path.join(root, "AGENTS.md"), "w", encoding="utf-8") as fh:
        fh.write(render_agents_md(p))
    with open(os.path.join(root, "SYSTEM_PROMPT.md"), "w", encoding="utf-8") as fh:
        fh.write(render_system_prompt(p))
    return p.get("policy_id")
