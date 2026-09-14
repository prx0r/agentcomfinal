from .scoring import score_candidate
from .evals import gen
def packet(c,s):
 rw=[]
 for t in s.get("tools",[]):
  d=t.get("description","").strip(); title=t.get("title") or t["name"].replace("_"," ")
  rw.append({"tool":t["name"],"original_description":d,"proposed_description": d if d.lower().startswith("use this when") else f"Use this when the user needs to {title.lower()}. {d}","annotations":t.get("annotations",{})})
 return {"candidate":c,"score":score_candidate(c),"mcp_server":s.get("server",{}),"tool_rewrites":rw,"seed_evals":gen(s,c.get("purpose","")),"gates":["rights","conformance","tool-semantics","MCPJam-eval","real-ChatGPT-host-eval","privacy-auth-CSP","OpenAI-submission"]}
