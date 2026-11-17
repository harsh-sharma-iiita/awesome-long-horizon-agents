"""Fixed-Periodic verification scheduler (Arm B — Primary Baseline).

Allocates exactly three check slots on the forward pass:
- Slot 1: ceil(H / 3)
- Slot 2: ceil(2 * H / 3)
- Slot 3: Terminal node execution (H)
"""

import math
from typing import Optional, Tuple


class FixedPeriodicScheduler:
    """Schedules deterministic verification at fixed periodic step intervals."""

    def __init__(self, horizon: int):
        self.horizon = horizon
        self.slot_1_step = math.ceil(horizon / 3)
        self.slot_2_step = math.ceil(2 * horizon / 3)
        self.slot_3_step = horizon
        self.allocated_slots = 3

    def get_scheduled_steps(self) -> Tuple[int, int, int]:
        """Return the exact 1-indexed execution step indices where checks occur."""
        return (self.slot_1_step, self.slot_2_step, self.slot_3_step)

    def should_check(self, step_idx: int, node_id: str) -> Tuple[bool, Optional[int]]:
        """Determine whether verification should run after completing step_idx (1-indexed).

        Returns:
            Tuple[bool, Optional[int]]: (should_verify, slot_index: 1, 2, or 3)
        """
        if step_idx == self.slot_1_step:
            return True, 1
        elif step_idx == self.slot_2_step:
            return True, 2
        elif step_idx == self.slot_3_step:
            return True, 3
        return False, None
