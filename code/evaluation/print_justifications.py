#!/usr/bin/env python3
import csv
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent.parent.parent
    pred_path = root / "code" / "evaluation" / "predictions_sample.csv"
    expected_path = root / "dataset" / "sample_claims.csv"

    with open(pred_path, "r", encoding="utf-8") as f:
        preds = {row["user_id"]: row for row in csv.DictReader(f)}

    with open(expected_path, "r", encoding="utf-8") as f:
        expected = {row["user_id"]: row for row in csv.DictReader(f)}

    mismatched_ids = ["user_001", "user_002", "user_004", "user_005", "user_006", "user_007", "user_008", "user_018", "user_020", "user_031", "user_032", "user_033", "user_034"]

    for uid in mismatched_ids:
        if uid in preds:
            p = preds[uid]
            e = expected[uid]
            print(f"=== {uid} ===")
            print(f"Claim: {e['user_claim'][:120]}...")
            print(f"Images: {e['image_paths']}")
            print(f"Expected: status={e['claim_status']}, issue={e['issue_type']}, part={e['object_part']}, met={e['evidence_standard_met']}, valid={e['valid_image']}, severity={e['severity']}, support={e['supporting_image_ids']}, risks={e['risk_flags']}")
            print(f"Got:      status={p['claim_status']}, issue={p['issue_type']}, part={p['object_part']}, met={p['evidence_standard_met']}, valid={p['valid_image']}, severity={p['severity']}, support={p['supporting_image_ids']}, risks={p['risk_flags']}")
            print(f"Got Reason: {p['evidence_standard_met_reason']}")
            print(f"Got Justification: {p['claim_status_justification']}")
            print("-" * 80)

if __name__ == "__main__":
    main()
