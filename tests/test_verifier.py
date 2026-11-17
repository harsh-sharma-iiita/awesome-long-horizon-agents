"""Unit tests for deterministic contract assertions and non-oracular verifier behavior."""

import pytest
from src.tasks.task_generator import TaskGenerator
from src.tasks.task_graph import ContractRule, TaskGraph, TaskNode
from src.verification.verifier import DeterministicVerifier


def test_verifier_passes_clean_completed_state():
    """Verify verifier passes when all registered contracts are met."""
    gen = TaskGenerator(seed=10)
    graph = gen.generate_task("test_v1", horizon=12, topology_motif="fork_join")
    verifier = DeterministicVerifier(graph)

    # Mock valid outputs for all nodes
    outputs = {}
    for nid, node in graph.nodes.items():
        if node.op_type == "aggregate":
            outputs[nid] = {"summary": {"alpha": {"count": 2, "total_value": 20.0}}}
        elif node.op_type == "serialize":
            outputs[nid] = {"status": "COMPLETED", "artifact_data": {"records": []}}
        else:
            outputs[nid] = {"records": [{"record_id": 1, "value": 25.0}], "batch_id": "b1"}

    res = verifier.verify_checkpoint("n_00", step_idx=1, slot_index=1, completed_outputs=outputs)
    assert res.passed is True
    assert len(res.failed_rule_ids) == 0


def test_verifier_detects_schema_violation():
    """Verify verifier fails when required key is missing."""
    gen = TaskGenerator(seed=11)
    graph = gen.generate_task("test_v2", horizon=12, topology_motif="fork_join")
    verifier = DeterministicVerifier(graph)

    # Missing "batch_id" on n_00
    outputs = {"n_00": {"records": []}}
    res = verifier.verify_checkpoint("n_00", step_idx=1, slot_index=1, completed_outputs=outputs)

    assert res.passed is False
    assert any("c_00_schema" in r for r in res.failed_rule_ids)


def test_verifier_detects_type_corruption():
    """Verify verifier fails on mismatched key type."""
    gen = TaskGenerator(seed=12)
    graph = gen.generate_task("test_v3", horizon=12, topology_motif="fork_join")
    verifier = DeterministicVerifier(graph)

    # "records" is int instead of list
    outputs = {"n_00": {"records": 9999, "batch_id": "b1"}}
    res = verifier.verify_checkpoint("n_00", step_idx=1, slot_index=1, completed_outputs=outputs)

    assert res.passed is False
    assert any("c_00_type" in r for r in res.failed_rule_ids)


def test_verifier_detects_numeric_range_violation():
    """Verify verifier fails when numerical values violate min/max bounds."""
    graph = TaskGraph("range_g", 1, "custom")
    graph.add_node(TaskNode(
        node_id="n1", op_type="normalize", parents=[],
        contracts=[ContractRule("c_range", "range", "check bounds", min_value=0.0, max_value=100.0)]
    ))
    graph.compute_topological_order()
    verifier = DeterministicVerifier(graph)

    bad_outputs = {"n1": {"records": [{"value": -50.0}]}}
    res = verifier.verify_checkpoint("n1", step_idx=1, slot_index=1, completed_outputs=bad_outputs)

    assert res.passed is False
    assert "c_range" in res.failed_rule_ids


def test_verifier_rejects_non_dict_output():
    """Negative test: verify verifier rejects non-dict output."""
    graph = TaskGraph("bad_out_g", 1, "custom")
    graph.add_node(TaskNode(
        node_id="n1", op_type="source", parents=[],
        contracts=[ContractRule("c_schema", "schema", "schema check", expected_keys=["records"])]
    ))
    graph.compute_topological_order()
    verifier = DeterministicVerifier(graph)

    res = verifier.verify_checkpoint("n1", step_idx=1, slot_index=1, completed_outputs={"n1": "string_not_dict"})
    assert res.passed is False
