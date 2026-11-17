"""Validator for task DAG structure, acyclicity, reachability, and contract completeness."""

from typing import List, Tuple
import networkx as nx
from src.tasks.task_graph import TaskGraph


class TaskValidator:
    """Performs static structural and contract validation on TaskGraph instances."""

    @staticmethod
    def validate_graph(graph: TaskGraph) -> Tuple[bool, List[str]]:
        """Validate all structural and semantic integrity rules for a task graph."""
        errors: List[str] = []

        # 1. Node count check
        if len(graph.nodes) != graph.horizon:
            errors.append(f"Node count mismatch: graph has {len(graph.nodes)} nodes, expected horizon {graph.horizon}.")

        # 2. Graph acyclicity
        nx_graph = graph.build_networkx_graph()
        if not nx.is_directed_acyclic_graph(nx_graph):
            errors.append("Graph contains cycles; must be a strict DAG.")

        # 3. Parent reference validity
        for node_id, node in graph.nodes.items():
            for p in node.parents:
                if p not in graph.nodes:
                    errors.append(f"Node {node_id} references nonexistent parent {p}.")

        # 4. Terminal node reachability
        if not graph.terminal_node_id or graph.terminal_node_id not in graph.nodes:
            errors.append(f"Invalid terminal node ID: {graph.terminal_node_id}.")
        else:
            # Check that every node has a directed path to the terminal node or is terminal
            for node_id in graph.nodes:
                if node_id != graph.terminal_node_id:
                    if not nx.has_path(nx_graph, node_id, graph.terminal_node_id):
                        errors.append(f"Node {node_id} cannot reach terminal node {graph.terminal_node_id}.")

        # 5. Integration boundaries (multi-parent joins)
        joins = [n for n in graph.nodes.values() if len(n.parents) > 1]
        if len(joins) < 2:
            errors.append(f"Graph contains {len(joins)} multi-parent joins; minimum 2 required for G4 protocol.")

        # 6. Contract registration
        for node_id, node in graph.nodes.items():
            if not node.contracts:
                errors.append(f"Node {node_id} has no registered contract rules.")

        is_valid = len(errors) == 0
        return is_valid, errors
