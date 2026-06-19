#!/usr/bin/env python3
import csv
import sys
import os
from pathlib import Path
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from code.data_loader import load_claims, DATASET_DIR
from code.claim_processor import ClaimProcessor

OUTPUT_COLUMNS = [
    "user_id", "image_paths", "user_claim", "claim_object",
    "evidence_standard_met", "evidence_standard_met_reason", "risk_flags",
    "issue_type", "object_part", "claim_status", "claim_status_justification",
    "supporting_image_ids", "valid_image", "severity",
]

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "output.csv"


def main():
    processor = ClaimProcessor()
    claims = load_claims()
    print(f"Processing {len(claims)} claims...")

    results = []
    for row in tqdm(claims, desc="Claims"):
        result = processor.process_claim(row)
        results.append(result)

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(results)

    print(f"Done. Wrote {len(results)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
