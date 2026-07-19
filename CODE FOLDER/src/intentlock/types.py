"""IntentLock types. Author: Haxhijaha, Agim ORCID 0009-0002-3234-7765"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

ACCEPTED = "ACCEPTED"
REJECTED = "REJECTED"
OUT_OF_ENVELOPE = "OUT_OF_ENVELOPE"
UNAUTHORIZED = "UNAUTHORIZED"
CAPABILITY_EXCEEDED = "CAPABILITY_EXCEEDED"
PENDING = "PENDING"

VERDICTS = {
    ACCEPTED,
    REJECTED,
    OUT_OF_ENVELOPE,
    UNAUTHORIZED,
    CAPABILITY_EXCEEDED,
    PENDING,
}


@dataclass
class IntentContract:
    contract_id: str
    task: str
    human_id: str
    paths_allowed: list[str]
    max_files: int
    max_ops: int
    capabilities: list[str]
    signed: bool = True
    digest: str = ""


@dataclass
class ExecutionUnit:
    unit_id: str
    op: str
    path: str
    capability: str


@dataclass
class Candidate:
    candidate_id: str
    files_touched: list[str]
    ops_count: int
    capabilities_used: list[str]
    agent_self_approved: bool = False


@dataclass
class Decision:
    verdict: str
    reasons: list[str]
    capsule_digest: str
    contract_id: str
    limits: str
    details: dict[str, Any] = field(default_factory=dict)
