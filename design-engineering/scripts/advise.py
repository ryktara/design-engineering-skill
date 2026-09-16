#!/usr/bin/env python3
"""design-engineering advisor CLI.

  python advise.py requirements "<request>" [--project inspect.json] [--pretty] [--explain] [--json]
  python advise.py classify "<request>"                       # legacy signals view + activation proxy
  python advise.py guidance "<request>" [--project inspect.json] [--explain] [--json] [--size N]   # task-oriented bundle (preferred)
  python advise.py search "<request>" [-k 5] [--kind rule] [--category focus] [--explain] [--json] [--no-facets]  # raw ranked lookup
  python advise.py direction "<request>" [--brand NAME] [--explain] [--json] [--out dir.json]
  python advise.py show <record-id>

Common options: --project <inspect.json> (from inspect_project.py; its findings become KNOWN evidence),
--platform/--stack/--product manual hints (repeatable).

Exit codes: 0 CONFIDENT/success · 3 PARTIAL · 4 AMBIGUOUS · 5 ABSTAIN · 2 invalid input · 1 tool failure.
Pass --exit-zero to always exit 0 on a successful run (for shells that treat non-zero as failure).
"""

from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import de_core as core  # noqa: E402

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

STATUS_EXIT = {"CONFIDENT": 0, "PARTIAL": 3, "AMBIGUOUS": 4, "ABSTAIN": 5}


def _project(args) -> dict | None:
    proj = None
    if getattr(args, "project", None):
        try:
            proj = json.loads(Path(args.project).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"error: cannot read project inspection file {args.project}: {e}", file=sys.stderr)
            sys.exit(2)
        if not isinstance(proj, dict) or "stack_groups" not in proj:
            print(f"error: {args.project} is not inspect_project.py output (missing stack_groups)", file=sys.stderr)
            sys.exit(2)
    manual = {"platforms": args.platform or [], "stack_groups": args.stack or [], "product_hints": args.product or [], "findings": []}
    for key, allowed in (("platforms", core.PLATFORMS), ("stack_groups", core.STACK_GROUPS), ("product_hints", core.PRODUCTS)):
        bad = [v for v in manual[key] if v not in allowed]
        if bad:
            print(f"error: unknown {key} {bad}; allowed: {sorted(allowed)}", file=sys.stderr)
            sys.exit(2)
    if any(manual[k] for k in ("platforms", "stack_groups", "product_hints")):
        proj = proj or {"stack_groups": [], "platforms": [], "product_hints": [], "findings": []}
        for k in ("platforms", "stack_groups", "product_hints"):
            proj[k] = list(dict.fromkeys(list(proj.get(k, [])) + manual[k]))
        proj["findings"] = list(proj.get("findings", [])) + [{"status": "KNOWN", "note": "manual hint: " + ", ".join(manual["platforms"] + manual["stack_groups"] + manual["product_hints"])}]
    return proj


def _finish(status: str, args) -> None:
    sys.exit(0 if getattr(args, "exit_zero", False) else STATUS_EXIT.get(status, 0))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--project", help="inspect_project.py JSON output")
        p.add_argument("--platform", action="append")
        p.add_argument("--stack", action="append")
        p.add_argument("--product", action="append")
        p.add_argument("--json", action="store_true")
        p.add_argument("--explain", action="store_true")
        p.add_argument("--exit-zero", action="store_true")

    p = sub.add_parser("requirements"); p.add_argument("request"); common(p)
    p.add_argument("--pretty", action="store_true", help="indented JSON (default is compact one-line JSON)")
    p.add_argument("--full", action="store_true", help="emit the full object including evidence maps")
    p = sub.add_parser("classify"); p.add_argument("request"); common(p)
    p = sub.add_parser("search"); p.add_argument("request"); common(p)
    p.add_argument("-k", type=int, default=5)
    p.add_argument("--kind", action="append", choices=sorted(core.KINDS))
    p.add_argument("--category", action="append")
    p.add_argument("--per-category", type=int, default=2)
    p.add_argument("--no-facets", action="store_true", help="disable facet-aware result composition")
    p = sub.add_parser("guidance"); p.add_argument("request"); common(p)
    p.add_argument("--size", type=int, help="override the bundle cap (default variable 5-8 by required concerns)")
    p = sub.add_parser("direction"); p.add_argument("request"); common(p)
    p.add_argument("--brand")
    p.add_argument("--out", help="write direction JSON (with fingerprint) to this path")
    p = sub.add_parser("show"); p.add_argument("record_id")
    args = ap.parse_args(argv)

    try:
        records = core.load_records()
    except ValueError as e:
        print(f"error: knowledge data is broken: {e}", file=sys.stderr)
        sys.exit(1)

    if args.cmd == "show":
        rec = next((r for r in records if r["id"] == args.record_id), None)
        if not rec:
            close = [r["id"] for r in records if args.record_id in r["id"]][:8]
            print(f"error: no record '{args.record_id}'. Similar: {close}", file=sys.stderr)
            sys.exit(2)
        print(json.dumps({k: v for k, v in rec.items() if not k.startswith("_")}, indent=2, ensure_ascii=False))
        return

    if not args.request.strip():
        print("error: empty request", file=sys.stderr)
        sys.exit(2)
    project = _project(args)
    req = core.build_requirements(args.request, project=project)
    errs = core.validate_requirements(req)
    if errs:
        print("error: requirements object failed schema validation: " + "; ".join(errs), file=sys.stderr)
        sys.exit(1)

    if args.cmd == "requirements":
        payload = req if args.full else core.compact_requirements(req, explain=args.explain)
        print(json.dumps(payload, indent=2 if (args.pretty or args.full) else None, ensure_ascii=False))
        _finish(core.requirements_status(req), args)

    if args.cmd == "classify":
        sig = core._signals_view(req)
        if args.json:
            sig = {k: v for k, v in sig.items() if k != "requirements"}
            print(json.dumps(sig, indent=2, ensure_ascii=False))
        else:
            print(json.dumps({"signals": core._compact_signals(req), "activation": req["activation"],
                              "missing": [f"{m['field']}: {m['reason']}" for m in req["missing"]], "status": core.requirements_status(req)}, indent=2))
        _finish(core.requirements_status(req), args)

    if args.cmd == "search":
        res = core.search(args.request, records, k=args.k, requirements=req,
                          kinds=set(args.kind) if args.kind else None,
                          categories=set(args.category) if args.category else None,
                          per_category=args.per_category, explain=args.explain, facets=not args.no_facets)
        print(json.dumps(res, indent=2, ensure_ascii=False) if args.json else core.format_search_md(res))
        _finish(res["status"], args)

    if args.cmd == "guidance":
        g = core.guidance(args.request, records, requirements=req, explain=args.explain, size=args.size)
        print(json.dumps(g, indent=2, ensure_ascii=False) if args.json else core.format_guidance_md(g))
        _finish(g["status"], args)

    if args.cmd == "direction":
        d = core.direction(args.request, records=records, explain=args.explain, brand_hint=args.brand, requirements=req)
        if args.out:
            payload = {"brand": args.brand or args.request, "fingerprint": d["fingerprint"],
                       "direction": {k: (v["id"] if v else None) for k, v in d["direction"].items()},
                       "requirements": core.compact_requirements(req), "validation": d["validation"]}
            Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print(f"wrote {args.out}", file=sys.stderr)
        print(json.dumps(d, indent=2, ensure_ascii=False) if args.json else core.format_direction_md(d))
        status = core.requirements_status(req)
        if not d["validation"]["ok"] and status == "CONFIDENT":
            status = "PARTIAL"
        _finish(status, args)


if __name__ == "__main__":
    main()
