"""Every-Step verification scheduler (Arm D — High-Frequency Reference).

Allocates H check slots on the forward pass (verification after every step).
Represents the maximal-frequency verification anchor with highest check overhead.
"""

from typing import Optional, Tuple


class EveryStepScheduler:
    """Invokes verification after each forward node execution (H check slots)."""

    def __init__(self, horizon: int):
        self.horizon = horizon
        self.allocated_slots = horizon

    def get_scheduled_steps(self) -> Tuple[int, ...]:
        """Return all execution step indices where checks occur."""
        return tuple(range(1, self.horizon + 1))

    def should_check(self, step_idx: int, node_id: str) -> Tuple[bool, Optional[int]]:
        """Verify after every single step 1..H."""
        if 1 <= step_idx <= self.horizon:
            return True, step_idx
        return False, None
