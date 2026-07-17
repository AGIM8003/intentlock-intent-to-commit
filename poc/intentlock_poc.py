#!/usr/bin/env python3
"""IntentLock minimal PoC — Diff Envelope acceptance."""
from __future__ import annotations
import json
from pathlib import Path
from intentlock import IntentLockEngine, ACCEPTED, OUT_OF_ENVELOPE

OUT = Path(__file__).with_name("intentlock_evidence.json")

def main() -> int:
    e = IntentLockEngine()
    e.create_intent("IC1", task="fix README typo", human_id="alice",
                    paths_allowed=["README.md"], max_files=1, max_ops=5)
    e.compile_policy("IC1")
    e.record_unit("IC1", "U1", op="edit", path="README.md")
    e.freeze_candidate("IC1", "C1")
    ok = e.accept("IC1")
    e2 = IntentLockEngine()
    e2.create_intent("IC2", task="fix README", human_id="alice",
                     paths_allowed=["README.md"], max_files=1)
    e2.compile_policy("IC2")
    e2.freeze_candidate("IC2", "C2", files_touched=["src/secret.py"], ops_count=1)
    bad = e2.accept("IC2")
    payload = {
        "ok_verdict": ok["verdict"],
        "bad_verdict": bad["verdict"],
        "ok_capsule": ok["capsule_digest"][:16],
        "pass": ok["verdict"] == ACCEPTED and bad["verdict"] == OUT_OF_ENVELOPE,
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("PoC", payload)
    return 0 if payload["pass"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
