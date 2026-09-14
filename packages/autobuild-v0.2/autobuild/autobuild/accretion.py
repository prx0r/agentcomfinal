import json
from pathlib import Path
from .canonical import digest,content_id
from .ledger import append_record,verify_ledger

CONTRIB_WEIGHTS={"facts":1.0,"negative_facts":1.0,"edges":0.8,"fixtures":0.7,"components":0.7,"outcomes":0.5,"conflicts":1.0,"duplicates":-0.8,"unsupported_claims":-1.0}
PROVENANCE_KEYS={"evidence_ids","source","sources","observed_at","as_of","run_id","proof","trace_id"}


def _strip_provenance(x):
    if isinstance(x,dict): return {k:_strip_provenance(v) for k,v in sorted(x.items()) if k not in PROVENANCE_KEYS}
    if isinstance(x,list): return [_strip_provenance(v) for v in x]
    return x


def semantic_projection(kind,item):
    if kind=="facts" and isinstance(item,dict):
        return {k:item.get(k) for k in ("subject","predicate","value","qualifiers") if k in item}
    if kind=="negative_facts" and isinstance(item,dict):
        return {k:item.get(k) for k in ("subject","predicate","result","qualifiers") if k in item}
    return _strip_provenance(item)


def semantic_key(kind,item):
    return content_id(kind.rstrip("s") or "item",{"kind":kind,"semantic":semantic_projection(kind,item)})


def proposition_key(kind,item):
    if kind not in {"facts","negative_facts"} or not isinstance(item,dict): return None
    return content_id("prop",{"subject":item.get("subject"),"predicate":item.get("predicate"),"qualifiers":item.get("qualifiers",{})})


def contribution_score_from_counts(counts):
    parts={}; total=0.0
    for k,w in CONTRIB_WEIGHTS.items():
        n=int(counts.get(k,0)); parts[k]={"count":n,"weight":w,"contribution":w*n}; total+=w*n
    return {"formula_id":"realized-useful-yield-v2","score":round(total,6),"parts":parts}


def _scan(path):
    sem=set(); props={}
    p=Path(path)
    if not p.exists(): return sem,props
    for line in p.read_text().splitlines():
        if not line.strip(): continue
        try:
            env=json.loads(line); rec=env.get("record",{})
        except Exception: continue
        if rec.get("record_type")!="KNOWLEDGE": continue
        sem.add(rec.get("content_key"))
        pk=rec.get("proposition_key")
        if pk: props.setdefault(pk,set()).add(rec.get("semantic_value_hash"))
    return sem,props


def accrue(path,run):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    chain=verify_ledger(path)
    if chain["result"]!="PASS": return {"result":"FAIL","accretion_gate":"FAIL","reason":"ledger integrity failure","ledger_check":chain}
    existing,props=_scan(path); run_root=digest(run)
    append_record(path,{"record_type":"RUN","run_root":run_root,"run":run})
    new_counts={k:0 for k in CONTRIB_WEIGHTS}; dup=0; conflicts=0
    for kind,items in sorted(run.get("contributions",{}).items()):
        if kind in {"duplicates","unsupported_claims"}:
            new_counts[kind]+=len(items or []); continue
        for item in items or []:
            key=semantic_key(kind,item)
            if key in existing:
                dup+=1; new_counts["duplicates"]+=1; continue
            proj=semantic_projection(kind,item); svh=digest(proj); pk=proposition_key(kind,item)
            conflict=False
            if pk and pk in props and svh not in props[pk]: conflict=True
            rec={"record_type":"KNOWLEDGE","run_root":run_root,"knowledge_kind":kind,"epistemic_status":"UNVERIFIED_OBSERVATION","content_key":key,"semantic":proj,"raw":item,"semantic_value_hash":svh,"proposition_key":pk,"promotion_requires":"QP_VERIFIED_RECEIPT_OR_EQUIVALENT_DETERMINISTIC_PROOF"}
            append_record(path,rec); existing.add(key); new_counts[kind]=new_counts.get(kind,0)+1
            if pk: props.setdefault(pk,set()).add(svh)
            if conflict:
                conflicts+=1; new_counts["conflicts"]+=1
                append_record(path,{"record_type":"CONFLICT","run_root":run_root,"proposition_key":pk,"new_content_key":key,"known_value_hashes":sorted(props[pk]),"status":"UNRESOLVED"})
    score=contribution_score_from_counts(new_counts)
    new_knowledge=sum(new_counts.get(k,0) for k in ("facts","negative_facts","edges","fixtures","components","outcomes","conflicts"))
    consumed=(run.get("cost") or 0)>0 or (run.get("duration_ms") or 0)>0 or (run.get("tokens") or 0)>0
    gate="PASS" if (new_knowledge>0 or not consumed) else "FAIL"
    return {"result":"PASS","accretion_gate":gate,"run_root":run_root,"new_knowledge_records":new_knowledge,"duplicates_suppressed":dup,"conflicts":conflicts,"yield":score,"ledger":str(path),"ledger_check":verify_ledger(path)}
