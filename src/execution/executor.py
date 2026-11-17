"""Deterministic workflow executor with snapshotting, rollback, and single-pass replay."""

import copy
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from src.execution.fault_injection import FaultInjector
from src.schedulers.fixed_periodic import FixedPeriodicScheduler
from src.tasks.task_graph import TaskGraph, TaskNode
from src.verification.verification_result import VerificationResult
from src.verification.verifier import DeterministicVerifier


@dataclass
class WorkflowExecutionResult:
    """Complete trajectory and metrics from executing a workflow episode."""
    run_id: str
    graph_id: str
    condition: str  # 'periodic_baseline' (Arm B)
    status: str  # 'ACCEPTED', 'REJECTED_VERIFICATION', 'ERROR'
    forward_steps_executed: int = 0
    replay_nodes_executed: int = 0
    rollback_occurred: bool = False
    rollback_distance: int = 0
    restored_checkpoint_step: int = 0
    allocated_verifier_slots: int = 3
    realized_verifier_calls: int = 0
    verification_results: List[VerificationResult] = field(default_factory=list)
    terminal_artifact: Optional[Dict[str, Any]] = None
    completed_outputs: Dict[str, Any] = field(default_factory=dict)
    executed_sequence: List[str] = field(default_factory=list)
    total_workflow_time: float = 0.0
    total_verifier_time: float = 0.0
    error_message: Optional[str] = None


class WorkflowExecutor:
    """Executes a TaskGraph deterministically, applying scheduled checks and recovery."""

    def __init__(self, task_graph: TaskGraph, scheduler: Any, condition: str = "fixed_periodic"):
        self.task_graph = task_graph
        self.scheduler = scheduler
        self.condition = condition
        self.verifier = DeterministicVerifier(task_graph)

    def execute(
        self,
        run_id: str,
        fault_injector: Optional[FaultInjector] = None,
        event_logger: Optional[Any] = None
    ) -> WorkflowExecutionResult:
        """Execute the workflow DAG from start to acceptance or terminal failure."""
        start_wall_time = time.perf_counter()
        topo_order = self.task_graph.topological_order
        horizon = len(topo_order)

        # Snapshot storage: step_idx -> state dictionary mapping node_id -> output
        snapshots: Dict[int, Dict[str, Any]] = {0: {}}
        latest_verified_step = 0  # 0 is the initial clean input state

        completed_outputs: Dict[str, Any] = {}
        verification_results: List[VerificationResult] = []
        executed_sequence: List[str] = []

        rollback_occurred = False
        rollback_distance = 0
        restored_checkpoint_step = 0
        replay_nodes_executed = 0

        current_step = 1
        halt_forward = False

        # --- FORWARD ATTEMPT ---
        for node_id in topo_order:
            node = self.task_graph.nodes[node_id]
            executed_sequence.append(node_id)

            # Execute node operation deterministically
            try:
                raw_out = self._execute_node_op(node, completed_outputs, self.task_graph.input_data)
            except Exception as e:
                return WorkflowExecutionResult(
                    run_id=run_id, graph_id=self.task_graph.graph_id, condition=self.condition,
                    status="ERROR", forward_steps_executed=current_step,
                    error_message=f"Node {node_id} execution error: {str(e)}"
                )

            # Injected fault hook
            if fault_injector:
                node_out = fault_injector.inject_if_target(node_id, current_step, raw_out)
            else:
                node_out = raw_out

            completed_outputs[node_id] = node_out
            snapshots[current_step] = copy.deepcopy(completed_outputs)

            if event_logger:
                event_logger.log_public_event("node_executed", {
                    "step_idx": current_step,
                    "node_id": node_id,
                    "op_type": node.op_type
                })

            # Check verification schedule
            should_check, slot_idx = self.scheduler.should_check(current_step, node_id)
            if should_check:
                ver_res = self.verifier.verify_checkpoint(
                    current_node_id=node_id,
                    step_idx=current_step,
                    slot_index=slot_idx,
                    completed_outputs=completed_outputs
                )
                verification_results.append(ver_res)

                if event_logger:
                    event_logger.log_public_event("verifier_invocation", ver_res.to_dict())

                if ver_res.passed:
                    latest_verified_step = current_step
                else:
                    # Check failed: halt forward pass and initiate restore-and-replay-once
                    halt_forward = True
                    rollback_occurred = True
                    rollback_distance = current_step - latest_verified_step
                    restored_checkpoint_step = latest_verified_step
                    break

            current_step += 1

        forward_steps = len(executed_sequence)

        # --- RECOVERY REPLAY (IF CHECK FAILED) ---
        if halt_forward:
            if event_logger:
                event_logger.log_public_event("rollback_initiated", {
                    "failed_step": forward_steps,
                    "restore_checkpoint_step": restored_checkpoint_step,
                    "rollback_distance": rollback_distance
                })

            # Restore verified snapshot
            completed_outputs = copy.deepcopy(snapshots[restored_checkpoint_step])

            # Disarm one-shot fault injector during replay
            if fault_injector:
                fault_injector.disarm()

            # Suffix replay: execute remaining nodes from restored_checkpoint_step + 1 to horizon
            replay_slice = topo_order[restored_checkpoint_step:]
            for r_node_id in replay_slice:
                r_node = self.task_graph.nodes[r_node_id]
                replay_nodes_executed += 1
                executed_sequence.append(f"{r_node_id}_replay")

                try:
                    r_raw_out = self._execute_node_op(r_node, completed_outputs, self.task_graph.input_data)
                except Exception as e:
                    return WorkflowExecutionResult(
                        run_id=run_id, graph_id=self.task_graph.graph_id, condition=self.condition,
                        status="ERROR", forward_steps_executed=forward_steps,
                        replay_nodes_executed=replay_nodes_executed,
                        rollback_occurred=True, rollback_distance=rollback_distance,
                        error_message=f"Replay error at node {r_node_id}: {str(e)}"
                    )

                # Fault injector is disarmed: outputs are clean
                completed_outputs[r_node_id] = r_raw_out

                if event_logger:
                    event_logger.log_public_event("replay_node_executed", {
                        "replay_idx": replay_nodes_executed,
                        "node_id": r_node_id
                    })

                # ZERO VERIFIER CHECKS DURING REPLAY per protocol!

        elapsed_total = time.perf_counter() - start_wall_time
        terminal_artifact = completed_outputs.get(self.task_graph.terminal_node_id)

        # Status determination: if terminal artifact produced, marked ACCEPTED (final evaluator will judge validity)
        status = "ACCEPTED" if terminal_artifact is not None else "FAILED_EXECUTION"

        return WorkflowExecutionResult(
            run_id=run_id,
            graph_id=self.task_graph.graph_id,
            condition=self.condition,
            status=status,
            forward_steps_executed=forward_steps,
            replay_nodes_executed=replay_nodes_executed,
            rollback_occurred=rollback_occurred,
            rollback_distance=rollback_distance,
            restored_checkpoint_step=restored_checkpoint_step,
            allocated_verifier_slots=self.scheduler.allocated_slots,
            realized_verifier_calls=len(verification_results),
            verification_results=verification_results,
            terminal_artifact=terminal_artifact,
            completed_outputs=completed_outputs,
            executed_sequence=executed_sequence,
            total_workflow_time=elapsed_total,
            total_verifier_time=self.verifier.total_verification_time
        )

    def _execute_node_op(
        self,
        node: TaskNode,
        completed_outputs: Dict[str, Any],
        initial_input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a deterministic operation with input validation."""
        op = node.op_type

        if op == "source":
            # Return copy of initial records
            records = copy.deepcopy(initial_input.get("records", []))
            return {
                "records": records,
                "batch_id": initial_input.get("batch_id", "batch_0"),
                "node_id": node.node_id
            }

        elif op == "filter":
            # Parent must have 'records'
            parent_out = completed_outputs.get(node.parents[0], {})
            parent_records = parent_out.get("records", []) if isinstance(parent_out, dict) else []
            if not isinstance(parent_records, list):
                parent_records = []
            field = node.params.get("field", "value")
            min_val = node.params.get("min_val")
            target = node.params.get("target")

            filtered = []
            for r in parent_records:
                if not isinstance(r, dict):
                    continue
                keep = True
                if min_val is not None and field in r:
                    if r[field] <= min_val:
                        keep = False
                if target is not None and field in r:
                    if r[field] != target:
                        keep = False
                if keep:
                    filtered.append(copy.deepcopy(r))
            return {"records": filtered, "node_id": node.node_id}

        elif op == "normalize":
            parent_out = completed_outputs.get(node.parents[0], {})
            parent_records = parent_out.get("records", []) if isinstance(parent_out, dict) else []
            if not isinstance(parent_records, list):
                parent_records = []
            scale = node.params.get("scale", 1.0)
            normalized = []
            for r in parent_records:
                if isinstance(r, dict):
                    r_copy = copy.deepcopy(r)
                    if "value" in r_copy and isinstance(r_copy["value"], (int, float)):
                        r_copy["value"] = round(r_copy["value"] * scale, 4)
                    normalized.append(r_copy)
            return {"records": normalized, "node_id": node.node_id}

        elif op == "aggregate":
            parent_out = completed_outputs.get(node.parents[0], {})
            if not isinstance(parent_out, dict):
                parent_out = {}
            group_by = node.params.get("group_by", "category")
            if "records" in parent_out and isinstance(parent_out["records"], list):
                summary = {}
                for r in parent_out["records"]:
                    if isinstance(r, dict):
                        grp = r.get(group_by, "unknown")
                        val = r.get("value", 0.0)
                        if isinstance(val, (int, float)):
                            if grp not in summary:
                                summary[grp] = {"count": 0, "total_value": 0.0}
                            summary[grp]["count"] += 1
                            summary[grp]["total_value"] = round(summary[grp]["total_value"] + val, 2)
            elif "summary" in parent_out and isinstance(parent_out["summary"], dict):
                summary = copy.deepcopy(parent_out["summary"])
            else:
                summary = {}
            return {"summary": summary, "node_id": node.node_id}

        elif op == "join":
            # Multi-parent merge
            merged_records = []
            combined_summary = {}
            had_summary_parent = False
            for p_id in node.parents:
                p_out = completed_outputs.get(p_id, {})
                if isinstance(p_out, dict):
                    if "records" in p_out and isinstance(p_out["records"], list):
                        merged_records.extend(copy.deepcopy(p_out["records"]))
                    if "summary" in p_out and isinstance(p_out["summary"], dict):
                        had_summary_parent = True
                        combined_summary.update(copy.deepcopy(p_out["summary"]))
            res = {"node_id": node.node_id}
            if merged_records:
                res["records"] = merged_records
            if had_summary_parent:
                res["summary"] = combined_summary
            return res

        elif op == "serialize":
            parent_out = completed_outputs.get(node.parents[0], {})
            return {
                "status": "COMPLETED",
                "artifact_data": copy.deepcopy(parent_out),
                "terminal_node_id": node.node_id
            }

        else:
            raise ValueError(f"Unsupported operation type: {op}")
