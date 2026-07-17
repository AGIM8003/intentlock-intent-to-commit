#!/usr/bin/env python3
"""IntentLock stress — 2000 execution units."""
from __future__ import annotations
import json, time, tracemalloc
from pathlib import Path
from intentlock import IntentLockEngine, ACCEPTED

OUT = Path(__file__).with_name("intentlock_stress_results.json")

def main() -> int:
    tracemalloc.start()
    e = IntentLockEngine()
    e.create_intent("S", task="stress", human_id="h", paths_allowed=["src/"], max_files=5000, max_ops=5000)
    e.compile_policy("S")
    t0 = time.perf_counter()
    n = 2000
    for i in range(n):
        e.record_unit("S", f"U{i}", op="edit", path=f"src/f{i}.py")
    e.freeze_candidate("S", "C")
    d = e.accept("S")
    elapsed = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    payload = {
        "units": n,
        "verdict": d["verdict"],
        "seconds": round(elapsed, 4),
        "peak_kib": round(peak / 1024, 1),
        "pass": d["verdict"] == ACCEPTED and elapsed < 30,
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(payload)
    return 0 if payload["pass"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
