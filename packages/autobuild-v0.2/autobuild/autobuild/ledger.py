import json
from pathlib import Path
from .canonical import canonical_bytes,digest

GENESIS="sha256:"+"0"*64


def append_record(path,record):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    prev=GENESIS
    if path.exists():
        lines=[x for x in path.read_text().splitlines() if x.strip()]
        if lines:
            prev=json.loads(lines[-1])["envelope_root"]
    body={"record":record,"record_root":digest(record),"prev_root":prev}
    env={**body,"envelope_root":digest(body)}
    with path.open("ab") as f:f.write(canonical_bytes(env)+b"\n")
    return env


def verify_ledger(path):
    path=Path(path); count=0; bad=[]; prev=GENESIS
    if not path.exists():return {"result":"PASS","count":0,"bad":[],"tip":prev}
    for n,line in enumerate(path.read_text().splitlines(),1):
        if not line.strip():continue
        count+=1
        try:
            env=json.loads(line)
            body={"record":env["record"],"record_root":env["record_root"],"prev_root":env["prev_root"]}
            if digest(env["record"])!=env["record_root"] or env["prev_root"]!=prev or digest(body)!=env["envelope_root"]:
                bad.append(n)
            prev=env["envelope_root"]
        except Exception:bad.append(n)
    return {"result":"PASS" if not bad else "FAIL","count":count,"bad":bad,"tip":prev}
