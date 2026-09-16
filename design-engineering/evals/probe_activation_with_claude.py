#!/usr/bin/env python3
"""Optional live activation probe: asks a real Claude model whether the installed skill's
description would be selected for each activation eval prompt.

  python evals/probe_activation_with_claude.py [--model claude-haiku-4-5-20251001] [--limit N]

Requires the `claude` CLI on PATH and the skill's SKILL.md (its frontmatter description is
sent verbatim). Costs tokens; not part of run_evals.py. The deterministic proxy in
run_evals.py is the permanent gate; this probe is evidence that the description and the
proxy agree with real model routing. Prints agreement per case and a summary.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def description() -> str:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"^description:\s*(.+)$", text, re.M)
    return m.group(1).strip().strip('"') if m else ""


def ask(model: str, prompt: str) -> str:
    proc = subprocess.run(["claude", "-p", "--model", model, "--output-format", "text", prompt],
                          capture_output=True, text=True, encoding="utf-8", timeout=120)
    return (proc.stdout or proc.stderr).strip()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="claude-haiku-4-5-20251001")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args(argv)
    desc = description()
    cases = json.loads((SKILL / "evals" / "cases" / "activation.json").read_text(encoding="utf-8"))["cases"]
    if args.limit:
        cases = cases[: args.limit]
    agree = total = 0
    for c in cases:
        q = (f"You are a coding agent choosing whether to load a skill. The skill's description is:\n\n{desc}\n\n"
             f"The user's request is: \"{c['prompt']}\"\n\nWould you load this skill for that request? "
             "Answer with exactly one word: YES or NO.")
        try:
            out = ask(args.model, q)
        except (OSError, subprocess.TimeoutExpired) as e:
            print(f"! {c['id']}: probe failed ({e})")
            continue
        if not re.search(r"\b(YES|NO)\b", out, re.I):
            sys.exit(f"probe invalid: the claude CLI did not answer YES/NO for {c['id']!r}. Raw output: {out[:200]!r}. "
                     "Typical cause: CLI not logged in for non-interactive use (run `claude` interactively once, or set an API key).")
        got = "activate" if re.search(r"\bYES\b", out, re.I) else "skip"
        expected = c["expect"]
        ok = expected == "ambiguous" or got == expected
        if expected != "ambiguous":
            total += 1
            agree += int(ok)
        print(f"{'✓' if ok else '✗'} {c['id']}: expected {expected}, model {got}")
    print(f"agreement on non-ambiguous cases: {agree}/{total}")


if __name__ == "__main__":
    main()
