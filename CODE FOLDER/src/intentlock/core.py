"""IntentLock core: Diff Envelope + acceptance boundary.
Author: Haxhijaha, Agim ORCID 0009-0002-3234-7765
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .types import (
    ACCEPTED,
    CAPABILITY_EXCEEDED,
    OUT_OF_ENVELOPE,
    PENDING,
    REJECTED,
    UNAUTHORIZED,
)


def contract_digest(task: str, human_id: str, paths: list[str], max_files: int, max_ops: int) -> str:
    payload = f"{task}|{human_id}|{','.join(sorted(paths))}|{max_files}|{max_ops}"
    return hashlib.sha256(payload.encode()).hexdigest()


def path_allowed(path: str, allowed: list[str]) -> bool:
    for prefix in allowed:
        if path == prefix or path.startswith(prefix.rstrip("/") + "/") or path.startswith(prefix):
            return True
    return False


def classify_decision(
    *,
    signed: bool,
    agent_self_approved: bool,
    files_touched: list[str],
    paths_allowed: list[str],
    max_files: int,
    max_ops: int,
    ops_count: int,
    capabilities_used: list[str],
    capabilities_allowed: list[str],
    frozen: bool,
) -> tuple[str, list[str]]:
    if not signed:
        return UNAUTHORIZED, ["intent contract not signed by human"]
    if agent_self_approved:
        return UNAUTHORIZED, ["agent cannot be acceptance authority for its own work"]
    if not frozen:
        return PENDING, ["candidate not frozen"]
    out_paths = [p for p in files_touched if not path_allowed(p, paths_allowed)]
    if out_paths:
        return OUT_OF_ENVELOPE, [f"paths outside Diff Envelope: {out_paths[:5]}"]
    if len(files_touched) > max_files:
        return OUT_OF_ENVELOPE, [f"file count {len(files_touched)} exceeds max_files {max_files}"]
    if ops_count > max_ops:
        return OUT_OF_ENVELOPE, [f"ops_count {ops_count} exceeds max_ops {max_ops}"]
    bad_caps = [c for c in capabilities_used if c not in capabilities_allowed]
    if bad_caps:
        return CAPABILITY_EXCEEDED, [f"capabilities not granted: {bad_caps}"]
    if not files_touched and ops_count == 0:
        return REJECTED, ["empty candidate — nothing to accept"]
    return ACCEPTED, ["within Diff Envelope; independent acceptance boundary OK"]


def json_stable(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def capsule_digest(parts: dict[str, Any]) -> str:
    return hashlib.sha256(json_stable(parts).encode()).hexdigest()
