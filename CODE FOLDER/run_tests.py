#!/usr/bin/env python3
from __future__ import annotations
import unittest
from pathlib import Path
HERE = Path(__file__).resolve().parent

def main() -> int:
    suite = unittest.defaultTestLoader.discover(str(HERE / "tests"), pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    raise SystemExit(main())
