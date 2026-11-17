"""Deterministic contract verifier for G4 workflows.

Evaluates registered public contracts against completed workflow state.
Strictly non-oracular: operates only on public contracts and available node outputs,
with zero access to ground-truth fault labels, injection locations, or hidden expected answers.
"""

import time
from typing import Any, Dict, List, Optional
from src.tasks.task_graph import ContractRule, TaskGraph, TaskNode
from src.verification.verification_result import AssertionResult, VerificationResult


class DeterministicVerifier:
    """Evaluates registered contract assertions across completed workflow outputs."""

    def __init__(self, task_graph: TaskGraph):
        self.task_graph = task_graph
        self.invocation_count = 0
        self.total_verification_time = 0.0

    def verify_checkpoint(
        self,
        current_node_id: str,
        step_idx: int,
        slot_index: int,
        completed_outputs: Dict[str, Any]
    ) -> VerificationResult:
        """Run all registered assertions for nodes completed up to current_node_id."""
        start_time = time.perf_counter()
        self.invocation_count += 1

        assertion_results: List[AssertionResult] = []
        failed_rule_ids: List[str] = []
        failure_details: List[str] = []

        # Find all nodes completed up to and including current_node_id in topological order
        topo = self.task_graph.topological_order
        if current_node_id in topo:
            cutoff = topo.index(current_node_id) + 1
            nodes_to_check = topo[:cutoff]
        else:
            nodes_to_check = list(completed_outputs.keys())

        for nid in nodes_to_check:
            node = self.task_graph.nodes.get(nid)
            if not node:
                continue

            node_output = completed_outputs.get(nid)
            if node_output is None:
                # If a completed node has no output, fail schema
                res = AssertionResult(
                    rule_id=f"missing_output_{nid}",
                    rule_type="schema",
                    passed=False,
                    message=f"Node {nid} has no recorded output artifact.",
                    checked_node_id=nid
                )
                assertion_results.append(res)
                failed_rule_ids.append(res.rule_id)
                failure_details.append(res.message)
                continue

            # Evaluate each registered contract rule
            for rule in node.contracts:
                passed, msg = self._evaluate_rule(rule, node_output, completed_outputs, node)
                res = AssertionResult(
                    rule_id=rule.rule_id,
                    rule_type=rule.rule_type,
                    passed=passed,
                    message=msg,
                    checked_node_id=nid
                )
                assertion_results.append(res)
                if not passed:
                    failed_rule_ids.append(rule.rule_id)
                    failure_details.append(msg)

        elapsed = time.perf_counter() - start_time
        self.total_verification_time += elapsed

        overall_passed = len(failed_rule_ids) == 0
        return VerificationResult(
            passed=overall_passed,
            checked_node_id=current_node_id,
            execution_step_idx=step_idx,
            slot_index=slot_index,
            assertion_results=assertion_results,
            failed_rule_ids=failed_rule_ids,
            failure_details=failure_details,
            duration_seconds=elapsed,
            timestamp=time.time()
        )

    def _evaluate_rule(
        self,
        rule: ContractRule,
        node_output: Any,
        all_outputs: Dict[str, Any],
        node: TaskNode
    ) -> (bool, str):
        """Evaluate a single ContractRule against the output artifact."""
        if not isinstance(node_output, dict):
            return False, f"Rule {rule.rule_id}: output is not a dictionary ({type(node_output).__name__})."

        # 1. Schema: expected keys
        if rule.rule_type == "schema" and rule.expected_keys:
            missing = [k for k in rule.expected_keys if k not in node_output]
            if missing:
                return False, f"Rule {rule.rule_id}: missing required keys {missing}."

        # 2. Type integrity
        if rule.rule_type == "type" and rule.key_types:
            type_map = {"int": int, "float": (int, float), "str": str, "list": list, "dict": dict}
            for key, expected_tname in rule.key_types.items():
                if key in node_output:
                    val = node_output[key]
                    exp_type = type_map.get(expected_tname)
                    if exp_type and not isinstance(val, exp_type):
                        return False, f"Rule {rule.rule_id}: key '{key}' has type {type(val).__name__}, expected {expected_tname}."

        # 3. Numeric range / invariant
        if rule.rule_type == "range":
            # Check numeric range on records if present
            records = node_output.get("records")
            if isinstance(records, list):
                for rec in records:
                    if isinstance(rec, dict) and "value" in rec:
                        val = rec["value"]
                        if rule.min_value is not None and val < rule.min_value:
                            return False, f"Rule {rule.rule_id}: record value {val} < min_value {rule.min_value}."
                        if rule.max_value is not None and val > rule.max_value:
                            return False, f"Rule {rule.rule_id}: record value {val} > max_value {rule.max_value}."

        # 4. Reference integrity at joins
        if rule.rule_type == "reference_integrity" and rule.foreign_key_source:
            # Check that join key in every record exists in at least one parent dataset
            records = node_output.get("records", [])
            if not isinstance(records, list):
                return False, f"Rule {rule.rule_id}: output records is not a list ({type(records).__name__})."

            parent_keys_all = set()
            for p_id in node.parents:
                parent_out = all_outputs.get(p_id, {})
                if isinstance(parent_out, dict):
                    parent_records = parent_out.get("records", [])
                    if isinstance(parent_records, list):
                        parent_keys_all.update(
                            r.get(rule.foreign_key_source)
                            for r in parent_records
                            if isinstance(r, dict)
                        )
            for r in records:
                if isinstance(r, dict):
                    k_val = r.get(rule.foreign_key_source)
                    if k_val is not None and k_val not in parent_keys_all:
                        return False, f"Rule {rule.rule_id}: broken reference key {k_val} not found in parent outputs."

        # 5. Custom validator callable if provided
        if rule.validator:
            try:
                if not rule.validator(node_output):
                    return False, f"Rule {rule.rule_id}: custom validator returned False."
            except Exception as e:
                return False, f"Rule {rule.rule_id}: custom validator raised exception: {str(e)}."

        return True, "Passed"
