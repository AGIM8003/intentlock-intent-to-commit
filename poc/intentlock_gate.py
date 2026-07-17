#!/usr/bin/env python3
"""IntentLock Reality Gate — 8 controlled tests."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from intentlock import (
    ACCEPTED, CAPABILITY_EXCEEDED, OUT_OF_ENVELOPE, PENDING, REJECTED,
    UNAUTHORIZED, IntentLockEngine,
)

OUT = Path(__file__).with_name("intentlock_gate_results.json")

def t(name, fn):
    try:
        return {"name": name, "pass": bool(fn()), "error": None}
    except Exception as e:
        return {"name": name, "pass": False, "error": str(e)}

def main() -> int:
    def t1():
        e = IntentLockEngine()
        e.create_intent("A", task="edit readme", human_id="h", paths_allowed=["README.md"], max_files=1)
        e.compile_policy("A"); e.freeze_candidate("A", "c", files_touched=["README.md"], ops_count=1)
        return e.accept("A")["verdict"] == ACCEPTED
    def t2():
        e = IntentLockEngine()
        e.create_intent("A", task="edit", human_id="h", paths_allowed=["README.md"], max_files=1)
        e.compile_policy("A"); e.freeze_candidate("A", "c", files_touched=["src/x.py"], ops_count=1)
        return e.accept("A")["verdict"] == OUT_OF_ENVELOPE
    def t3():
        e = IntentLockEngine()
        e.create_intent("A", task="edit", human_id="h", paths_allowed=["src/"], max_files=1, signed=False)
        e.compile_policy("A"); e.freeze_candidate("A", "c", files_touched=["src/a.py"], ops_count=1)
        return e.accept("A")["verdict"] == UNAUTHORIZED
    def t4():
        e = IntentLockEngine()
        e.create_intent("A", task="edit", human_id="h", paths_allowed=["src/"], max_files=2)
        e.compile_policy("A")
        e.freeze_candidate("A", "c", files_touched=["src/a.py"], ops_count=1, agent_self_approved=True)
        return e.accept("A")["verdict"] == UNAUTHORIZED
    def t5():
        e = IntentLockEngine()
        e.create_intent("A", task="edit", human_id="h", paths_allowed=["src/"], max_files=1,
                        capabilities=["edit"])
        e.compile_policy("A")
        e.freeze_candidate("A", "c", files_touched=["src/a.py"], ops_count=1,
                           capabilities_used=["network"])
        return e.accept("A")["verdict"] == CAPABILITY_EXCEEDED
    def t6():
        e = IntentLockEngine()
        e.create_intent("A", task="edit", human_id="h", paths_allowed=["src/"], max_files=1)
        e.compile_policy("A")
        return e.accept("A")["verdict"] == PENDING
    def t7():
        e = IntentLockEngine()
        e.create_intent("A", task="edit", human_id="h", paths_allowed=["src/"], max_files=1)
        e.compile_policy("A"); e.freeze_candidate("A", "c", files_touched=[], ops_count=0)
        return e.accept("A")["verdict"] == REJECTED
    def t8():
        e = IntentLockEngine()
        e.create_intent("A", task="edit", human_id="h", paths_allowed=["src/"], max_files=5, max_ops=2)
        e.compile_policy("A"); e.freeze_candidate("A", "c", files_touched=["src/a.py"], ops_count=9)
        return e.accept("A")["verdict"] == OUT_OF_ENVELOPE

    results = [t(n, f) for n, f in [
        ("accepted_in_envelope", t1), ("out_of_envelope_path", t2), ("unsigned_unauthorized", t3),
        ("agent_self_approve_blocked", t4), ("capability_exceeded", t5), ("pending_unfrozen", t6),
        ("empty_rejected", t7), ("ops_over_max", t8),
    ]]
    passed = sum(1 for r in results if r["pass"])
    payload = {
        "gate": "IntentLock Reality Gate",
        "passed": passed,
        "total": len(results),
        "all_pass": passed == len(results),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": results,
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Gate {passed}/{len(results)}")
    return 0 if payload["all_pass"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
