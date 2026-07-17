#!/usr/bin/env python3
"""IntentLock benchmark harness."""
from __future__ import annotations
import json, time
from pathlib import Path
from intentlock import IntentLockEngine, ACCEPTED

OUT = Path(__file__).with_name("intentlock_benchmark_results.json")

def main() -> int:
    cases = []
    e = IntentLockEngine()
    t0 = time.perf_counter()
    e.create_intent("B", task="bulk", human_id="h", paths_allowed=["src/"], max_files=500, max_ops=2000)
    e.compile_policy("B")
    files = [f"src/f{i}.py" for i in range(200)]
    for i, f in enumerate(files):
        e.record_unit("B", f"U{i}", op="edit", path=f)
    e.freeze_candidate("B", "C")
    d = e.accept("B")
    t1 = time.perf_counter()
    cases.append({"name": "200_files_accept", "pass": d["verdict"] == ACCEPTED, "seconds": round(t1-t0, 6)})
    OUT.write_text(json.dumps({"cases": cases, "all_pass": all(c["pass"] for c in cases)}, indent=2), encoding="utf-8")
    print(cases)
    return 0 if all(c["pass"] for c in cases) else 1

if __name__ == "__main__":
    raise SystemExit(main())
