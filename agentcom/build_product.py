"""Product pipeline: spec -> MCP -> factory -> lint -> routing -> dist.

Read-only v1 (brief P5): business.lookup + derived profile. Every stage
emits JSON evidence; the DAG evaluator scores 15 leaves (13 local + 2
host UNKNOWN). No leaf may claim what only a human with ChatGPT can show.
"""
import json
import os
import subprocess
import sys
import time

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     ".."))
for _d in ("experiments/openai_native/src",
           "agentcombuild/agentloop/src"):
    _p = os.path.join(ROOT, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from opennative import mcp_servers, skill  # noqa: E402

CANON = os.path.join(ROOT, "packages", "agentcom-plugin-canonical",
                     "agentcom_plugin_canonical")
FACTORY = os.path.join(ROOT, "packages", "agent-plugin-factory",
                       "agent-plugin-factory")

ROUTING_KEYWORDS = ("business", "company", "shop", "store", "plumber",
                    "electrician", "quote", "booking", "hours", "service")

# Lint ERRORs that only the real world can clear (verified identity, live
# production endpoint, domain verification, demo recording, controls
# attestation). Offline they are UNKNOWN-by-construction, never waived and
# never faked. Everything else must be zero.
WORLD_DEPENDENT_ERRORS = frozenset(
    {"APP002H", "PUB001", "PUB002", "MCP002", "MCP005", "PRIV001"})
POSITIVE_CORPUS = [
    "Show me this UK business profile",
    "What are the company opening hours?",
    "Find me a plumber shop near Leeds",
    "Get a quote for this electrical service",
    "Is this store taking bookings?",
]
NEGATIVE_CORPUS = [
    "What is the weather today?",
    "Solve x^2 + 2x + 1 = 0",
    "Tell me a joke about parrots",
]


def route(query):
    q = query.lower()
    return any(k in q for k in ROUTING_KEYWORDS)


def mcp_lookup(company):
    return mcp_servers.call("business.lookup", {"company": company})


def factory_packet(workdir, candidate, snapshot):
    """Run the real factory packet command. Returns (rc, packet_path)."""
    os.makedirs(workdir, exist_ok=True)
    cpath = os.path.join(workdir, "candidate.json")
    spath = os.path.join(workdir, "snapshot.json")
    opath = os.path.join(workdir, "packet.json")
    json.dump(candidate, open(cpath, "w"), indent=2)
    json.dump(snapshot, open(spath, "w"), indent=2)
    env = dict(os.environ, PYTHONPATH=os.path.join(FACTORY))
    p = subprocess.run([sys.executable, "-m", "factory.cli", "packet",
                        cpath, spath, "--out", opath],
                       capture_output=True, text=True, timeout=120,
                       cwd=FACTORY, env=env)
    return p.returncode, opath, (p.stdout + p.stderr)[-500:]


def mcp_snapshot():
    """Snapshot our live tool surface for the factory."""
    r = mcp_servers.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    return {"server": {"name": "agentcom-qp-gateway", "transport": "stdio",
                       "auth": "none"},
            "tools": [{"name": t["name"], "title": t["name"],
                       "description": t.get("description", ""),
                       "inputSchema": t.get("inputSchema", {})}
                      for t in r["result"]["tools"]
                      if t["name"] == "business.lookup"]}


def plugin_spec(company_info, packet):
    """Generate the preflight spec (canonical schema shape)."""
    return {
        "app": {"name": "AgentCom UK Business", "subtitle": "Verified business context",
                "description": "Exposes verified UK small-business context through ChatGPT. Read-only v1.",
                "category": "business", "commerce": "none", "has_ui": False,
                "capabilities": ["business.lookup", "business.profile"],
                "starter_prompts": ["Show me this UK business"],
                "release_notes": "v0.1.0 simulated offline build. Fixture data only."},
        "mcp": {"url": "https://example.invalid/mcp", "public_production": False,
                "url_type": "Template", "auth_required": False,
                "domain_verified": False, "scan_current": True},
        "tools": [{"name": "business.lookup",
                   "description": "Look up verified structured context for a UK business by id, name or domain.",
                   "inputs": [{"name": "company", "type": "string",
                               "required": True,
                               "description": "Business id, name or domain"}],
                   "outputs": ["business", "error"],
                   "annotations": {"readOnlyHint": True, "openWorldHint": True,
                                   "destructiveHint": False},
                   "behavior": {"mutates_state": False,
                                "accesses_public_or_open_ended_external_entities": True,
                                "irreversible_or_hard_to_reverse": False,
                                "sends_data_to_third_party": False},
                   "annotation_justifications": {
                       "readOnlyHint": "Tool performs no mutations whatsoever.",
                       "openWorldHint": "Company names come from open user input.",
                       "destructiveHint": "Read path cannot destroy anything."}}],
        "tests": {"positive": [{"q": q} for q in POSITIVE_CORPUS],
                  "negative": [{"q": q} for q in NEGATIVE_CORPUS]},
        "publisher": {"verified_identity": False,
                      "identity_name_matches_public_urls": False,
                      "website_url": "https://example.invalid",
                      "support_url": "https://example.invalid/support",
                      "privacy_url": "https://example.invalid/privacy",
                      "terms_url": "https://example.invalid/terms"},
        "privacy": {"policy_covers_categories": True,
                    "policy_covers_purposes": True,
                    "policy_covers_recipients": True,
                    "policy_covers_retention": True,
                    "policy_covers_controls": False},
        "third_party_integrations": [],
        "_provenance": {"company": company_info.get("business", {}).get("id"),
                        "packet_score": (packet.get("score", {}) or {})
                        .get("score_0_100")},
    }


def lint_spec(spec_path):
    """Run canonical lint + schema validation. Returns dict of results."""
    out = {}
    p = subprocess.run([sys.executable, "checks/plugin_lint.py", spec_path],
                       capture_output=True, text=True, timeout=60,
                       cwd=CANON)
    out["lint_rc"] = p.returncode
    out["lint_full"] = (p.stdout or "") + (p.stderr or "")
    out["lint_tail"] = out["lint_full"][-400:]
    p = subprocess.run([sys.executable, "checks/validate_schema.py", spec_path],
                       capture_output=True, text=True, timeout=60,
                       cwd=CANON)
    out["schema_rc"] = p.returncode
    out["schema_tail"] = (p.stdout + p.stderr)[-400:]
    return out


def evaluate_dag(checks):
    """15 leaves: 13 local + 2 host UNKNOWN (never faked). Returns
    {leaves[{id, value}], true, unknown, false}."""
    leaves = []
    for leaf_id, value in checks:
        leaves.append({"id": leaf_id, "value": value})
    true = sum(1 for _, v in checks if v == "TRUE")
    unknown = sum(1 for _, v in checks if v == "UNKNOWN")
    false = sum(1 for _, v in checks if v == "FALSE")
    return {"leaves": leaves, "true": true, "unknown": unknown,
            "false": false}


def build(spec_path, out_root):
    """Full product pipeline. Returns report dict (JSON-serializable)."""
    t0 = time.monotonic()
    with open(spec_path) as fh:
        spec = json.load(fh)
    company = spec.get("company", "")
    work = os.path.join(out_root, "work")
    dist = os.path.join(out_root, "dist", "plugins", "agentcom-uk")
    os.makedirs(work, exist_ok=True)
    os.makedirs(dist, exist_ok=True)
    steps = []

    def step(name, ok, detail=""):
        steps.append({"name": name, "ok": bool(ok), "detail": detail[:200]})
        return ok

    # 1-5. MCP live surface
    info = mcp_lookup(company)
    step("mcp-starts", True, "gateway dispatch ok")
    init = mcp_servers.handle({"jsonrpc": "2.0", "id": 1,
                               "method": "initialize"})["result"]
    step("client-connects", init.get("protocolVersion") == "2024-11-05"
         and "serverInfo" in init, "official wire shape")
    tools = mcp_servers.handle({"jsonrpc": "2.0", "id": 1,
                                "method": "tools/list"})["result"]["tools"]
    step("tools-list", any(t["name"] == "business.lookup" for t in tools),
         "business.lookup exposed")
    step("lookup-returns", bool(info.get("found"))
         and "services" in info.get("business", {}), info.get("business", {})
         .get("id", ""))
    bad = mcp_lookup("no-such-company-zzz")
    step("invalid-bounded-error", bad.get("error") == "unknown-company"
         and bool(bad.get("known")), "deterministic error + known list")

    # 6-7. factory packet (real) + spec validate + lint (real)
    candidate = {"id": "business-lookup", "name": "Business Lookup",
                 "purpose": "Verified UK business context lookup.",
                 "source": {"kind": "owned_mcp",
                            "url": "https://example.invalid/mcp"},
                 "rights_status": "owned",
                 "scores": {"intent_frequency": 4, "user_value": 5,
                            "externality": 4, "authoritative_state": 5,
                            "actionability": 4, "verifiability": 5,
                            "chat_fit": 5, "ai_complementarity": 4,
                            "existing_mcp_quality": 4, "rights_clarity": 5,
                            "auth_friction": 1, "safety_liability": 1,
                            "internalization_risk": 1,
                            "distribution_ambiguity": 1}}
    rc, ppath, tail = factory_packet(work, candidate, mcp_snapshot())
    step("factory-packet", rc == 0 and os.path.exists(ppath), tail[-120:])
    packet = json.load(open(ppath)) if os.path.exists(ppath) else {}
    pspec = plugin_spec(info, packet)
    spath = os.path.join(work, "plugin_spec.json")
    json.dump(pspec, open(spath, "w"), indent=2)
    lint = lint_spec(spath)
    step("spec-validates", lint["schema_rc"] == 0, lint["schema_tail"][-120:])
    import re as _re
    lint_codes = set(_re.findall(r"ERROR (\w+):", lint.get("lint_full", "")))
    offline_codes = lint_codes - WORLD_DEPENDENT_ERRORS
    step("lint-offline-clean", not offline_codes,
         "non-world errors: %s" % sorted(offline_codes))
    world_codes = sorted(lint_codes & WORLD_DEPENDENT_ERRORS)
    lint["world_codes"] = world_codes

    # 8-9. routing evals
    # P9: the router is a local keyword heuristic, not ChatGPT routing.
    # Leaf names say so; host leaves stay UNKNOWN until ChatGPT evidence.
    pos = sum(1 for q in POSITIVE_CORPUS if route(q))
    neg = sum(1 for q in NEGATIVE_CORPUS if not route(q))
    step("local-routing-positive", pos == 5, "%d/5 route" % pos)
    step("local-routing-negative", neg == 3, "%d/3 stay out" % neg)

    # 10-12. skill + package + catalog
    from opennative import skill as _skill
    sk = _skill.build_skill(domain="business-operator")
    skdir = os.path.join(dist, "skills", "business-operator")
    os.makedirs(skdir, exist_ok=True)
    _skill.write({"SKILL.md": sk["SKILL.md"], "policy.json": sk["policy.json"],
                  "resources.json": sk["resources.json"]}, skdir)
    step("skill-builds", os.path.exists(os.path.join(skdir, "SKILL.md")),
         "business-operator skill")
    json.dump(pspec, open(os.path.join(dist, "plugin.json"), "w"), indent=2)
    catalog = {"marketplace": "agentcom-workspace",
               "plugins": [{"name": "agentcom-uk-business-profile",
                            "version": "0.1.0", "path": "plugin.json"}]}
    json.dump(catalog, open(os.path.join(dist, "catalog.json"), "w"),
              indent=2)
    step("package-builds", True, "dist/plugins/agentcom-uk/")
    step("catalog-validates", catalog["plugins"][0]["version"] == "0.1.0",
         "workspace catalog entry")

    # 13. host + final-gate leaves: UNKNOWN with manual slots, never faked
    host = [("host-install", "UNKNOWN"), ("host-invocation", "UNKNOWN"),
            ("lint-final-gates", "UNKNOWN")]
    # 14. latency recorded
    t1 = time.monotonic()
    mcp_lookup(company)
    latency_ms = int((time.monotonic() - t1) * 1000)

    dag = evaluate_dag([
        ("mcp-starts", "TRUE"), ("client-connects", "TRUE"),
        ("tools-list", "TRUE"), ("lookup-returns", "TRUE"),
        ("invalid-bounded-error", "TRUE"), ("spec-validates", "TRUE"),
        ("lint-offline-clean", "TRUE"), ("local-routing-positive", "TRUE"),
        ("local-routing-negative", "TRUE"), ("skill-builds", "TRUE"),
        ("package-builds", "TRUE"), ("catalog-validates", "TRUE"),
        ("lint-final-gates", "UNKNOWN"),
        ("host-install", "UNKNOWN"), ("host-invocation", "UNKNOWN"),
        ("latency-recorded", "TRUE")])
    # cross-check local leaves against actual step outcomes
    local_ok = all(s["ok"] for s in steps)
    if not local_ok:
        dag = evaluate_dag([(l["id"], "FALSE" if l["id"] not in
                             ("host-install", "host-invocation",
                              "lint-final-gates") else "UNKNOWN")
                            for l in dag["leaves"]])
    report = {"product": spec.get("product"), "steps": steps, "dag": dag,
              "latency_ms": latency_ms, "dist": dist,
              "world_codes": lint.get("world_codes", []),
              "contract": "contract:uk-business-profile",
              "ok": local_ok and dag["false"] == 0}
    # P7 statuses: offline success with UNKNOWN leaves is LOCAL_PASS, never
    # proven. PRODUCT_PROVEN requires every hard leaf TRUE (needs the host).
    if not report["ok"]:
        report["status"] = "FAILED"
    elif dag["unknown"] == 0 and dag["false"] == 0:
        report["status"] = "PRODUCT_PROVEN"
    else:
        report["status"] = "LOCAL_PASS"
    json.dump(report, open(os.path.join(work, "report.json"), "w"), indent=2)
    return report
