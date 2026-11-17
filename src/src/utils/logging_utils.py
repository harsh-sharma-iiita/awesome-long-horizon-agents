"""Logging utilities for G4 experimental protocol.

Provides append-only structured JSONL event logging, console logging,
and run trace management, strictly preserving separation between
verifier-visible state and ground-truth evaluator records.
"""

import json
import logging
import os
import sys
from typing import Any, Dict, Optional


def setup_console_logger(name: str = "g4_experiment", level: int = logging.INFO) -> logging.Logger:
    """Configure a clean console logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger


class JsonlEventLogger:
    """Append-only JSONL logger for experiment events and trajectories."""

    def __init__(self, log_path: str):
        self.log_path = os.path.abspath(log_path)
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Write a single event dictionary as a JSON line."""
        record = {
            "event_type": event_type,
            **data
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=str) + "\n")


class RunTrajectoryLogger:
    """Manages separate event logs for public workflow execution and evaluator ground truth."""

    def __init__(self, run_dir: str, run_id: str):
        self.run_dir = os.path.abspath(run_dir)
        self.run_id = run_id
        os.makedirs(self.run_dir, exist_ok=True)
        
        self.public_log = JsonlEventLogger(os.path.join(self.run_dir, f"{run_id}_public_trace.jsonl"))
        self.evaluator_log = JsonlEventLogger(os.path.join(self.run_dir, f"{run_id}_evaluator_truth.jsonl"))

    def log_public_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Log event observable to verifiers/schedulers (no ground-truth fault labels)."""
        payload["run_id"] = self.run_id
        self.public_log.log_event(event_type, payload)

    def log_evaluator_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Log confidential ground truth (fault labels, injection nodes, taint lineage)."""
        payload["run_id"] = self.run_id
        self.evaluator_log.log_event(event_type, payload)
