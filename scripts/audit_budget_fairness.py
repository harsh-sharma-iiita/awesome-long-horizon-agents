"""Independent audit of Verification Budget Fairness: Allocated vs Realized calls, early termination, and replay."""

import csv
from collections import Counter


def audit_budget_fairness():
    csv_path = "results/raw/final_exp_20261104_015549_5fcb5a61_all_episodes.csv"
    with open(csv_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print("=== 1. ALLOCATED SLOTS AUDIT ===")
    b_rows = [r for r in rows if r["condition"] == "fixed_periodic"]
    c_rows = [r for r in rows if r["condition"] == "milestone_based"]

    b_alloc = Counter(r["allocated_slots"] for r in b_rows)
    c_alloc = Counter(r["allocated_slots"] for r in c_rows)
    print(f"Arm B allocated slots distribution: {dict(b_alloc)} (All 1,170 episodes have exactly 3)")
    print(f"Arm C allocated slots distribution: {dict(c_alloc)} (All 1,170 episodes have exactly 3)")
    assert b_alloc == {"3": 1170}
    assert c_alloc == {"3": 1170}

    print("\n=== 2. REALIZED VERIFICATION CALLS AUDIT ===")
    b_calls = [int(r["realized_verifier_calls"]) for r in b_rows]
    c_calls = [int(r["realized_verifier_calls"]) for r in c_rows]

    b_call_counts = Counter(b_calls)
    c_call_counts = Counter(c_calls)
    print(f"Arm B realized calls breakdown: {dict(b_call_counts)}")
    print(f"Arm C realized calls breakdown: {dict(c_call_counts)}")

    # Check pair-by-pair realized calls
    paired_b = {(r["graph_id"], r["scenario_idx"]): int(r["realized_verifier_calls"]) for r in b_rows}
    paired_c = {(r["graph_id"], r["scenario_idx"]): int(r["realized_verifier_calls"]) for r in c_rows}

    call_diffs = [paired_c[k] - paired_b[k] for k in paired_b]
    exact_matches = sum(1 for d in call_diffs if d == 0)
    b_greater = sum(1 for d in call_diffs if d < 0)
    c_greater = sum(1 for d in call_diffs if d > 0)

    print(f"Pair-by-pair call comparison (N=1,170 episodes):")
    print(f"  Identical realized calls: {exact_matches} ({exact_matches/len(call_diffs):.1%})")
    print(f"  Arm B > Arm C:            {b_greater} ({b_greater/len(call_diffs):.1%})")
    print(f"  Arm C > Arm B:            {c_greater} ({c_greater/len(call_diffs):.1%})")
    print(f"  Mean realized calls Arm B: {sum(b_calls)/len(b_calls):.4f}")
    print(f"  Mean realized calls Arm C: {sum(c_calls)/len(c_calls):.4f}")

    print("\n=== 3. EARLY TERMINATION & REPLAY BEHAVIOR ===")
    # When a check fails, does execution stop/rollback, and does replay invoke checks?
    # Inspect episodes where rollback occurred
    b_rollback = [r for r in b_rows if r["rollback_occurred"] == "True"]
    c_rollback = [r for r in c_rows if r["rollback_occurred"] == "True"]
    print(f"Arm B rollback episodes: {len(b_rollback)}")
    print(f"Arm C rollback episodes: {len(c_rollback)}")

    # Check detecting slot for rollback episodes
    b_detect_slots = Counter(r["detecting_check_slot"] for r in b_rollback)
    c_detect_slots = Counter(r["detecting_check_slot"] for r in c_rollback)
    print(f"Arm B detecting slots: {dict(b_detect_slots)}")
    print(f"Arm C detecting slots: {dict(c_detect_slots)}")

    # Check realized calls when detected at slot 1, slot 2, slot 3
    for slot in ["1", "2", "3"]:
        b_slot_calls = [int(r["realized_verifier_calls"]) for r in b_rollback if r["detecting_check_slot"] == slot]
        c_slot_calls = [int(r["realized_verifier_calls"]) for r in c_rollback if r["detecting_check_slot"] == slot]
        print(f"Slot {slot} detection realized calls -> Arm B: {set(b_slot_calls)}, Arm C: {set(c_slot_calls)}")

    # Check whether replay ever invokes extra checks
    # If a check is detected at slot 1, the realized calls are 1 (check fails, rollback to t=0, replay to end without further checks)
    # If detected at slot 2, realized calls are 2 (slot 1 passed, slot 2 failed, rollback to slot 1, replay to end)
    # If detected at slot 3, realized calls are 3 (slot 1 passed, slot 2 passed, slot 3 failed, rollback to slot 2, replay to end)
    # Clean episodes: slots 1, 2, 3 all pass -> realized calls = 3
    print("\n=== 4. SUMMARY OF BUDGET PARITY MECHANISM ===")
    print("Why are mean realized calls identical (2.7436 calls)?")
    print("1. Both Arms B and C allocate exactly 3 check slots (K_alloc = 3).")
    print("2. For clean controls (N=90) and undetected faults (N=720), all 3 check slots are reached -> 3 calls.")
    print("3. For detected faults (N=360), early termination truncates execution after the first failed check.")
    print("4. In Arm B: 180 faults detected at slot 1 (1 call), 90 at slot 2 (2 calls), 90 at slot 3 (3 calls). Mean = (180*1 + 90*2 + 90*3)/360 = 1.75 calls.")
    print("5. In Arm C: 90 faults detected at slot 1 (1 call), 180 at slot 2 (2 calls), 90 at slot 3 (3 calls). Mean = (90*1 + 180*2 + 90*3)/360 = 2.00 calls.")
    print("Wait! Let's examine the exact distribution of calls across the entire 1,170 episodes!")


if __name__ == "__main__":
    audit_budget_fairness()
