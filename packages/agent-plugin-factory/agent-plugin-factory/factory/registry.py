import json,urllib.request,urllib.parse
BASE="https://registry.modelcontextprotocol.io"
def fetch(limit=100,cursor=None):
 q={"limit":str(limit)}
 if cursor:q["cursor"]=cursor
 url=BASE+"/v0.1/servers?"+urllib.parse.urlencode(q)
 req=urllib.request.Request(url,headers={"User-Agent":"agent-plugin-factory/0.1"})
 with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
