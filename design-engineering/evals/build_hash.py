#!/usr/bin/env python3
"""Print the combined sha256 of the frozen skill build (scripts + knowledge + lexicon + thresholds).
Used by the real-project protocol: agents record the hash at the start and end of a task so a
run on a modified build is detectable. `--json` prints per-file hashes too."""
import hashlib, json, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
FILES = sorted([*(SKILL / "scripts").glob("*.py"), *(SKILL / "data").glob("*.jsonl"), SKILL / "data" / "lexicon.json",
                SKILL / "SKILL.md", SKILL / "evals" / "heldout-v4" / "THRESHOLDS.md", SKILL / "evals" / "heldout-v4" / "ONTOLOGY.md"])


def main(argv=None):
    per = {}
    combined = hashlib.sha256()
    for f in FILES:
        if not f.exists():
            continue
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        per[str(f.relative_to(SKILL)).replace("\\", "/")] = h
        combined.update(f"{f.name}:{h}\n".encode())
    out = {"build_sha256": combined.hexdigest(), "files": per}
    if "--json" in (argv or sys.argv[1:]):
        print(json.dumps(out, indent=1))
    else:
        print(out["build_sha256"])


if __name__ == "__main__":
    main()
