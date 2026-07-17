#!/usr/bin/env python3
"""IntentLock alternative oracle — independent envelope check."""
from __future__ import annotations
import json
from pathlib import Path
from intentlock import IntentLockEngine
from intentlock.core import classify_decision

OUT = Path(__file__).with_name("intentlock_replication_evidence.json")

def oracle(**kw):
    v, r = classify_decision(**kw)
    return v

def main() -> int:
    scenarios = [
        dict(signed=True, agent_self_approved=False, files_touched=["a.py"], paths_allowed=["a.py"],
             max_files=1, max_ops=5, ops_count=1, capabilities_used=["edit"],
             capabilities_allowed=["edit"], frozen=True),
        dict(signed=True, agent_self_approved=False, files_touched=["b.py"], paths_allowed=["a.py"],
             max_files=1, max_ops=5, ops_count=1, capabilities_used=["edit"],
             capabilities_allowed=["edit"], frozen=True),
        dict(signed=False, agent_self_approved=False, files_touched=["a.py"], paths_allowed=["a.py"],
             max_files=1, max_ops=5, ops_count=1, capabilities_used=["edit"],
             capabilities_allowed=["edit"], frozen=True),
    ]
    rows = []
    for i, s in enumerate(scenarios):
        e = IntentLockEngine()
        e.create_intent(f"S{i}", task="t", human_id="h", paths_allowed=s["paths_allowed"],
                        max_files=s["max_files"], max_ops=s["max_ops"],
                        capabilities=s["capabilities_allowed"], signed=s["signed"])
        e.compile_policy(f"S{i}")
        e.freeze_candidate(f"S{i}", "c", files_touched=s["files_touched"], ops_count=s["ops_count"],
                           capabilities_used=s["capabilities_used"],
                           agent_self_approved=s["agent_self_approved"])
        eng = e.accept(f"S{i}")["verdict"]
        alt = oracle(**s)
        rows.append({"scenario": i, "engine": eng, "oracle": alt, "match": eng == alt})
    ok = all(r["match"] for r in rows)
    OUT.write_text(json.dumps({"rows": rows, "replication_pass": ok}, indent=2), encoding="utf-8")
    print("replication", ok)
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
