"""Data classes for verification outcomes and assertion records."""

from dataclasses import dataclass, field
import time
from typing import Any, Dict, List, Optional


@dataclass
class AssertionResult:
    """Outcome of evaluating a single contract assertion."""
    rule_id: str
    rule_type: str
    passed: bool
    message: str = ""
    checked_node_id: str = ""


@dataclass
class VerificationResult:
    """Aggregate result of invoking the deterministic verifier at a checkpoint."""
    passed: bool
    checked_node_id: str
    execution_step_idx: int
    slot_index: int  # 1, 2, or 3
    assertion_results: List[AssertionResult] = field(default_factory=list)
    failed_rule_ids: List[str] = field(default_factory=list)
    failure_details: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize verification result for event logging."""
        return {
            "passed": self.passed,
            "checked_node_id": self.checked_node_id,
            "execution_step_idx": self.execution_step_idx,
            "slot_index": self.slot_index,
            "failed_rule_ids": self.failed_rule_ids,
            "failure_details": self.failure_details,
            "num_assertions_evaluated": len(self.assertion_results),
            "duration_seconds": self.duration_seconds,
            "timestamp": self.timestamp,
        }
