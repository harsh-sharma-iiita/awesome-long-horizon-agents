"""Task DAG representation and dependency graph structures for G4 workflows."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set
import networkx as nx


@dataclass
class ContractRule:
    """Declared public contract rule for a task node output."""
    rule_id: str
    rule_type: str  # 'schema', 'type', 'range', 'reference_integrity'
    description: str
    validator: Optional[Callable[[Any], bool]] = None
    expected_keys: Optional[List[str]] = None
    key_types: Optional[Dict[str, str]] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    foreign_key_source: Optional[str] = None  # parent node output to cross-check


@dataclass
class TaskNode:
    """Represents a single deterministic computation step in the workflow DAG."""
    node_id: str
    op_type: str  # 'source', 'parse', 'filter', 'normalize', 'aggregate', 'join', 'serialize'
    parents: List[str] = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=dict)
    contracts: List[ContractRule] = field(default_factory=list)
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Public serialization of node metadata (excluding runtime state)."""
        return {
            "node_id": self.node_id,
            "op_type": self.op_type,
            "parents": self.parents,
            "params": self.params,
            "description": self.description,
            "contract_ids": [c.rule_id for c in self.contracts],
        }


@dataclass
class TaskGraph:
    """Represents a full multi-step structured-data transformation DAG."""
    graph_id: str
    horizon: int
    topology_motif: str  # 'fork_join', 'spine_join', 'hierarchical_reduction'
    nodes: Dict[str, TaskNode] = field(default_factory=dict)
    topological_order: List[str] = field(default_factory=list)
    integration_boundaries: List[str] = field(default_factory=list)  # join nodes with in-degree > 1
    input_data: Dict[str, Any] = field(default_factory=dict)
    terminal_node_id: str = ""

    def __post_init__(self):
        if self.nodes and not self.topological_order:
            self.compute_topological_order()

    def add_node(self, node: TaskNode) -> None:
        """Add a node to the DAG."""
        self.nodes[node.node_id] = node

    def build_networkx_graph(self) -> nx.DiGraph:
        """Construct a NetworkX DiGraph representation."""
        g = nx.DiGraph()
        for node_id, node in self.nodes.items():
            g.add_node(node_id, op_type=node.op_type)
            for parent_id in node.parents:
                g.add_edge(parent_id, node_id)
        return g

    def compute_topological_order(self) -> List[str]:
        """Compute a deterministic topological sorting with stable alphanumeric tie-breaking."""
        g = self.build_networkx_graph()
        if not nx.is_directed_acyclic_graph(g):
            raise ValueError(f"TaskGraph {self.graph_id} contains cycles; not a valid DAG.")
        
        # Deterministic lexicographical topological sort
        self.topological_order = list(nx.lexicographical_topological_sort(g))
        return self.topological_order

    def find_descendants(self, node_id: str) -> Set[str]:
        """Return all topological descendants of a given node."""
        g = self.build_networkx_graph()
        if node_id not in g:
            return set()
        return nx.descendants(g, node_id)

    def find_ancestors(self, node_id: str) -> Set[str]:
        """Return all topological ancestors of a given node."""
        g = self.build_networkx_graph()
        if node_id not in g:
            return set()
        return nx.ancestors(g, node_id)

    def identify_integration_boundaries(self) -> List[str]:
        """Identify multi-parent join nodes (in-degree > 1) ordered by execution index."""
        g = self.build_networkx_graph()
        joins = [n for n in self.topological_order if g.in_degree(n) > 1]
        self.integration_boundaries = joins
        return joins
