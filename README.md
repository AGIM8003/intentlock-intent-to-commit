# IntentLock v6.0.0

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21361708.svg)](https://doi.org/10.5281/zenodo.21361708)

**Deterministic intent-to-commit control** for AI-assisted software development: signed Intent Contracts, Diff Envelopes, independent acceptance, offline proof capsules.

## Authoritative documents

- SSOT: `INTENTLOCK_v6.0.0_PUBLIC_RESEARCH_EDITION.md`
- API: `INTENTLOCK_API_REFERENCE.md`
- Evidence: `poc/`

## Quickstart

```bash
cd poc
python intentlock_quickstart.py
```

```python
from intentlock import IntentLockEngine
e = IntentLockEngine()
e.create_intent("QS", task="Update CHANGELOG.md", human_id="you", paths_allowed=["CHANGELOG.md"], max_files=1)
e.compile_policy("QS")
e.record_unit("QS", "U1", op="edit", path="CHANGELOG.md")
e.freeze_candidate("QS", "C1")
print(e.accept("QS")["verdict"])
```

## Citation

Haxhijaha, Agim. *IntentLock*. v6.0.0. DOI: [10.5281/zenodo.21361708](https://doi.org/10.5281/zenodo.21361708)

## Honest limits

Not production, not peer reviewed, not independently replicated, not universal agent security. The agent that produced a change is never the acceptance authority.

## License

CC BY-NC-ND 4.0 · ORCID 0009-0002-3234-7765 · agim@vertogroup.ai
