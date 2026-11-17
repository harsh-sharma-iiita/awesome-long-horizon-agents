"""Unit tests for JSONL event logging and trace isolation."""

import json
import os
import tempfile
import pytest
from src.utils.logging_utils import JsonlEventLogger, RunTrajectoryLogger


def test_jsonl_logger_writes_and_parses():
    """Verify JsonlEventLogger appends valid JSON records."""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = os.path.join(tmpdir, "test_events.jsonl")
        logger = JsonlEventLogger(log_file)

        logger.log_event("step_start", {"step": 1, "node": "n_01"})
        logger.log_event("step_end", {"step": 1, "status": "ok"})

        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) == 2
        rec1 = json.loads(lines[0])
        rec2 = json.loads(lines[1])

        assert rec1["event_type"] == "step_start"
        assert rec1["node"] == "n_01"
        assert rec2["event_type"] == "step_end"


def test_run_trajectory_logger_separates_public_and_evaluator_logs():
    """Verify RunTrajectoryLogger keeps evaluator ground truth in a separate file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        traj_logger = RunTrajectoryLogger(tmpdir, "run_test_123")

        traj_logger.log_public_event("verifier_invocation", {"slot": 1, "passed": True})
        traj_logger.log_evaluator_event("ground_truth_fault", {"fault": "missing_field", "target": "n_01"})

        assert os.path.exists(traj_logger.public_log.log_path)
        assert os.path.exists(traj_logger.evaluator_log.log_path)

        with open(traj_logger.public_log.log_path, "r", encoding="utf-8") as f:
            pub_content = f.read()
        with open(traj_logger.evaluator_log.log_path, "r", encoding="utf-8") as f:
            eval_content = f.read()

        assert "verifier_invocation" in pub_content
        assert "ground_truth_fault" not in pub_content

        assert "ground_truth_fault" in eval_content
