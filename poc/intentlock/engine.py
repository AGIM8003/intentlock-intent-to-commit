"""IntentLockEngine — usable research library API.
Author: Haxhijaha, Agim ORCID 0009-0002-3234-7765
"""
from __future__ import annotations

from typing import Any

from .core import capsule_digest, classify_decision, contract_digest
from .types import PENDING, Candidate, Decision, ExecutionUnit, IntentContract
from .validators import require_id, require_paths, require_positive_int, require_text

_LIMITS = (
    "Bounded intent-to-commit control only. IntentLock does not claim universal "
    "agent security, production GRC, peer review, or independent replication. "
    "The agent that produced a change is never the acceptance authority."
)


class IntentLockEngine:
    """Signed Intent Contract -> Diff Envelope -> independent acceptance -> proof capsule.

    Usage:
        e = IntentLockEngine()
        e.create_intent("IC1", task="fix typo in README", human_id="alice",
                        paths_allowed=["README.md"], max_files=1)
        e.compile_policy("IC1")
        e.record_unit("IC1", "U1", op="edit", path="README.md", capability="edit")
        e.freeze_candidate("IC1", "CAND1", files_touched=["README.md"], ops_count=1)
        decision = e.accept("IC1")  # -> ACCEPTED + capsule
    """

    def __init__(self) -> None:
        self._contracts: dict[str, IntentContract] = {}
        self._units: dict[str, list[ExecutionUnit]] = {}
        self._candidates: dict[str, Candidate] = {}
        self._frozen: dict[str, bool] = {}
        self._policies: dict[str, dict[str, Any]] = {}

    def create_intent(
        self,
        contract_id: str,
        *,
        task: str,
        human_id: str,
        paths_allowed: list[str],
        max_files: int = 10,
        max_ops: int = 100,
        capabilities: list[str] | None = None,
        signed: bool = True,
    ) -> IntentContract:
        contract_id = require_id("contract_id", contract_id)
        if contract_id in self._contracts:
            raise ValueError(f"duplicate contract: {contract_id}")
        paths = require_paths(paths_allowed)
        caps = list(capabilities or ["edit", "read"])
        digest = contract_digest(task, human_id, paths, max_files, max_ops)
        c = IntentContract(
            contract_id=contract_id,
            task=require_text("task", task),
            human_id=require_text("human_id", human_id),
            paths_allowed=paths,
            max_files=require_positive_int("max_files", max_files),
            max_ops=require_positive_int("max_ops", max_ops),
            capabilities=caps,
            signed=bool(signed),
            digest=digest,
        )
        self._contracts[contract_id] = c
        self._units[contract_id] = []
        self._frozen[contract_id] = False
        return c

    def _get(self, contract_id: str) -> IntentContract:
        contract_id = require_id("contract_id", contract_id)
        if contract_id not in self._contracts:
            raise ValueError(f"unknown contract: {contract_id}")
        return self._contracts[contract_id]

    def compile_policy(self, contract_id: str) -> dict[str, Any]:
        c = self._get(contract_id)
        pol = {
            "contract_id": c.contract_id,
            "paths_allowed": list(c.paths_allowed),
            "max_files": c.max_files,
            "max_ops": c.max_ops,
            "capabilities": list(c.capabilities),
            "acceptance_authority": "independent_merge_boundary",
            "agent_is_non_authoritative": True,
            "contract_digest": c.digest,
        }
        self._policies[contract_id] = pol
        return dict(pol)

    def record_unit(
        self,
        contract_id: str,
        unit_id: str,
        *,
        op: str,
        path: str,
        capability: str = "edit",
    ) -> ExecutionUnit:
        self._get(contract_id)
        unit_id = require_id("unit_id", unit_id)
        u = ExecutionUnit(
            unit_id=unit_id,
            op=require_text("op", op),
            path=require_text("path", path),
            capability=require_text("capability", capability),
        )
        self._units[contract_id].append(u)
        return u

    def freeze_candidate(
        self,
        contract_id: str,
        candidate_id: str,
        *,
        files_touched: list[str] | None = None,
        ops_count: int | None = None,
        capabilities_used: list[str] | None = None,
        agent_self_approved: bool = False,
    ) -> Candidate:
        self._get(contract_id)
        units = self._units[contract_id]
        files = list(files_touched) if files_touched is not None else sorted({u.path for u in units})
        ops = ops_count if ops_count is not None else len(units)
        caps = list(capabilities_used) if capabilities_used is not None else sorted({u.capability for u in units})
        cand = Candidate(
            candidate_id=require_id("candidate_id", candidate_id),
            files_touched=files,
            ops_count=ops,
            capabilities_used=caps,
            agent_self_approved=bool(agent_self_approved),
        )
        self._candidates[contract_id] = cand
        self._frozen[contract_id] = True
        return cand

    def accept(self, contract_id: str) -> dict[str, Any]:
        c = self._get(contract_id)
        cand = self._candidates.get(contract_id)
        frozen = self._frozen.get(contract_id, False)
        if cand is None:
            verdict, reasons = PENDING, ["no candidate frozen"]
            details: dict[str, Any] = {}
        else:
            verdict, reasons = classify_decision(
                signed=c.signed,
                agent_self_approved=cand.agent_self_approved,
                files_touched=cand.files_touched,
                paths_allowed=c.paths_allowed,
                max_files=c.max_files,
                max_ops=c.max_ops,
                ops_count=cand.ops_count,
                capabilities_used=cand.capabilities_used,
                capabilities_allowed=c.capabilities,
                frozen=frozen,
            )
            details = {
                "files_touched": cand.files_touched,
                "ops_count": cand.ops_count,
                "capabilities_used": cand.capabilities_used,
            }
        parts = {
            "contract_digest": c.digest,
            "policy": self._policies.get(contract_id, {}),
            "verdict": verdict,
            "reasons": reasons,
            "details": details,
            "units": [u.__dict__ for u in self._units.get(contract_id, [])],
        }
        digest = capsule_digest(parts)
        return {
            "verdict": verdict,
            "reasons": reasons,
            "capsule_digest": digest,
            "contract_id": contract_id,
            "limits": _LIMITS,
            "details": details,
        }

    def issue_proof_capsule(self, contract_id: str) -> dict[str, Any]:
        decision = self.accept(contract_id)
        return {
            "type": "intent_to_commit_proof_capsule",
            "contract_id": contract_id,
            "verdict": decision["verdict"],
            "capsule_digest": decision["capsule_digest"],
            "offline_verifiable": True,
            "limits": _LIMITS,
        }
