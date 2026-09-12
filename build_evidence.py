"""Generate evidence.html plain table from a run-result JSON. 1h-max tool, no framework."""
import argparse, html, json, pathlib

TEMPLATE_ROW = "<tr><td>{i}</td><td>{claim}</td><td>{url}</td><td><code>{snippet}</code></td><td>{off}</td><td>{sha}</td><td>{ref}</td></tr>"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="last_run.json")
    ap.add_argument("--out", default="evidence.html")
    ap.add_argument("--template", default="evidence.html")
    a = ap.parse_args()
    data = json.loads(pathlib.Path(a.inp).read_text(encoding="utf-8"))
    evs = data.get("evidence", [])
    rows = []
    for i, e in enumerate(evs, 1):
        rows.append(TEMPLATE_ROW.format(
            i=i, claim=html.escape(str(e.get("claim", ""))),
            url=html.escape(str(e.get("url", ""))),
            snippet=html.escape(str(e.get("snippet_verbatim", ""))[:300]),
            off=e.get("char_offset", ""), sha=str(e.get("sha256", ""))[:12],
            ref=e.get("action_log_ref", "")))
    tpl = pathlib.Path("evidence_template.html")
    base = tpl.read_text(encoding="utf-8") if tpl.exists() else pathlib.Path(a.template).read_text(encoding="utf-8")
    out = base.replace("<!--ROWS-->", ("\n".join(rows) if rows else "<tr><td colspan=7>no evidence</td></tr>") + "\n<!--ROWS-->")
    pathlib.Path(a.out).write_text(out, encoding="utf-8")
    print(f"wrote {a.out} with {len(rows)} rows")

if __name__ == "__main__":
    main()
