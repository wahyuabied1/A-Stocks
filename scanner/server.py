"""API lokal (hanya localhost) untuk dashboard Next.js + worker pemindaian di latar belakang."""
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .config import STYLES
from .engine import MAX_WATCHLIST


def serve(scanner, cfg):
    class Handler(BaseHTTPRequestHandler):
        def _json(self, code, payload):
            body = json.dumps(payload, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _read_json(self):
            # Wajib application/json: request lintas situs dengan tipe ini selalu butuh preflight CORS
            # (yang tidak dijawab server ini), sehingga situs lain tidak bisa mengubah watchlist diam-diam.
            if not self.headers.get("Content-Type", "").startswith("application/json"):
                return None
            length = int(self.headers.get("Content-Length") or 0)
            if length > 64_000:
                return None
            try:
                return json.loads(self.rfile.read(length) or b"{}")
            except ValueError:
                return None

        def do_GET(self):
            url = urlparse(self.path)
            query = parse_qs(url.query)
            if url.path == "/api/state":
                self._json(200, scanner.snapshot())
            elif url.path == "/api/chart":
                ticker = (query.get("ticker") or [""])[0].strip().upper().removesuffix(".JK")
                style = (query.get("style") or ["swing"])[0].strip().lower()
                if style not in STYLES:
                    self._json(400, {"error": f"Gaya tidak dikenal: {style}"})
                    return
                data = scanner.chart(ticker, style)
                if data is None:
                    self._json(404, {"error": f"{ticker} tidak ada di watchlist, atau gaya {style} tidak dipindai."})
                else:
                    self._json(200, data)
            elif url.path == "/api/watchlist":
                self._json(200, {"watchlist": scanner.cfg["watchlist"], "max": MAX_WATCHLIST})
            elif url.path == "/api/search":
                q = (query.get("q") or [""])[0].strip()
                if len(q) < 2:
                    self._json(200, {"results": []})
                    return
                watchlist = set(scanner.cfg["watchlist"])
                results = [{**r, "in_watchlist": r["ticker"] in watchlist} for r in scanner.source.search(q)]
                self._json(200, {"results": results})
            elif url.path == "/":
                self._json(200, {"message": "API pemindai sinyal IDX. Dashboard: jalankan `npm run dev` di folder web "
                                            "lalu buka http://localhost:3000"})
            else:
                self._json(404, {"error": "not found"})

        def do_POST(self):
            path = urlparse(self.path).path
            if path == "/api/scan":
                scanner.request_scan()
                self._json(202, {"ok": True})
            elif path == "/api/watchlist":
                body = self._read_json()
                if not isinstance(body, dict):
                    self._json(400, {"error": "Body harus JSON (Content-Type: application/json)."})
                    return

                def as_list(key):
                    value = body.get(key)
                    return [value] if isinstance(value, str) else list(value or [])

                replace = body.get("set")
                self._json(200, scanner.update_watchlist(add=as_list("add"), remove=as_list("remove"),
                                                         replace=replace if isinstance(replace, list) else None))
            else:
                self._json(404, {"error": "not found"})

        def log_message(self, *args):
            pass

    host, port = cfg["dashboard"]["host"], cfg["dashboard"]["port"]
    stop = threading.Event()
    threading.Thread(target=scanner.run_forever, args=(stop,), daemon=True).start()
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"API berjalan di http://{host}:{port}  (Ctrl+C untuk berhenti)")
    print("Dashboard Next.js: jalankan `npm run dev` di folder web lalu buka http://localhost:3000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nBerhenti.")
    finally:
        stop.set()
        httpd.server_close()
