"""Unit tests for all four verification schedulers and budget parity constraints."""

import pytest
from src.schedulers.every_step import EveryStepScheduler
from src.schedulers.final_only import FinalOnlyScheduler
from src.schedulers.fixed_periodic import FixedPeriodicScheduler
from src.schedulers.milestone_based import MilestoneBasedScheduler
from src.tasks.task_generator import TaskGenerator


def test_fixed_periodic_scheduler_slot_allocation_h12():
    """Verify H=12 schedules exactly at ceil(H/3)=4, ceil(2H/3)=8, H=12."""
    sched = FixedPeriodicScheduler(horizon=12)
    assert sched.get_scheduled_steps() == (4, 8, 12)
    assert sched.allocated_slots == 3

    for step in range(1, 13):
        should_check, slot = sched.should_check(step, f"n_{step}")
        if step in (4, 8, 12):
            assert should_check is True
            expected_slot = 1 if step == 4 else (2 if step == 8 else 3)
            assert slot == expected_slot
        else:
            assert should_check is False
            assert slot is None


def test_final_only_scheduler_allocation():
    """Verify Final-Only (Arm A) allocates exactly 1 slot at terminal step H."""
    sched = FinalOnlyScheduler(horizon=12)
    assert sched.allocated_slots == 1
    assert sched.get_scheduled_steps() == (12,)

    for step in range(1, 12):
        should_check, slot = sched.should_check(step, f"n_{step}")
        assert should_check is False
        assert slot is None

    should_check, slot = sched.should_check(12, "n_12")
    assert should_check is True
    assert slot == 1


def test_every_step_scheduler_allocation():
    """Verify Every-Step (Arm D) allocates exactly H slots."""
    sched = EveryStepScheduler(horizon=12)
    assert sched.allocated_slots == 12
    assert len(sched.get_scheduled_steps()) == 12

    for step in range(1, 13):
        should_check, slot = sched.should_check(step, f"n_{step}")
        assert should_check is True
        assert slot == step


def test_milestone_based_scheduler_budget_parity_with_periodic():
    """Verify Milestone (Arm C) allocates exactly 3 slots, matching Periodic (Arm B)."""
    gen = TaskGenerator(seed=42)
    graph = gen.generate_task("test_sched_parity", horizon=12, topology_motif="fork_join")

    periodic = FixedPeriodicScheduler(horizon=12)
    milestone = MilestoneBasedScheduler(graph)

    # Budget parity check
    assert periodic.allocated_slots == 3
    assert milestone.allocated_slots == 3
    assert periodic.allocated_slots == milestone.allocated_slots

    m_steps = milestone.get_scheduled_steps()
    assert len(m_steps) == 3
    m1, m2, m3 = m_steps
    assert 1 <= m1 < m2 < m3 == 12

    # Check invocation counts over forward pass
    periodic_checks = 0
    milestone_checks = 0
    for step in range(1, 13):
        p_check, _ = periodic.should_check(step, f"n_{step}")
        m_check, _ = milestone.should_check(step, f"n_{step}")
        if p_check:
            periodic_checks += 1
        if m_check:
            milestone_checks += 1

    assert periodic_checks == 3
    assert milestone_checks == 3
