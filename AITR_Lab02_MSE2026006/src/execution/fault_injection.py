"""Controlled fault injection module for G4 experimental protocol.

Implements the four preregistered one-shot fault classes:
1. missing_field: drops a required dictionary key.
2. type_corruption: replaces declared data type with incompatible type.
3. numeric_corruption: perturbs a numerical value outside invariant bounds.
4. broken_reference: alters a foreign reference key to a nonexistent entity.

Ground truth is retained strictly for independent evaluation;
the verifier and executor cannot access fault labels, targets, or parameters.
"""

import copy
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class FaultDescriptor:
    """Ground-truth specification of an injected fault."""
    fault_type: str  # 'missing_field', 'type_corruption', 'numeric_corruption', 'broken_reference'
    target_node_id: str
    position_bin: str  # 'early', 'middle', 'late'
    parameter_field: str = ""
    is_contract_violating: bool = True
    disarmed: bool = False
    injected_at_step: Optional[int] = None

    def to_evaluator_dict(self) -> Dict[str, Any]:
        """Evaluator-only serialization of fault ground truth."""
        return {
            "fault_type": self.fault_type,
            "target_node_id": self.target_node_id,
            "position_bin": self.position_bin,
            "parameter_field": self.parameter_field,
            "is_contract_violating": self.is_contract_violating,
            "disarmed": self.disarmed,
            "injected_at_step": self.injected_at_step,
        }


class FaultInjector:
    """Applies a controlled one-shot fault mutation to a node's output artifact."""

    def __init__(self, fault_descriptor: Optional[FaultDescriptor] = None):
        self.fault_descriptor = fault_descriptor
        self.has_injected = False

    def disarm(self) -> None:
        """Disarm the injector (used during rollback replay)."""
        if self.fault_descriptor:
            self.fault_descriptor.disarmed = True

    def inject_if_target(self, node_id: str, step_idx: int, raw_output: Any) -> Any:
        """Apply mutation if node_id matches target and injector is armed."""
        if not self.fault_descriptor:
            return raw_output

        if self.fault_descriptor.disarmed or self.has_injected:
            return raw_output

        if node_id != self.fault_descriptor.target_node_id:
            return raw_output

        # Perform one-shot mutation
        mutated_output = copy.deepcopy(raw_output)
        ftype = self.fault_descriptor.fault_type

        if ftype == "missing_field":
            # Remove records or primary payload key
            if isinstance(mutated_output, dict):
                target_key = self.fault_descriptor.parameter_field or "records"
                mutated_output.pop(target_key, None)

        elif ftype == "type_corruption":
            # Corrupt type of a key
            if isinstance(mutated_output, dict):
                target_key = self.fault_descriptor.parameter_field or "records"
                mutated_output[target_key] = 123456789  # int instead of list/dict/str

        elif ftype == "numeric_corruption":
            # Invariant breach: set value negative or extreme
            if isinstance(mutated_output, dict) and "records" in mutated_output:
                recs = mutated_output["records"]
                if isinstance(recs, list) and recs:
                    recs[0]["value"] = -9999.0  # violates min_value >= 0.0

        elif ftype == "broken_reference":
            # Corrupt join / foreign key
            if isinstance(mutated_output, dict) and "records" in mutated_output:
                recs = mutated_output["records"]
                if isinstance(recs, list) and recs:
                    recs[0]["record_id"] = -88888  # nonexistent reference ID

        self.has_injected = True
        self.fault_descriptor.injected_at_step = step_idx
        return mutated_output
