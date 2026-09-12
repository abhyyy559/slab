"""Serve mocks statically: site_a at /site_a, site_b at /site_b."""
import argparse, functools, http.server, pathlib

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--dir", default=str(pathlib.Path(__file__).resolve().parent))
    a = ap.parse_args()
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=a.dir)
    srv = http.server.ThreadingHTTPServer(("0.0.0.0", a.port), handler)
    print(f"mocks serving {a.dir} at http://127.0.0.1:{a.port}/site_a/search.html and /site_b/check.html")
    srv.serve_forever()

if __name__ == "__main__":
    main()
