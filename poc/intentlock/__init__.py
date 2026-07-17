"""IntentLock research library — intent-to-commit control.
Author: Haxhijaha, Agim ORCID 0009-0002-3234-7765
"""
from .engine import IntentLockEngine
from .types import (
    ACCEPTED,
    CAPABILITY_EXCEEDED,
    OUT_OF_ENVELOPE,
    PENDING,
    REJECTED,
    UNAUTHORIZED,
)

__version__ = "6.0.0"
__all__ = [
    "IntentLockEngine",
    "ACCEPTED",
    "REJECTED",
    "OUT_OF_ENVELOPE",
    "UNAUTHORIZED",
    "CAPABILITY_EXCEEDED",
    "PENDING",
    "__version__",
]
