#!/usr/bin/env python3
"""IntentLock integration — full capsule path."""
from __future__ import annotations
import json
from pathlib import Path
from intentlock import IntentLockEngine, ACCEPTED

OUT = Path(__file__).with_name("intentlock_integration_results.json")

def main() -> int:
    e = IntentLockEngine()
    e.create_intent("I", task="add test", human_id="h", paths_allowed=["tests/"], max_files=3, max_ops=10)
    pol = e.compile_policy("I")
    e.record_unit("I", "U1", op="create", path="tests/test_new.py")
    e.freeze_candidate("I", "C")
    d = e.accept("I")
    cap = e.issue_proof_capsule("I")
    ok = (
        d["verdict"] == ACCEPTED
        and cap["capsule_digest"] == d["capsule_digest"]
        and pol["agent_is_non_authoritative"] is True
        and len(d["capsule_digest"]) == 64
    )
    OUT.write_text(json.dumps({"pass": ok, "verdict": d["verdict"], "capsule": cap["capsule_digest"][:16]}, indent=2), encoding="utf-8")
    print("integration", ok)
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
