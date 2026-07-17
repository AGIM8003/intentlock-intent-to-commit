# IntentLock API Reference (v6.0.0)

## Import

```python
from intentlock import IntentLockEngine, ACCEPTED, OUT_OF_ENVELOPE, UNAUTHORIZED
```

## IntentLockEngine

| Method | Purpose |
|--------|---------|
| `create_intent(id, task=, human_id=, paths_allowed=, max_files=, max_ops=, capabilities=, signed=)` | Create signed Intent Contract |
| `compile_policy(id)` | Compile Diff Envelope + capability policy |
| `record_unit(id, unit_id, op=, path=, capability=)` | Record non-authoritative execution unit |
| `freeze_candidate(id, candidate_id, files_touched=, ops_count=, capabilities_used=, agent_self_approved=)` | Freeze candidate |
| `accept(id)` | Independent acceptance → verdict + capsule digest |
| `issue_proof_capsule(id)` | Offline-verifiable capsule |

## Verdicts

`ACCEPTED`, `REJECTED`, `OUT_OF_ENVELOPE`, `UNAUTHORIZED`, `CAPABILITY_EXCEEDED`, `PENDING`
