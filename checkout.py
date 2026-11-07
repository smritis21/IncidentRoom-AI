"""Intentionally broken checkout fixture. No external services required."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

def total(cents, coupon):
    # INCIDENT: optional coupon is None for ordinary customers.
    if coupon.upper() == "SAVE10":
        return cents * 90 // 100
    return cents

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if urlparse(self.path).path != "/checkout":
            self.send_error(404); return
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))))
            result = {"total_cents": total(data["cents"], data.get("coupon"))}
            body = json.dumps(result).encode(); self.send_response(200)
        except Exception:
            body = b'{"error":"checkout failed"}'; self.send_response(500)
        self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(body)

if __name__ == "__main__": HTTPServer(("127.0.0.1", 8081), Handler).serve_forever()
