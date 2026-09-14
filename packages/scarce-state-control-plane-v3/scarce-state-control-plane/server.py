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
    def _body(self):
        n=int(self.headers.get('Content-Length','0')); return json.loads(self.rfile.read(n) or b'{}')
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
        if u.path=='/api/experiment-worlds':
            from runtime.experiments import catalog,select_world
            pid=q.get('id',[''])[0]
            try:return self._json(select_world(pid) if pid else catalog())
            except KeyError:return self._json({'error':'not found'},404)
        if u.path=='/api/target-profiles':
            from runtime.experiments import target_profiles; return self._json(target_profiles())
        if u.path=='/api/schedule':
            from runtime.scheduler import schedule; return self._json(schedule())
        if u.path=='/api/resources':
            from runtime.resources import resources; return self._json(resources())
        if u.path=='/api/hdesk':
            from runtime.hdesk import queue,templates; return self._json({'queue':queue(),'templates':templates()})
        if u.path=='/api/performance':
            from runtime.performance import strategy_performance,replication_candidates; return self._json({'families':strategy_performance(),'replication_candidates':replication_candidates()})
        if u.path=='/api/selflab':
            from runtime.selflab import breadup_self_lab; return self._json(breadup_self_lab())
        if u.path=='/api/simulate':
            from runtime.simulation import simulate_project
            try:return self._json(simulate_project(q.get('id',[''])[0]))
            except KeyError:return self._json({'error':'not found'},404)
        if u.path=='/api/health': return self._json({'ok':True,'service':'autonomous-economic-discovery-control-plane','version':'3.0.0'})
        if u.path=='/': self.path='/web/index.html'
        return super().do_GET()
    def do_POST(self):
        u=urlparse(self.path)
        try:
            body=self._body()
            if u.path=='/api/htask/answer':
                from runtime.hdesk import answer
                return self._json(answer(body['task_id'],body['decision'],body.get('note','')))
            if u.path=='/api/htask/add':
                from runtime.hdesk import add
                return self._json(add(body['kind'],body['question'],body.get('project_id'),body.get('options'),body.get('recommendation'),body.get('why_human',''),body.get('blocking_value',1),body.get('estimated_minutes',5)),201)
            if u.path=='/api/experiment/record':
                from runtime.performance import record
                return self._json(record(body['project_id'],body['world'],body['evidence_source'],body['result'],body.get('strategy_family'),body.get('metric'),body.get('cost'),body.get('human_minutes'),body.get('receipt_ref'),body.get('hypothesis','')),201)
            return self._json({'error':'not found'},404)
        except (KeyError,ValueError,TypeError,json.JSONDecodeError) as e:
            return self._json({'error':str(e)},400)

if __name__=='__main__':
    os.chdir(ROOT); port=int(os.environ.get('PORT','8787'))
    print(f'Autonomous Economic Discovery Control Plane: http://127.0.0.1:{port}')
    ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
