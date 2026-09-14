#!/usr/bin/env python3
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
import json, os
from runtime.model import portfolio,projects,project,bottlenecks,components,ROOT
from runtime.drift import repo_drift
from runtime.underengineer import plan,ranked,order
from runtime.scarcity import declared_assets,ledger,substitution_summary

class Handler(SimpleHTTPRequestHandler):
    def _json(self,obj,status=200):
        raw=json.dumps(obj).encode(); self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        u=urlparse(self.path); q=parse_qs(u.query)
        if u.path=='/api/portfolio': return self._json(portfolio())
        if u.path=='/api/projects': return self._json(projects())
        if u.path=='/api/project':
            try:return self._json(project(q.get('id',[''])[0]))
            except KeyError:return self._json({'error':'not found'},404)
        if u.path=='/api/underengineer':
            pid=q.get('id',[''])[0]
            try:return self._json(plan(pid) if pid else ranked())
            except KeyError:return self._json({'error':'not found'},404)
        if u.path=='/api/order':
            pid=q.get('id',[''])[0] or None
            try:return self._json(order(pid))
            except KeyError:return self._json({'error':'not found'},404)
        if u.path=='/api/assets': return self._json({'declared':declared_assets(),'ledger':ledger()})
        if u.path=='/api/substitution': return self._json(substitution_summary())
        if u.path=='/api/bottlenecks': return self._json(bottlenecks())
        if u.path=='/api/components': return self._json(components())
        if u.path=='/api/repo-snapshots': return self._json(json.loads((ROOT/'data/repo_snapshots.json').read_text()))
        if u.path=='/api/drift':
            try:return self._json(repo_drift(q.get('id',[''])[0]))
            except KeyError:return self._json({'error':'not found'},404)
        if u.path=='/api/health': return self._json({'ok':True,'service':'scarce-state-control-plane','version':'2.0.0'})
        if u.path=='/': self.path='/web/index.html'
        return super().do_GET()

if __name__=='__main__':
    os.chdir(ROOT); port=int(os.environ.get('PORT','8787'))
    print(f'Scarce State Control Plane: http://127.0.0.1:{port}')
    ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
