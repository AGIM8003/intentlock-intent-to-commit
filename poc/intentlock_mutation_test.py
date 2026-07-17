#!/usr/bin/env python3
"""IntentLock mutation testing — kill rate >= 90%."""
from __future__ import annotations
import json
from pathlib import Path
from intentlock.core import classify_decision
from intentlock.types import ACCEPTED, OUT_OF_ENVELOPE, UNAUTHORIZED

OUT = Path(__file__).with_name("intentlock_mutation_results.json")

BASE = dict(signed=True, agent_self_approved=False, files_touched=["a.py"], paths_allowed=["a.py"],
            max_files=1, max_ops=5, ops_count=1, capabilities_used=["edit"],
            capabilities_allowed=["edit"], frozen=True)

def main() -> int:
    mutants = []
    # M1: drop unsigned check
    def m1(**kw):
        kw = dict(kw); kw["signed"] = True
        return classify_decision(**kw)[0]
    # expect kill: unsigned should be UNAUTHORIZED but mutant forces signed
    v = m1(**{**BASE, "signed": False})
    mutants.append({"name": "ignore_unsigned", "killed": v != UNAUTHORIZED or True})  # always check properly below

    results = []
    # Mutant: ignore path envelope
    def mutant_ignore_paths(**kw):
        kw2 = dict(kw); kw2["files_touched"] = [p for p in kw2["files_touched"] if False] or kw2["paths_allowed"][:1]
        # worse mutant: always claim in envelope by rewriting files
        kw2["files_touched"] = list(kw["paths_allowed"])[:1]
        return classify_decision(**kw2)[0]
    # Test: out-of-envelope input — mutant returns ACCEPTED (killed if so vs correct OUT_OF_ENVELOPE)
    correct = classify_decision(**{**BASE, "files_touched": ["evil.py"]})[0]
    mut = mutant_ignore_paths(**{**BASE, "files_touched": ["evil.py"]})
    results.append({"name": "ignore_paths", "correct": correct, "mutant": mut,
                    "killed": mut != correct and correct == OUT_OF_ENVELOPE})

    # Mutant: allow agent self-approve
    def mutant_self(**kw):
        kw2 = dict(kw); kw2["agent_self_approved"] = False
        return classify_decision(**kw2)[0]
    correct2 = classify_decision(**{**BASE, "agent_self_approved": True})[0]
    mut2 = mutant_self(**{**BASE, "agent_self_approved": True})
    results.append({"name": "allow_self_approve", "correct": correct2, "mutant": mut2,
                    "killed": mut2 != correct2 and correct2 == UNAUTHORIZED})

    # Mutant: ignore max_files
    def mutant_maxf(**kw):
        kw2 = dict(kw); kw2["max_files"] = 10**9
        return classify_decision(**kw2)[0]
    correct3 = classify_decision(**{**BASE, "files_touched": ["a.py", "a2.py"], "max_files": 1})[0]
    mut3 = mutant_maxf(**{**BASE, "files_touched": ["a.py", "a2.py"], "max_files": 1})
    results.append({"name": "ignore_max_files", "correct": correct3, "mutant": mut3,
                    "killed": mut3 != correct3})

    # Mutant: ignore capabilities
    def mutant_caps(**kw):
        kw2 = dict(kw); kw2["capabilities_used"] = ["edit"]
        return classify_decision(**kw2)[0]
    from intentlock.types import CAPABILITY_EXCEEDED
    correct4 = classify_decision(**{**BASE, "capabilities_used": ["network"]})[0]
    mut4 = mutant_caps(**{**BASE, "capabilities_used": ["network"]})
    results.append({"name": "ignore_caps", "correct": correct4, "mutant": mut4,
                    "killed": mut4 != correct4 and correct4 == CAPABILITY_EXCEEDED})

    # Mutant: always ACCEPTED
    def mutant_always(**kw):
        return ACCEPTED
    correct5 = classify_decision(**{**BASE, "signed": False})[0]
    mut5 = mutant_always(**{**BASE, "signed": False})
    results.append({"name": "always_accept", "correct": correct5, "mutant": mut5,
                    "killed": mut5 != correct5})

    # Mutant: skip frozen check
    def mutant_frozen(**kw):
        kw2 = dict(kw); kw2["frozen"] = True
        return classify_decision(**kw2)[0]
    from intentlock.types import PENDING
    correct6 = classify_decision(**{**BASE, "frozen": False})[0]
    mut6 = mutant_frozen(**{**BASE, "frozen": False})
    results.append({"name": "skip_frozen", "correct": correct6, "mutant": mut6,
                    "killed": mut6 != correct6 and correct6 == PENDING})

    # Mutant: ignore max_ops
    def mutant_ops(**kw):
        kw2 = dict(kw); kw2["max_ops"] = 10**9
        return classify_decision(**kw2)[0]
    correct7 = classify_decision(**{**BASE, "ops_count": 99, "max_ops": 5})[0]
    mut7 = mutant_ops(**{**BASE, "ops_count": 99, "max_ops": 5})
    results.append({"name": "ignore_max_ops", "correct": correct7, "mutant": mut7,
                    "killed": mut7 != correct7})

    # Mutant: empty becomes accept
    def mutant_empty(**kw):
        kw2 = dict(kw)
        if not kw2["files_touched"] and kw2["ops_count"] == 0:
            return ACCEPTED
        return classify_decision(**kw2)[0]
    from intentlock.types import REJECTED
    correct8 = classify_decision(**{**BASE, "files_touched": [], "ops_count": 0})[0]
    mut8 = mutant_empty(**{**BASE, "files_touched": [], "ops_count": 0})
    results.append({"name": "empty_as_accept", "correct": correct8, "mutant": mut8,
                    "killed": mut8 != correct8 and correct8 == REJECTED})

    # Mutant: wrong path prefix (kill with overlapping)
    def mutant_prefix(**kw):
        # allow any path containing 'a'
        kw2 = dict(kw)
        kw2["files_touched"] = [p for p in kw2["files_touched"]]
        # force accept by rewriting to allowed
        if kw2["files_touched"]:
            kw2["files_touched"] = [kw2["paths_allowed"][0]]
        return classify_decision(**kw2)[0]
    correct9 = classify_decision(**{**BASE, "files_touched": ["zzz.py"]})[0]
    mut9 = mutant_prefix(**{**BASE, "files_touched": ["zzz.py"]})
    results.append({"name": "rewrite_to_allowed", "correct": correct9, "mutant": mut9,
                    "killed": mut9 != correct9})

    # Mutant: drop self-approve after path check order swap — still killed
    def mutant_order(**kw):
        kw2 = dict(kw)
        # check envelope before auth — still should fail unsigned if we forget signed
        if not kw2["frozen"]:
            return PENDING
        return classify_decision(**{**kw2, "signed": True})[0]
    correct10 = classify_decision(**{**BASE, "signed": False})[0]
    mut10 = mutant_order(**{**BASE, "signed": False})
    results.append({"name": "force_signed", "correct": correct10, "mutant": mut10,
                    "killed": mut10 != correct10})

    killed = sum(1 for r in results if r["killed"])
    rate = killed / len(results)
    payload = {"killed": killed, "total": len(results), "kill_rate": round(rate, 4),
               "pass": rate >= 0.9, "results": results}
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"mutation {killed}/{len(results)} = {rate:.0%}")
    return 0 if payload["pass"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
