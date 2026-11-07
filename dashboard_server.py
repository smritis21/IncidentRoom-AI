"""Local dashboard for the disposable incident fixture."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import hashlib, json, os, secrets, subprocess, sys
ROOT = Path(__file__).resolve().parent
TOKEN = secrets.token_urlsafe(32)
PORT = int(os.environ.get("INCIDENTROOM_PORT", "8080"))
HOST = f"127.0.0.1:{PORT}"
ORIGIN = f"http://{HOST}"
class Handler(BaseHTTPRequestHandler):
 def reply(self, code, body, content="application/json"):
  self.send_response(code); self.send_header("Content-Type",content); self.send_header("Cache-Control","no-store"); self.send_header("X-Content-Type-Options","nosniff"); self.end_headers(); self.wfile.write(body)
 def do_GET(self):
  if self.headers.get("Host") != HOST: self.send_error(403); return
  if self.path == "/api/status":
   path = ROOT / ".incident-state.json"
   try: body = path.read_bytes() if path.exists() else b'{"status":"ready","events":[]}'
   except OSError: self.send_error(500); return
   self.reply(200,body)
  elif self.path in ("/", "/index.html"):
   page=(ROOT / "dashboard" / "index.html").read_text(encoding="utf-8").replace("__SESSION_TOKEN__",TOKEN)
   self.reply(200,page.encode(),"text/html; charset=utf-8")
  else: self.send_error(404)
 def do_POST(self):
  if (self.headers.get("Host") != HOST or self.headers.get("Origin") != ORIGIN or
      not secrets.compare_digest(self.headers.get("X-Incident-Token", ""), TOKEN)):
   self.send_error(403); return
  if self.path not in ("/api/triage", "/api/approve", "/api/reset"): self.send_error(404); return
  try:
   length=int(self.headers.get("Content-Length", "0"))
   if length > 1024: raise ValueError("Request too large")
   data=json.loads(self.rfile.read(length) or b"{}")
   if not isinstance(data,dict): raise ValueError("Invalid request")
   state_path=ROOT / ".incident-state.json"
   state=json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {"status":"ready"}
   if self.path == "/api/reset":
    target=ROOT / "checkout.py"; current=target.read_bytes()
    if state.get("status") not in ("verified", "verification_failed", "applied") or hashlib.sha256(current).hexdigest()!=state.get("patch_sha256"):
     raise ValueError("Cannot reset: the fixture differs from the approved version.")
    original=current.decode("utf-8").replace('if (coupon or "").upper() == "SAVE10":','if coupon.upper() == "SAVE10":',1).encode("utf-8")
    if hashlib.sha256(original).hexdigest()!=state.get("source_sha256"): raise ValueError("Cannot reset: original fixture does not match.")
    target.write_bytes(original); state_path.unlink(); self.reply(200,b'{"message":"Demo reset."}'); return
   if self.path == "/api/triage":
    if state.get("status") != "ready": raise ValueError("An incident is already in progress. Restore the fixture to start again.")
    args=["triage"]
   else:
    value=data.get("sha256", "")
    if not isinstance(value,str) or len(value)!=64 or any(c not in "0123456789abcdef" for c in value): raise ValueError("Invalid approval hash")
    args=["approve",value]
   result=subprocess.run([sys.executable,str(ROOT / "incident.py"),*args],cwd=ROOT,text=True,capture_output=True,timeout=60)
   self.reply(200 if result.returncode == 0 else 400,json.dumps({"message":result.stdout+result.stderr}).encode())
  except (ValueError,OSError,subprocess.TimeoutExpired) as e: self.reply(400,json.dumps({"message":str(e)}).encode())
if __name__ == "__main__":
 print(f"IncidentRoom dashboard: {ORIGIN}", flush=True)
 HTTPServer(("127.0.0.1",PORT), Handler).serve_forever()
