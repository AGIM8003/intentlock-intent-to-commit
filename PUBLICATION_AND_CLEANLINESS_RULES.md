# PUBLICATION_AND_CLEANLINESS_RULES.md — 01.PUBLISHED PROJECTS

**Authority:** Already-published Zenodo / Google Scholar projects (public GitHub)  
**Author:** Haxhijaha, Agim · ORCID `0009-0002-3234-7765`

These projects are **already published**. Repos stay **public**. Do not make them private. Do not “close” deposits.

---

## Locked rules

1. **Publication status:** Already on Zenodo + Scholar — improve code without inventing a new DOI unless owner requests a versioned update.  
2. **Repos visibility:** **PUBLIC** — never `gh repo edit --visibility private` on these nine.  
3. **Blueprint forever:** never delete/stub research edition / blueprint markdown; lives **outside** `CODE FOLDER/`.  
4. **Blueprint ↔ code map:** maintain `CODE FOLDER/BLUEPRINT_CODE_MAP.md` after code changes.  
5. **Clean tree:** no double folders, zip dumps, `evidence/v*` sprawl.  
6. **Canonical code:** new work in `CODE FOLDER/`; `poc/` is legacy mirror until fully migrated.  
7. **Honesty:** not production unless proven; do not claim patent grants.

## Required layout

```
<PROJECT>_PUBLICATION_PACKAGE_*/
  AGENTS.md
  RULES.md
  IMPLEMENTATION_STATUS.md
  <blueprint / public research edition>.md   ← NEVER DELETE
  CODE FOLDER/
    BUILD_AND_IMPROVE.md
    BLUEPRINT_CODE_MAP.md
    src/<package>/
    tests/
    run_tests.py
    evidence/CURRENT/
  poc/   ← legacy
```

## XP-AEGIS patent-first package

`XP-AEGIS_OS_PCOL_v05_PATENT_FIRST_PACKAGE` is **not** one of the nine published Zenodo libraries — do not treat it as a public research CODE FOLDER target unless the owner says so.
