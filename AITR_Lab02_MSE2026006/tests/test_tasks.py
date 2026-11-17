"""Unit tests for task graph creation, generation, and structural validation."""

import pytest
from src.tasks.task_generator import TaskGenerator
from src.tasks.task_graph import ContractRule, TaskGraph, TaskNode
from src.tasks.task_validator import TaskValidator


def test_task_generator_fork_join_structure():
    """Verify fork_join motif generates valid DAG with >= 2 multi-parent joins."""
    gen = TaskGenerator(seed=42)
    graph = gen.generate_task("test_fj_12", horizon=12, topology_motif="fork_join")

    assert len(graph.nodes) == 12
    assert len(graph.topological_order) == 12
    assert graph.terminal_node_id in graph.nodes

    # Check integration boundaries
    joins = graph.identify_integration_boundaries()
    assert len(joins) >= 2, f"Expected >= 2 join integration boundaries, found {len(joins)}"

    # Validate with TaskValidator
    is_valid, errors = TaskValidator.validate_graph(graph)
    assert is_valid, f"Graph validation failed: {errors}"


def test_task_generator_spine_join_structure():
    """Verify spine_join motif generates valid DAG with >= 2 multi-parent joins."""
    gen = TaskGenerator(seed=123)
    graph = gen.generate_task("test_sj_12", horizon=12, topology_motif="spine_join")

    assert len(graph.nodes) == 12
    is_valid, errors = TaskValidator.validate_graph(graph)
    assert is_valid, f"Graph validation failed: {errors}"


def test_task_generator_invalid_horizon():
    """Verify horizons below 6 raise ValueError."""
    gen = TaskGenerator(seed=1)
    with pytest.raises(ValueError, match="Horizon H=5 must be at least 6"):
        gen.generate_task("test_bad_h", horizon=5, topology_motif="fork_join")


def test_task_validator_catches_cycles():
    """Negative test: verify validator rejects cyclical graphs."""
    graph = TaskGraph(graph_id="cycle_graph", horizon=3, topology_motif="custom")
    graph.add_node(TaskNode(node_id="n1", op_type="source", parents=["n3"], contracts=[ContractRule("c1", "schema", "desc")]))
    graph.add_node(TaskNode(node_id="n2", op_type="filter", parents=["n1"], contracts=[ContractRule("c2", "schema", "desc")]))
    graph.add_node(TaskNode(node_id="n3", op_type="serialize", parents=["n2"], contracts=[ContractRule("c3", "schema", "desc")]))
    graph.terminal_node_id = "n3"

    is_valid, errors = TaskValidator.validate_graph(graph)
    assert not is_valid
    assert any("cycles" in e.lower() for e in errors)


def test_task_validator_catches_unreachable_terminal():
    """Negative test: verify validator rejects disconnected components."""
    graph = TaskGraph(graph_id="unreachable_graph", horizon=3, topology_motif="custom")
    graph.add_node(TaskNode(node_id="n1", op_type="source", parents=[], contracts=[ContractRule("c1", "schema", "desc")]))
    graph.add_node(TaskNode(node_id="n2", op_type="source", parents=[], contracts=[ContractRule("c2", "schema", "desc")]))
    graph.add_node(TaskNode(node_id="n3", op_type="serialize", parents=["n1"], contracts=[ContractRule("c3", "schema", "desc")]))
    graph.terminal_node_id = "n3"

    is_valid, errors = TaskValidator.validate_graph(graph)
    assert not is_valid
    assert any("cannot reach terminal" in e for e in errors)
