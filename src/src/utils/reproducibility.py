"""Reproducibility utilities for G4 experimental protocol.

Ensures deterministic execution, random seeding, environment hashing,
and unique run ID generation.
"""

import hashlib
import json
import os
import random
import sys
import time
import uuid
from typing import Any, Dict


def set_seed(seed: int) -> None:
    """Set global random seeds for deterministic execution."""
    random.seed(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass


def generate_run_id(prefix: str = "run") -> str:
    """Generate a unique run ID with timestamp and UUID suffix."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    short_uuid = uuid.uuid4().hex[:8]
    return f"{prefix}_{timestamp}_{short_uuid}"


def compute_object_hash(obj: Any) -> str:
    """Compute a deterministic SHA-256 hash of a serializable object."""
    try:
        serialized = json.dumps(obj, sort_keys=True, default=str)
    except Exception:
        serialized = str(obj)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]


def get_runtime_environment_metadata() -> Dict[str, Any]:
    """Capture environment metadata for execution logs."""
    return {
        "python_version": sys.version,
        "platform": sys.platform,
        "cwd": os.getcwd(),
        "timestamp": time.time(),
        "iso_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
