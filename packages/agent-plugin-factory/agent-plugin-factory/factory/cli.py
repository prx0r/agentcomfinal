import argparse,json
from pathlib import Path
from .scoring import score_candidate
from .packet import packet
from .registry import fetch
def load(p):return json.loads(Path(p).read_text())
def emit(x,out=None):
 s=json.dumps(x,indent=2);
 if out: Path(out).parent.mkdir(parents=True,exist_ok=True);Path(out).write_text(s);print(out)
 else: print(s)
def main():
 ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest="cmd",required=True)
 a=sub.add_parser("score");a.add_argument("candidate")
 p=sub.add_parser("packet");p.add_argument("candidate");p.add_argument("snapshot");p.add_argument("--out")
 r=sub.add_parser("registry");r.add_argument("--limit",type=int,default=100);r.add_argument("--out")
 x=ap.parse_args()
 if x.cmd=="score":emit(score_candidate(load(x.candidate)))
 elif x.cmd=="packet":emit(packet(load(x.candidate),load(x.snapshot)),x.out)
 else:emit(fetch(x.limit),x.out)
if __name__=="__main__":main()
