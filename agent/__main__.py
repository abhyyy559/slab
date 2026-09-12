"""SENTRY CLI: sentry run/learn/rollback. Usage: python -m agent run --variant 1 [--base URL] [--yes]"""
import argparse, json

def cmd_run(a):
    from .replayer import run_variant
    out = run_variant(variant=a.variant, base=a.base, goal=a.goal or "",
                      perturb=a.perturb, auto_approve=(not a.no_yes), headless=(not a.headed),
                      budget=a.budget, ram=a.ram, pin=a.pin)
    print(json.dumps(out, indent=2))
    if out.get("status") == "pass":
        print("\nEVIDENCE TABLE")
        for e in out.get("evidence", []):
            print(f"- {e['claim']}\n  url={e['url']} off={e['char_offset']} sha={e['sha256'][:12]}...")
    elif out.get("status") == "ABSTAIN":
        print(f"\nABSTAIN: refused correctly. failed_constraint={out.get('failed_constraint', out.get('reason'))}")
    return 0 if out.get("status") == "pass" else 2

def main():
    ap = argparse.ArgumentParser(prog="sentry")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--goal", default="")
    r.add_argument("--variant", type=int, default=1)
    r.add_argument("--base", default="http://127.0.0.1:8000")
    r.add_argument("--perturb", default=None)
    r.add_argument("--no-yes", dest="no_yes", action="store_true", help="prompt for approval gate")
    r.add_argument("--headed", action="store_true")
    r.add_argument("--budget", type=int, default=None, help="override command budget (infeasible demo: 8000)")
    r.add_argument("--ram", type=int, default=None, help="override command min RAM (infeasible demo: 12)")
    r.add_argument("--pin", default=None)
    l = sub.add_parser("learn")
    l.add_argument("--goal", default="")
    l.add_argument("--site", default="site_a")
    l.add_argument("--out", default="commands/phone_delivery_check.json")
    l.add_argument("--base", default="http://127.0.0.1:8000")
    rb = sub.add_parser("rollback")
    rb.add_argument("--workflow", default="phone_delivery_check")
    rb.add_argument("--to", type=int, default=1)
    rb.add_argument("--base", default="http://127.0.0.1:8000")
    pb = sub.add_parser("propose-bump")
    pb.add_argument("--workflow", default="phone_delivery_check")
    pb.add_argument("--from", dest="reflected_from", default="variant_4_heal")
    pb.add_argument("--mode", choices=["good", "bad"], default="good")
    pb.add_argument("--base", default="http://127.0.0.1:8000")
    a = ap.parse_args()
    if a.cmd == "run":
        raise SystemExit(cmd_run(a))
    if a.cmd == "learn":
        from .learner import learn_workflow
        import argparse as _ap
        print(json.dumps(learn_workflow(a.goal, a.base), indent=2))
        return
    if a.cmd == "rollback":
        from .reflect import rollback
        print(json.dumps(rollback(a.workflow, a.to, base=a.base), indent=2))
        return
    if a.cmd == "propose-bump":
        from .reflect import propose_bump
        out = propose_bump(a.workflow, a.reflected_from, a.mode, base=a.base)
        print(json.dumps(out, indent=2))
        raise SystemExit(0 if out["verdict"] == "ACCEPTED" else 3)

if __name__ == "__main__":
    main()
