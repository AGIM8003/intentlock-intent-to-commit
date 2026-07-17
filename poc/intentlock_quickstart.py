#!/usr/bin/env python3
"""IntentLock 2-minute quickstart."""
from intentlock import IntentLockEngine

e = IntentLockEngine()
e.create_intent("QS", task="Update CHANGELOG.md", human_id="you",
                paths_allowed=["CHANGELOG.md"], max_files=1)
e.compile_policy("QS")
e.record_unit("QS", "U1", op="edit", path="CHANGELOG.md")
e.freeze_candidate("QS", "C1")
d = e.accept("QS")
print("Verdict:", d["verdict"])
print("Capsule:", d["capsule_digest"][:24], "...")
print("Reasons:", "; ".join(d["reasons"]))
