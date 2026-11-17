"""Independent evaluator for G4 experimental protocol.

Operates with complete access to ground-truth fault labels, injection targets,
and DAG taint lineage. Evaluates terminal artifact acceptance and calculates
unbiased propagation metrics strictly isolated from the verifier.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
from src.execution.executor import WorkflowExecutionResult
from src.execution.fault_injection import FaultDescriptor
from src.tasks.task_graph import TaskGraph


@dataclass
class EpisodeEvaluationReport:
    """Ground-truth evaluation metrics for a single execution episode."""
    run_id: str
    graph_id: str
    condition: str
    is_clean_control: bool
    fault_type: Optional[str]
    target_node_id: Optional[str]
    is_contract_violating: bool
    num_topological_descendants: int
    is_eligible_for_tcf: bool
    nodes_tainted: Set[str] = field(default_factory=set)
    downstream_taint_consumed_count: int = 0
    taint_consumption_fraction: Optional[float] = None
    fault_detected_by_verifier: bool = False
    detecting_check_slot: Optional[int] = None
    detecting_node_id: Optional[str] = None
    detection_delay_nodes: Optional[int] = None
    rollback_occurred: bool = False
    rollback_distance: int = 0
    replay_nodes_executed: int = 0
    realized_verifier_calls: int = 0
    final_acceptance_passed: bool = False
    false_positive_check: bool = False
    total_workflow_time: float = 0.0
    total_verifier_time: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert evaluation report to dictionary for logging and analysis."""
        return {
            "run_id": self.run_id,
            "graph_id": self.graph_id,
            "condition": self.condition,
            "is_clean_control": self.is_clean_control,
            "fault_type": self.fault_type,
            "target_node_id": self.target_node_id,
            "is_contract_violating": self.is_contract_violating,
            "num_topological_descendants": self.num_topological_descendants,
            "is_eligible_for_tcf": self.is_eligible_for_tcf,
            "downstream_taint_consumed_count": self.downstream_taint_consumed_count,
            "taint_consumption_fraction": self.taint_consumption_fraction,
            "fault_detected_by_verifier": self.fault_detected_by_verifier,
            "detecting_check_slot": self.detecting_check_slot,
            "detecting_node_id": self.detecting_node_id,
            "detection_delay_nodes": self.detection_delay_nodes,
            "rollback_occurred": self.rollback_occurred,
            "rollback_distance": self.rollback_distance,
            "replay_nodes_executed": self.replay_nodes_executed,
            "realized_verifier_calls": self.realized_verifier_calls,
            "final_acceptance_passed": self.final_acceptance_passed,
            "false_positive_check": self.false_positive_check,
            "total_workflow_time": self.total_workflow_time,
            "total_verifier_time": self.total_verifier_time,
        }


class IndependentEvaluator:
    """Evaluates execution trajectories against ground-truth DAG lineage and acceptance rules."""

    def __init__(self, task_graph: TaskGraph):
        self.task_graph = task_graph
        self.nx_graph = task_graph.build_networkx_graph()

    def evaluate_episode(
        self,
        exec_result: WorkflowExecutionResult,
        fault_desc: Optional[FaultDescriptor] = None
    ) -> EpisodeEvaluationReport:
        """Conduct post-hoc ground truth evaluation of a completed execution episode."""
        is_clean = (fault_desc is None)
        target_nid = fault_desc.target_node_id if fault_desc else None
        ftype = fault_desc.fault_type if fault_desc else None
        is_contract_viol = fault_desc.is_contract_violating if fault_desc else False

        # 1. Topological descendants of fault target
        descendants: Set[str] = set()
        if target_nid and target_nid in self.task_graph.nodes:
            descendants = self.task_graph.find_descendants(target_nid)
        num_desc = len(descendants)
        is_eligible_tcf = (num_desc >= 1) and (not is_clean)

        # 2. Taint lineage propagation tracking during forward pass
        # The target node output was mutated. Any node executed in the forward attempt
        # that consumed mutated output directly or indirectly is tainted.
        tainted_nodes: Set[str] = set()
        if target_nid:
            tainted_nodes.add(target_nid)

        # Forward nodes actually executed before halt or completion
        forward_nodes = [nid for nid in exec_result.executed_sequence if not nid.endswith("_replay")]
        
        # Propagate taint along forward execution sequence
        consumed_taint_nodes: Set[str] = set()
        for nid in forward_nodes:
            if nid == target_nid:
                continue
            node = self.task_graph.nodes.get(nid)
            if not node:
                continue
            # If any parent is in tainted_nodes, this node consumed taint
            if any(p in tainted_nodes for p in node.parents):
                tainted_nodes.add(nid)
                if nid in descendants:
                    consumed_taint_nodes.add(nid)

        c_e = len(consumed_taint_nodes)
        tcf = (c_e / num_desc) if is_eligible_tcf and num_desc > 0 else None

        # 3. Verifier detection tracking
        detected = False
        det_slot = None
        det_node = None
        det_delay = None

        for v_res in exec_result.verification_results:
            if not v_res.passed:
                detected = True
                det_slot = v_res.slot_index
                det_node = v_res.checked_node_id
                # Delay = index of check node - index of target node in topological order
                if target_nid in self.task_graph.topological_order and det_node in self.task_graph.topological_order:
                    t_idx = self.task_graph.topological_order.index(det_node)
                    j_idx = self.task_graph.topological_order.index(target_nid)
                    det_delay = max(0, t_idx - j_idx)
                break

        # 4. False positive detection check on clean runs
        false_positive = is_clean and any(not v.passed for v in exec_result.verification_results)

        # 5. Independent final acceptance check
        # Ground truth acceptance: terminal artifact exists, contains required status, and data is valid
        final_passed = False
        term = exec_result.terminal_artifact
        if term and isinstance(term, dict):
            if term.get("status") == "COMPLETED" and "artifact_data" in term:
                final_passed = True
                # If unrecovered fault reached terminal artifact without rollback, fail acceptance
                if (not is_clean) and (not exec_result.rollback_occurred) and (self.task_graph.terminal_node_id in tainted_nodes):
                    final_passed = False

        return EpisodeEvaluationReport(
            run_id=exec_result.run_id,
            graph_id=exec_result.graph_id,
            condition=exec_result.condition,
            is_clean_control=is_clean,
            fault_type=ftype,
            target_node_id=target_nid,
            is_contract_violating=is_contract_viol,
            num_topological_descendants=num_desc,
            is_eligible_for_tcf=is_eligible_tcf,
            nodes_tainted=tainted_nodes,
            downstream_taint_consumed_count=c_e,
            taint_consumption_fraction=tcf,
            fault_detected_by_verifier=detected,
            detecting_check_slot=det_slot,
            detecting_node_id=det_node,
            detection_delay_nodes=det_delay,
            rollback_occurred=exec_result.rollback_occurred,
            rollback_distance=exec_result.rollback_distance,
            replay_nodes_executed=exec_result.replay_nodes_executed,
            realized_verifier_calls=exec_result.realized_verifier_calls,
            final_acceptance_passed=final_passed,
            false_positive_check=false_positive,
            total_workflow_time=exec_result.total_workflow_time,
            total_verifier_time=exec_result.total_verifier_time
        )
