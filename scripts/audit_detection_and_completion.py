"""Investigation of Identical Detection (33.33%) and Completion (38.46%) rates across all four arms."""

import csv
from collections import Counter, defaultdict


def investigate_detection_and_completion():
    csv_path = "results/raw/final_exp_20261104_015549_5fcb5a61_all_episodes.csv"
    with open(csv_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print("=== 1. FAULT DETECTION COVERAGE BREAKDOWN ===")
    arms = ["final_only", "fixed_periodic", "milestone_based", "every_step"]
    
    # Fault rows only (N=1,080 per arm)
    for arm in arms:
        arm_faults = [r for r in rows if r["condition"] == arm and r["is_clean_control"] == "False"]
        detected = [r for r in arm_faults if r["fault_detected_by_verifier"] == "True"]
        print(f"Arm {arm:<15}: Detected {len(detected)} / {len(arm_faults)} ({len(detected)/len(arm_faults):.2%})")

    # Breakdown by fault type
    f_types = ["missing_field", "type_corruption", "numeric_corruption", "broken_reference"]
    print("\n--- Detection by Fault Type across Arms ---")
    for ft in f_types:
        print(f"\nFault Type: {ft} (N=270 episodes per arm)")
        for arm in arms:
            sub = [r for r in rows if r["condition"] == arm and r["fault_type"] == ft]
            det = [r for r in sub if r["fault_detected_by_verifier"] == "True"]
            print(f"  {arm:<15}: Detected {len(det)} / {len(sub)} ({len(det)/len(sub):.2%})")

    # Breakdown by position bin
    print("\n--- Detection by Position Bin across Arms ---")
    for pos in ["early", "middle", "late"]:
        print(f"\nPosition Bin: {pos} (N=360 episodes per arm)")
        for arm in arms:
            sub = [r for r in rows if r["condition"] == arm and r["is_clean_control"] == "False"]
            # Filter by target node position
            pos_sub = []
            for r in sub:
                nid = int(r["target_node_id"].split("_")[1])
                h = int(r["horizon"])
                if (pos == "early" and nid <= h//3) or \
                   (pos == "middle" and h//3 < nid <= 2*h//3) or \
                   (pos == "late" and nid > 2*h//3):
                    pos_sub.append(r)
            det = [r for r in pos_sub if r["fault_detected_by_verifier"] == "True"]
            print(f"  {arm:<15}: Detected {len(det)} / {len(pos_sub)} ({len(det)/len(pos_sub):.2%})")

    # Breakdown by Horizon
    print("\n--- Detection by Horizon across Arms ---")
    for h in [12, 24, 36]:
        print(f"\nHorizon: H={h} (N=360 episodes per arm)")
        for arm in arms:
            sub = [r for r in rows if r["condition"] == arm and r["is_clean_control"] == "False" and int(r["horizon"]) == h]
            det = [r for r in sub if r["fault_detected_by_verifier"] == "True"]
            print(f"  {arm:<15}: Detected {len(det)} / {len(sub)} ({len(det)/len(sub):.2%})")

    print("\n=== 2. TASK COMPLETION RATE BREAKDOWN ===")
    print("--- Clean vs Faulted Completion across Arms ---")
    for arm in arms:
        clean = [r for r in rows if r["condition"] == arm and r["is_clean_control"] == "True"]
        fault = [r for r in rows if r["condition"] == arm and r["is_clean_control"] == "False"]
        clean_pass = [r for r in clean if r["final_acceptance_passed"] == "True"]
        fault_pass = [r for r in fault if r["final_acceptance_passed"] == "True"]
        overall_pass = [r for r in rows if r["condition"] == arm and r["final_acceptance_passed"] == "True"]
        print(f"{arm:<15}: Overall = {len(overall_pass)}/1170 ({len(overall_pass)/1170:.2%}) | Clean = {len(clean_pass)}/90 ({len(clean_pass)/90:.2%}) | Fault = {len(fault_pass)}/1080 ({len(fault_pass)/1080:.2%})")

    print("\n--- Completion by Fault Type across Arms ---")
    for ft in f_types:
        print(f"\nFault Type: {ft} (N=270 episodes per arm)")
        for arm in arms:
            sub = [r for r in rows if r["condition"] == arm and r["fault_type"] == ft]
            p = [r for r in sub if r["final_acceptance_passed"] == "True"]
            print(f"  {arm:<15}: Passed {len(p)} / {len(sub)} ({len(p)/len(sub):.2%})")

    print("\n=== 3. ROOT CAUSE OF IDENTICAL RATES ===")
    print("Question A: Why is fault detection coverage identical (33.33%) across all four arms?")
    print("Fact 1: All 4 arms include a terminal check at step H (or every-step includes step H).")
    print("Fact 2: If a fault violates a registered verifier contract, it violates it either at an intermediate check OR at the terminal check at step H.")
    print("Fact 3: Missing field: 270/270 detected in all arms (Arm D detects immediately; Arm B detects at slot 1, 2, or 3; Arm C detects at slot 1, 2, or 3; Arm A detects at slot 3 (step H)). Because Arm A checks at step H, it STILL catches the missing field eventually!")
    print("Fact 4: Type corruption: 90/270 detected in all arms (the 90 that violate contracts are detected at or before step H).")
    print("Fact 5: Numeric corruption & broken reference: 0/270 detected in all arms because they do not trigger the schema/type contract.")
    print("Total detected: 270 + 90 + 0 + 0 = 360 episodes out of 1,080 = exactly 33.33% across all 4 arms!")
    print("\nQuestion B: Why is task completion identical (38.46%) across all four arms?")
    print("Fact 1: Clean runs (N=90) have 0 faults and 0 false alarms -> 90 pass final acceptance (100%).")
    print("Fact 2: In fault runs (N=1,080), exactly the 360 detected episodes trigger rollback-and-single-replay.")
    print("Fact 3: During replay, the fault injector is disarmed -> all 360 detected episodes recover successfully and pass final acceptance!")
    print("Fact 4: The 720 undetected fault episodes (180 type corruption + 270 numeric + 270 broken reference) are never detected by intermediate checks OR terminal checks, so no rollback occurs, and they reach terminal acceptance corrupted -> fail final acceptance!")
    print("Total passing episodes: 90 clean + 360 recovered = 450 out of 1,170 = exactly 38.46% across all 4 arms!")


if __name__ == "__main__":
    investigate_detection_and_completion()
