"""Unit tests for fault injection classes, mutations, and disarm behavior."""

import pytest
from src.execution.fault_injection import FaultDescriptor, FaultInjector


def test_fault_injection_missing_field():
    """Verify missing_field removes target key."""
    desc = FaultDescriptor(fault_type="missing_field", target_node_id="n_01", position_bin="early", parameter_field="records")
    injector = FaultInjector(desc)
    data = {"records": [{"id": 1, "value": 10.0}], "batch_id": "b1"}

    mutated = injector.inject_if_target("n_01", step_idx=1, raw_output=data)
    assert "records" not in mutated
    assert "batch_id" in mutated
    assert injector.has_injected is True


def test_fault_injection_type_corruption():
    """Verify type_corruption replaces declared type with integer."""
    desc = FaultDescriptor(fault_type="type_corruption", target_node_id="n_02", position_bin="early", parameter_field="records")
    injector = FaultInjector(desc)
    data = {"records": [{"id": 1}], "status": "ok"}

    mutated = injector.inject_if_target("n_02", step_idx=2, raw_output=data)
    assert isinstance(mutated["records"], int)


def test_fault_injection_numeric_corruption():
    """Verify numeric_corruption perturbs value to negative."""
    desc = FaultDescriptor(fault_type="numeric_corruption", target_node_id="n_03", position_bin="middle")
    injector = FaultInjector(desc)
    data = {"records": [{"record_id": 1, "value": 50.0}]}

    mutated = injector.inject_if_target("n_03", step_idx=3, raw_output=data)
    assert mutated["records"][0]["value"] == -9999.0


def test_fault_injection_broken_reference():
    """Verify broken_reference corrupts join ID."""
    desc = FaultDescriptor(fault_type="broken_reference", target_node_id="n_04", position_bin="late")
    injector = FaultInjector(desc)
    data = {"records": [{"record_id": 1, "value": 50.0}]}

    mutated = injector.inject_if_target("n_04", step_idx=4, raw_output=data)
    assert mutated["records"][0]["record_id"] == -88888


def test_fault_injection_one_shot_and_disarm():
    """Verify fault injection is one-shot and disabled when disarmed."""
    desc = FaultDescriptor(fault_type="missing_field", target_node_id="n_01", position_bin="early")
    injector = FaultInjector(desc)
    data = {"records": [1, 2, 3]}

    # First injection
    out1 = injector.inject_if_target("n_01", step_idx=1, raw_output=data)
    assert "records" not in out1

    # Second injection attempt at same node is ignored (one-shot)
    out2 = injector.inject_if_target("n_01", step_idx=1, raw_output=data)
    assert "records" in out2

    # Disarm test
    desc2 = FaultDescriptor(fault_type="missing_field", target_node_id="n_05", position_bin="early")
    injector2 = FaultInjector(desc2)
    injector2.disarm()
    out3 = injector2.inject_if_target("n_05", step_idx=5, raw_output=data)
    assert "records" in out3
