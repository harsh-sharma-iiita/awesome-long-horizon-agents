"""Final-Only verification scheduler (Arm A — Reference Condition).

Allocates exactly one check slot at the terminal acceptance step (H).
Provides the baseline reference for uncontained error propagation with minimal check overhead.
"""

from typing import Optional, Tuple


class FinalOnlyScheduler:
    """Invokes verification solely at terminal workflow completion (1 check slot)."""

    def __init__(self, horizon: int):
        self.horizon = horizon
        self.allocated_slots = 1

    def get_scheduled_steps(self) -> Tuple[int]:
        """Return the execution step index where the terminal check occurs."""
        return (self.horizon,)

    def should_check(self, step_idx: int, node_id: str) -> Tuple[bool, Optional[int]]:
        """Verify only at the final step H."""
        if step_idx == self.horizon:
            return True, 1
        return False, None
