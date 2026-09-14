
#!/usr/bin/env python3
"""Public GitHub snapshot poller. Implementation evidence only; never behavioral proof."""
import json, os, urllib.request, urllib.error, time
from pathlib import Path
from .model import projects, ROOT

def api(url):
    req=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','User-Agent':'campaign-control-plane/1.0'})
    tok=os.environ.get('GITHUB_TOKEN')
    if tok: req.add_header('Authorization',f'Bearer {tok}')
    with urllib.request.urlopen(req,timeout=15) as r: return json.loads(r.read())

def snapshot(repo_url):
    owner,repo=repo_url.rstrip('/').split('/')[-2:]
    meta=api(f'https://api.github.com/repos/{owner}/{repo}')
    branch=meta['default_branch']
    commit=api(f'https://api.github.com/repos/{owner}/{repo}/commits/{branch}')
    tree=api(f"https://api.github.com/repos/{owner}/{repo}/git/trees/{commit['sha']}?recursive=1")
    return {'repo':repo_url,'default_branch':branch,'commit':commit['sha'],'tree_sha':commit['commit']['tree']['sha'],'files':[x['path'] for x in tree.get('tree',[]) if x.get('type')=='blob'],'polled_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}

def poll_all():
    out=[]
    for p in projects():
        if not p.get('repo'): continue
        try: out.append(snapshot(p['repo']))
        except Exception as e: out.append({'repo':p['repo'],'error':str(e),'polled_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})
    path=ROOT/'data/repo_snapshots.json'; path.write_text(json.dumps({'snapshots':out},indent=2)); return out

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--watch',action='store_true',help='poll forever')
    ap.add_argument('--interval',type=int,default=900,help='seconds between polls')
    a=ap.parse_args()
    if not a.watch:
        print(json.dumps(poll_all(),indent=2))
    else:
        while True:
            print(json.dumps(poll_all(),indent=2),flush=True)
            time.sleep(max(60,a.interval))
