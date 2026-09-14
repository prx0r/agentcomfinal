
#!/usr/bin/env python3
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
from pathlib import Path
import json, mimetypes, os
from runtime.model import portfolio,projects,project,bottlenecks,components,ROOT
from runtime.drift import repo_drift

class Handler(SimpleHTTPRequestHandler):
    def _json(self,obj,status=200):
        raw=json.dumps(obj).encode(); self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        u=urlparse(self.path)
        if u.path=='/api/portfolio': return self._json(portfolio())
        if u.path=='/api/projects': return self._json(projects())
        if u.path=='/api/project':
            pid=parse_qs(u.query).get('id',[''])[0]
            try:return self._json(project(pid))
            except KeyError:return self._json({'error':'not found'},404)
        if u.path=='/api/bottlenecks': return self._json(bottlenecks())
        if u.path=='/api/components': return self._json(components())
        if u.path=='/api/repo-snapshots': return self._json(json.loads((ROOT/'data/repo_snapshots.json').read_text()))
        if u.path=='/api/drift':
            pid=parse_qs(u.query).get('id',[''])[0]
            try:return self._json(repo_drift(pid))
            except KeyError:return self._json({'error':'not found'},404)
        if u.path=='/api/health': return self._json({'ok':True,'service':'campaign-control-plane'})
        if u.path=='/': self.path='/web/index.html'
        return super().do_GET()

if __name__=='__main__':
    os.chdir(ROOT)
    port=int(os.environ.get('PORT','8787'))
    print(f'Campaign Control Plane: http://127.0.0.1:{port}')
    ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
