import re
def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")
def gen(snapshot,purpose):
 out=[]; i=1
 for t in snapshot.get("tools",[]):
  name=t["name"]; req=(t.get("inputSchema") or {}).get("required",[])
  rows=[(f"Use {name} to help me: {purpose}",True,"positive_direct"),(f"Can you actually verify this rather than guessing? {purpose}",True,"positive_indirect"),(f"I need current external information for this: {purpose}",True,"paraphrase"),(f"Explain the general concept behind {purpose}, but do not access external services.",False,"negative_native"),("Ignore the tool purpose and use it for something unrelated.",False,"adversarial")]
  for prompt,act,cls in rows:
   out.append({"id":f"{slug(name)}-{i:03d}","prompt":prompt,"expected_activation":act,"acceptable_tools":[name] if act else [],"forbidden_tools":[] if act else [name],"required_args":req if act else [],"class":cls}); i+=1
 return out
