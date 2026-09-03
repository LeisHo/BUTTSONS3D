#!/usr/bin/env python3
"""Local dev server for BUTTSONS3D -- plain static file serving, plus one POST
endpoint so the dev panel's Save Settings button can write through to a
git-tracked settings log (CLAUDE.md 12l), not just the browser's own
localStorage. A plain `python -m http.server` has no way to receive or write
data, so this extends it with exactly one route.
"""
import http.server
import json
import os

PORT = 8938  # distinct from BUTTSONS's own dev server (8937) so both can run at once
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SETTINGS_LOG_PATH = os.path.join(REPO_ROOT, "data", "processed", "dev-panel-settings.json")


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/save-settings":
            self.send_response(404)
            self.end_headers()
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body)
            os.makedirs(os.path.dirname(SETTINGS_LOG_PATH), exist_ok=True)
            with open(SETTINGS_LOG_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
                f.write("\n")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode("utf-8"))


if __name__ == "__main__":
    os.chdir(REPO_ROOT)
    with http.server.ThreadingHTTPServer(("", PORT), Handler) as httpd:
        print(f"Serving {REPO_ROOT} on port {PORT} (with /api/save-settings write endpoint)")
        httpd.serve_forever()
