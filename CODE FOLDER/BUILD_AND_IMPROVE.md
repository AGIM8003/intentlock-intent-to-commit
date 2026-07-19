# BUILD_AND_IMPROVE — intentlock-intent-to-commit

Already published. Keep GitHub **public**. Blueprint outside CODE FOLDER forever.

| Spec | Action |
|---|---|
| 0 | Freeze DOI/repo in AGENTS.md |
| 1 | CODE FOLDER/src canonical + smoke tests |
| 2+ | Improve mechanisms; sync BLUEPRINT_CODE_MAP + blueprint status notes |
| Zenodo | Version bump only with owner approval |

`ash
python run_tests.py
`
"@

  Set-Content -LiteralPath (Join-Path D:\00.AGIM PUBLICATIONS\01.PUBLISHED PROJECTS\INTENTLOCK_PUBLICATION_PACKAGE_2026-07-13\CODE FOLDER 'README.md') -Encoding utf8 -Value @"
# CODE FOLDER — intentlock-intent-to-commit

Canonical software workspace. Blueprint remains outside this folder.

`ash
python run_tests.py
`
"@

  Set-Content -LiteralPath (Join-Path D:\00.AGIM PUBLICATIONS\01.PUBLISHED PROJECTS\INTENTLOCK_PUBLICATION_PACKAGE_2026-07-13\CODE FOLDER 'run_tests.py') -Encoding utf8 -Value @"
#!/usr/bin/env python3
from __future__ import annotations
import unittest
from pathlib import Path
HERE = Path(__file__).resolve().parent

def main() -> int:
    suite = unittest.defaultTestLoader.discover(str(HERE / 'tests'), pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    raise SystemExit(main())
