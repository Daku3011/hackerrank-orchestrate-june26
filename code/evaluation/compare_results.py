#!/usr/bin/env python3
import csv
import sys
from pathlib import Path

def normalize(val):
    v = str(val).strip().lower()
    parts = sorted([p.strip() for p in v.replace(";", ";").split(";") if p.strip()])
    return ";".join(parts)

def main():
    root = Path(__file__).resolve().parent.parent.parent
    expected_path = root / "dataset" / "sample_claims.csv"
    pred_path = root / "code" / "evaluation" / "predictions_sample.csv"

    if not pred_path.exists():
        print("Predictions file not found!")
        return

    with open(expected_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        expected_rows = list(reader)

    with open(pred_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        pred_rows = list(reader)

    CATEGORICAL_FIELDS = [
        "evidence_standard_met", "risk_flags", "issue_type", "object_part",
        "claim_status", "supporting_image_ids", "valid_image", "severity",
    ]

    for idx, (expected, pred) in enumerate(zip(expected_rows, pred_rows)):
        mismatches = []
        for field in CATEGORICAL_FIELDS:
            ev = normalize(expected.get(field, ""))
            pv = normalize(pred.get(field, ""))
            if ev != pv:
                mismatches.append(f"{field}: expected={ev!r}, got={pv!r}")
        
        if mismatches:
            print(f"Row {idx+2} ({expected['user_id']}):")
            print(f"  Claim: {expected['user_claim'][:100]}...")
            for m in mismatches:
                print(f"    - {m}")
            print("-" * 60)

if __name__ == "__main__":
    main()
