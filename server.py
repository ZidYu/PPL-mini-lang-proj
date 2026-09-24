from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json, sys
ROOT = Path(__file__).parent.resolve()
SRC = ROOT / 'src'
sys.path.insert(0, str(ROOT))
from src.main import execute_source
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT/'server'/'web'),**kwargs)
    def do_POST(self):
        if self.path != '/api/run': self.send_error(404); return
        try:
            length=int(self.headers.get('Content-Length','0')); data=json.loads(self.rfile.read(length))
            output=execute_source(data.get('code',''))
            payload={'ok':True,'output':'\n'.join(output)}
            self.send_response(200)
        except Exception as e:
            payload={'ok':False,'error':str(e)}; self.send_response(400)
        self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(json.dumps(payload).encode())
if __name__=='__main__':
    print('Open http://127.0.0.1:8000')
    ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()
