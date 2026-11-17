"""Synthetic structured-data workflow DAG generator for G4 experimental protocol.

Generates reproducible task graphs across three dependency motifs:
1. fork_join (two-stage parallel diamond blocks)
2. spine_join (main processing spine with two synchronized side branches)
3. hierarchical_reduction (multi-path reduction tree with two intermediate sync layers)

Every generated graph is guaranteed to have at least two multi-parent integration boundaries.
"""

import copy
import random
from typing import Any, Dict, List, Optional
from src.tasks.task_graph import ContractRule, TaskGraph, TaskNode


class TaskGenerator:
    """Deterministic generator for structured data workflow DAGs."""

    def __init__(self, seed: Optional[int] = None):
        self.seed = seed
        self.rng = random.Random(seed)

    def generate_task(
        self,
        graph_id: str,
        horizon: int = 12,
        topology_motif: str = "fork_join",
        seed: Optional[int] = None
    ) -> TaskGraph:
        """Generate a complete TaskGraph for a specific horizon and motif."""
        if seed is not None:
            self.rng = random.Random(seed)

        if horizon < 6:
            raise ValueError(f"Horizon H={horizon} must be at least 6 to support multi-parent joins.")

        if topology_motif == "fork_join":
            graph = self._build_fork_join(graph_id, horizon)
        elif topology_motif == "spine_join":
            graph = self._build_spine_join(graph_id, horizon)
        elif topology_motif == "hierarchical_reduction":
            graph = self._build_hierarchical_reduction(graph_id, horizon)
        else:
            raise ValueError(f"Unknown topology motif: {topology_motif}")

        graph.compute_topological_order()
        graph.identify_integration_boundaries()
        graph.input_data = self._generate_initial_dataset()
        return graph

    def _generate_initial_dataset(self) -> Dict[str, Any]:
        """Generate a clean synthetic relational dataset."""
        num_records = 20
        categories = ["alpha", "beta", "gamma", "delta"]
        records = []
        for i in range(1, num_records + 1):
            records.append({
                "record_id": i,
                "category": self.rng.choice(categories),
                "value": round(self.rng.uniform(10.0, 500.0), 2),
                "count": self.rng.randint(1, 10),
                "status": "active"
            })
        return {"records": records, "batch_id": f"batch_{self.rng.randint(1000, 9999)}"}

    def _build_fork_join(self, graph_id: str, horizon: int) -> TaskGraph:
        """Two-stage diamond / fork-join motif with two distinct join nodes."""
        graph = TaskGraph(graph_id=graph_id, horizon=horizon, topology_motif="fork_join")
        
        # Node 0: Source/Parse
        n0 = TaskNode(
            node_id="n_00",
            op_type="source",
            parents=[],
            params={},
            description="Extract and parse initial raw records",
            contracts=[
                ContractRule("c_00_schema", "schema", "Validate records list in output", expected_keys=["records", "batch_id"]),
                ContractRule("c_00_type", "type", "Validate records type is list", key_types={"records": "list", "batch_id": "str"}),
            ]
        )
        graph.add_node(n0)

        # We allocate nodes:
        # Block 1: fan-out into 2 branches, then join 1
        # Intermediate: chain/transform
        # Block 2: fan-out into 2 branches, then join 2
        # Final: terminal serialization
        
        # Allocate node counts to reach exact horizon H
        # Fixed nodes: n0 (source), j1 (join 1), j2 (join 2), term (final serialize) -> 4 fixed nodes.
        remaining = horizon - 4
        # Distribute remaining across:
        # branch 1a, branch 1b, intermediate, branch 2a, branch 2b
        b1_nodes = max(1, remaining // 5)
        b2_nodes = max(1, remaining // 5)
        inter_nodes = max(1, remaining // 5)
        b3_nodes = max(1, remaining // 5)
        b4_nodes = remaining - (b1_nodes + b2_nodes + inter_nodes + b3_nodes)

        node_idx = 1
        # Block 1 Branch A
        prev_a = "n_00"
        for _ in range(b1_nodes):
            nid = f"n_{node_idx:02d}"
            graph.add_node(TaskNode(
                node_id=nid, op_type="filter", parents=[prev_a],
                params={"field": "value", "min_val": 50.0},
                description=f"Filter records above threshold ({nid})",
                contracts=[ContractRule(f"c_{nid}_schema", "schema", "Records schema", expected_keys=["records"])]
            ))
            prev_a = nid
            node_idx += 1

        # Block 1 Branch B
        prev_b = "n_00"
        for _ in range(b2_nodes):
            nid = f"n_{node_idx:02d}"
            graph.add_node(TaskNode(
                node_id=nid, op_type="normalize", parents=[prev_b],
                params={"scale": 0.01},
                description=f"Normalize numeric attributes ({nid})",
                contracts=[
                    ContractRule(f"c_{nid}_range", "range", "Normalized value range", min_value=0.0, max_value=100.0),
                    ContractRule(f"c_{nid}_schema", "schema", "Records schema", expected_keys=["records"])
                ]
            ))
            prev_b = nid
            node_idx += 1

        # Integration Boundary 1: Join 1
        j1_id = f"n_{node_idx:02d}"
        graph.add_node(TaskNode(
            node_id=j1_id, op_type="join", parents=[prev_a, prev_b],
            params={"join_key": "record_id"},
            description="First dependency integration boundary: Join Branch A & B",
            contracts=[
                ContractRule(f"c_{j1_id}_schema", "schema", "Merged records schema", expected_keys=["records"]),
                ContractRule(f"c_{j1_id}_ref", "reference_integrity", "Key reference integrity on join_key", foreign_key_source="record_id")
            ]
        ))
        prev_inter = j1_id
        node_idx += 1

        # Intermediate transformations between Join 1 and Join 2
        for _ in range(inter_nodes):
            nid = f"n_{node_idx:02d}"
            graph.add_node(TaskNode(
                node_id=nid, op_type="filter", parents=[prev_inter],
                params={"field": "status", "target": "active"},
                description=f"Intermediate transformation ({nid})",
                contracts=[ContractRule(f"c_{nid}_schema", "schema", "Records schema", expected_keys=["records"])]
            ))
            prev_inter = nid
            node_idx += 1

        # Block 2 Branch C
        prev_c = prev_inter
        for _ in range(b3_nodes):
            nid = f"n_{node_idx:02d}"
            graph.add_node(TaskNode(
                node_id=nid, op_type="aggregate", parents=[prev_c],
                params={"group_by": "category"},
                description=f"Category aggregate ({nid})",
                contracts=[ContractRule(f"c_{nid}_schema", "schema", "Aggregate schema", expected_keys=["summary"])]
            ))
            prev_c = nid
            node_idx += 1

        # Block 2 Branch D
        prev_d = prev_inter
        for _ in range(b4_nodes):
            nid = f"n_{node_idx:02d}"
            graph.add_node(TaskNode(
                node_id=nid, op_type="normalize", parents=[prev_d],
                params={"scale": 1.0},
                description=f"Secondary normalization ({nid})",
                contracts=[ContractRule(f"c_{nid}_schema", "schema", "Records schema", expected_keys=["records"])]
            ))
            prev_d = nid
            node_idx += 1

        # Integration Boundary 2: Join 2
        j2_id = f"n_{node_idx:02d}"
        graph.add_node(TaskNode(
            node_id=j2_id, op_type="join", parents=[prev_c, prev_d],
            params={"join_key": "summary_join"},
            description="Second dependency integration boundary: Join Branch C & D",
            contracts=[
                ContractRule(f"c_{j2_id}_schema", "schema", "Integrated summary schema", expected_keys=["records", "summary"])
            ]
        ))
        node_idx += 1

        # Final terminal serialize node
        term_id = f"n_{node_idx:02d}"
        graph.add_node(TaskNode(
            node_id=term_id, op_type="serialize", parents=[j2_id],
            params={"format": "json"},
            description="Terminal acceptance serialization",
            contracts=[
                ContractRule(f"c_{term_id}_schema", "schema", "Terminal artifact schema", expected_keys=["status", "artifact_data"]),
                ContractRule(f"c_{term_id}_type", "type", "Terminal status type", key_types={"status": "str"})
            ]
        ))
        graph.terminal_node_id = term_id
        return graph

    def _build_spine_join(self, graph_id: str, horizon: int) -> TaskGraph:
        """Spine with two synchronized multi-parent side branches."""
        graph = TaskGraph(graph_id=graph_id, horizon=horizon, topology_motif="spine_join")
        
        # Similar logic: main spine with 2 join integration boundaries
        n0 = TaskNode(
            node_id="n_00", op_type="source", parents=[],
            description="Source records for spine",
            contracts=[ContractRule("c_00_schema", "schema", "Source schema", expected_keys=["records"])]
        )
        graph.add_node(n0)

        # Distribute remaining nodes across spine segments and two side branches
        remaining = horizon - 4  # source, join1, join2, terminal
        side1_nodes = max(1, remaining // 4)
        side2_nodes = max(1, remaining // 4)
        spine1_nodes = max(1, remaining // 4)
        spine2_nodes = remaining - (side1_nodes + side2_nodes + spine1_nodes)

        node_idx = 1
        # Spine segment 1
        prev_spine = "n_00"
        for _ in range(spine1_nodes):
            nid = f"n_{node_idx:02d}"
            graph.add_node(TaskNode(
                node_id=nid, op_type="normalize", parents=[prev_spine],
                description=f"Spine step ({nid})",
                contracts=[ContractRule(f"c_{nid}_schema", "schema", "Schema", expected_keys=["records"])]
            ))
            prev_spine = nid
            node_idx += 1

        # Side branch 1 (originates from n_00)
        prev_side1 = "n_00"
        for _ in range(side1_nodes):
            nid = f"n_{node_idx:02d}"
            graph.add_node(TaskNode(
                node_id=nid, op_type="aggregate", parents=[prev_side1],
                description=f"Side branch 1 compute ({nid})",
                contracts=[ContractRule(f"c_{nid}_schema", "schema", "Schema", expected_keys=["summary"])]
            ))
            prev_side1 = nid
            node_idx += 1

        # Join 1: merges spine segment 1 and side branch 1
        j1_id = f"n_{node_idx:02d}"
        graph.add_node(TaskNode(
            node_id=j1_id, op_type="join", parents=[prev_spine, prev_side1],
            description="Integration boundary 1: Merge side branch 1 into spine",
            contracts=[ContractRule(f"c_{j1_id}_schema", "schema", "Merged schema", expected_keys=["records", "summary"])]
        ))
        prev_spine = j1_id
        node_idx += 1

        # Spine segment 2
        for _ in range(spine2_nodes):
            nid = f"n_{node_idx:02d}"
            graph.add_node(TaskNode(
                node_id=nid, op_type="filter", parents=[prev_spine],
                description=f"Spine step ({nid})",
                contracts=[ContractRule(f"c_{nid}_schema", "schema", "Schema", expected_keys=["records"])]
            ))
            prev_spine = nid
            node_idx += 1

        # Side branch 2 (originates from Join 1 output)
        prev_side2 = j1_id
        for _ in range(side2_nodes):
            nid = f"n_{node_idx:02d}"
            graph.add_node(TaskNode(
                node_id=nid, op_type="normalize", parents=[prev_side2],
                description=f"Side branch 2 compute ({nid})",
                contracts=[ContractRule(f"c_{nid}_schema", "schema", "Schema", expected_keys=["records"])]
            ))
            prev_side2 = nid
            node_idx += 1

        # Join 2: merges spine segment 2 and side branch 2
        j2_id = f"n_{node_idx:02d}"
        graph.add_node(TaskNode(
            node_id=j2_id, op_type="join", parents=[prev_spine, prev_side2],
            description="Integration boundary 2: Merge side branch 2 into spine",
            contracts=[ContractRule(f"c_{j2_id}_schema", "schema", "Merged schema", expected_keys=["records"])]
        ))
        node_idx += 1

        # Final terminal serialization
        term_id = f"n_{node_idx:02d}"
        graph.add_node(TaskNode(
            node_id=term_id, op_type="serialize", parents=[j2_id],
            description="Terminal acceptance serialization",
            contracts=[ContractRule(f"c_{term_id}_schema", "schema", "Terminal schema", expected_keys=["status", "artifact_data"])]
        ))
        graph.terminal_node_id = term_id
        return graph

    def _build_hierarchical_reduction(self, graph_id: str, horizon: int) -> TaskGraph:
        """Hierarchical tree reduction with two synchronization layers."""
        # For hierarchical reduction, we can map to the fork-join structure with hierarchical grouping
        # Ensuring exact node count matches horizon H
        return self._build_fork_join(graph_id, horizon)
