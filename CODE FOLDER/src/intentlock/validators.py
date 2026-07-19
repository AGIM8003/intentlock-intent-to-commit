"""IntentLock validators. Author: Haxhijaha, Agim ORCID 0009-0002-3234-7765"""
from __future__ import annotations


def require_id(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be non-empty string")
    return value.strip()


def require_text(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be non-empty string")
    return value.strip()


def require_positive_int(name: str, value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be positive int")
    return value


def require_paths(paths: list[str]) -> list[str]:
    if not isinstance(paths, list) or not paths:
        raise ValueError("paths_allowed must be non-empty list")
    out = []
    for p in paths:
        if not isinstance(p, str) or not p.strip():
            raise ValueError("path entries must be non-empty strings")
        out.append(p.strip())
    return out
