"""Audit script: Directory reconciliation, file hash comparisons, and artifact integrity."""

import hashlib
from pathlib import Path


def get_hash(p: Path):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def reconcile_directories():
    root = Path(".")
    sub = Path("AITR_Lab02_MSE2026006")

    print("=== RECONCILING ROOT vs AITR_Lab02_MSE2026006 ===")

    key_dirs = [
        "research",
        "results/raw",
        "results/processed",
        "results/tables",
        "results/comparisons",
        "runs/configurations",
        "runs/logs",
        "runs/trajectories",
        "figures/experiments",
        "figures/analysis",
        "paper",
        "paper/sections",
        "src/tasks",
        "src/execution",
        "src/verification",
        "src/schedulers",
        "src/evaluation",
        "src/utils",
        "tests",
        "scripts",
        "ai_logs"
    ]

    total_checked = 0
    identical_count = 0
    mismatches = []
    missing_in_root = []
    missing_in_sub = []

    for d in key_dirs:
        root_d = root / d
        sub_d = sub / d

        # Check all files in root_d
        if root_d.exists():
            for p in root_d.glob("*"):
                if p.is_file() and not p.name.endswith(".pyc") and p.name != ".gitkeep":
                    total_checked += 1
                    sub_p = sub_d / p.name
                    if not sub_p.exists():
                        missing_in_sub.append(str(sub_p))
                    else:
                        h_root = get_hash(p)
                        h_sub = get_hash(sub_p)
                        if h_root == h_sub:
                            identical_count += 1
                        else:
                            mismatches.append((str(p), str(sub_p), h_root[:8], h_sub[:8]))

        # Check files in sub_d missing in root
        if sub_d.exists():
            for p in sub_d.glob("*"):
                if p.is_file() and not p.name.endswith(".pyc") and p.name != ".gitkeep":
                    root_p = root_d / p.name
                    if not root_p.exists():
                        missing_in_root.append(str(root_p))

    print(f"Total key files checked: {total_checked}")
    print(f"Identical files (SHA-256 match): {identical_count}")
    print(f"Mismatches: {len(mismatches)}")
    for r_f, s_f, hr, hs in mismatches:
        print(f"  MISMATCH: {r_f} (hash {hr}) != {s_f} (hash {hs})")

    print(f"Missing in subfolder: {len(missing_in_sub)}")
    for m in missing_in_sub:
        print(f"  MISSING IN SUB: {m}")

    print(f"Missing in root: {len(missing_in_root)}")
    for m in missing_in_root:
        print(f"  MISSING IN ROOT: {m}")


if __name__ == "__main__":
    reconcile_directories()
