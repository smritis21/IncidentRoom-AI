"""Local read-only dashboard. Incident actions remain in the terminal."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parent
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  if self.path == "/api/status":
   path = ROOT / ".incident-state.json"
   try: body = path.read_bytes() if path.exists() else b'{"status":"ready","events":[]}'
   except OSError: self.send_error(500); return
   content = "application/json"
  elif self.path in ("/", "/index.html"):
   body = (ROOT / "dashboard" / "index.html").read_bytes(); content = "text/html; charset=utf-8"
  else: self.send_error(404); return
  self.send_response(200); self.send_header("Content-Type",content); self.send_header("Cache-Control","no-store"); self.send_header("X-Content-Type-Options","nosniff"); self.end_headers(); self.wfile.write(body)
if __name__ == "__main__":
 print("IncidentRoom dashboard: http://127.0.0.1:8080", flush=True)
 HTTPServer(("127.0.0.1",8080), Handler).serve_forever()
