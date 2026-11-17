"""Dependency-Milestone verification scheduler (Arm C — Candidate Condition).

Allocates exactly three check slots on the forward pass:
- Milestone 1: Completion of all parent inputs to Integration Boundary 1 (Join 1)
- Milestone 2: Completion of all parent inputs to Integration Boundary 2 (Join 2)
- Milestone 3: Terminal acceptance node execution (H)

Strictly matched budget to Arm B (K_alloc = 3).
Derived purely from public DAG dependency graph topology with zero oracular fault knowledge.
"""

from typing import List, Optional, Tuple
from src.tasks.task_graph import TaskGraph


class MilestoneBasedScheduler:
    """Schedules deterministic verification at graph-derived dependency integration boundaries."""

    def __init__(self, task_graph: TaskGraph):
        self.task_graph = task_graph
        self.horizon = task_graph.horizon
        self.allocated_slots = 3

        # Derive milestones from public DAG topology
        topo = task_graph.topological_order
        joins = task_graph.integration_boundaries
        if len(joins) < 2:
            joins = [n for n in topo if len(task_graph.nodes[n].parents) > 1]

        if len(joins) < 2:
            raise ValueError(f"TaskGraph {task_graph.graph_id} must have >= 2 joins for milestone scheduling.")

        j1 = joins[0]
        j2 = joins[1]

        # Milestone 1: step where all parents of Join 1 are complete
        j1_parents = task_graph.nodes[j1].parents
        m1_step = max(topo.index(p) for p in j1_parents) + 1

        # Milestone 2: step where all parents of Join 2 are complete
        j2_parents = task_graph.nodes[j2].parents
        m2_step = max(topo.index(p) for p in j2_parents) + 1

        # Ensure strict ordering: m1 < m2 < horizon
        if m2_step <= m1_step:
            m2_step = m1_step + 1
        if m2_step >= self.horizon:
            m2_step = self.horizon - 1

        self.m1_step = m1_step
        self.m2_step = m2_step
        self.terminal_step = self.horizon

    def get_scheduled_steps(self) -> Tuple[int, int, int]:
        """Return the exact 1-indexed execution step indices where milestone checks occur."""
        return (self.m1_step, self.m2_step, self.terminal_step)

    def should_check(self, step_idx: int, node_id: str) -> Tuple[bool, Optional[int]]:
        """Determine whether verification should run at step_idx (1-indexed).

        Returns:
            Tuple[bool, Optional[int]]: (should_verify, slot_index: 1, 2, or 3)
        """
        if step_idx == self.m1_step:
            return True, 1
        elif step_idx == self.m2_step:
            return True, 2
        elif step_idx == self.terminal_step:
            return True, 3
        return False, None
