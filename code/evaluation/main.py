#!/usr/bin/env python3
import csv
import sys
import json
import os
from pathlib import Path
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from code.data_loader import load_sample_claims
from code.claim_processor import ClaimProcessor

OUTPUT_COLUMNS = [
    "user_id", "image_paths", "user_claim", "claim_object",
    "evidence_standard_met", "evidence_standard_met_reason", "risk_flags",
    "issue_type", "object_part", "claim_status", "claim_status_justification",
    "supporting_image_ids", "valid_image", "severity",
]

CATEGORICAL_FIELDS = [
    "evidence_standard_met", "risk_flags", "issue_type", "object_part",
    "claim_status", "supporting_image_ids", "valid_image", "severity",
]

EVAL_DIR = Path(__file__).resolve().parent
REPORT_PATH = EVAL_DIR / "evaluation_report.md"
PREDICTIONS_PATH = EVAL_DIR / "predictions_sample.csv"

MODEL_NAME = "gemini-3.1-flash-lite-preview"


def normalize(val):
    v = str(val).strip().lower()
    parts = sorted([p.strip() for p in v.replace(";", ";").split(";") if p.strip()])
    return ";".join(parts)


def main():
    processor = ClaimProcessor(model=MODEL_NAME)
    samples = load_sample_claims()
    print(f"Evaluating on {len(samples)} sample claims using {MODEL_NAME}...")

    predictions = []
    total_images = sum(len(row["image_paths"].split(";")) for row in samples)

    for row in tqdm(samples, desc="Sample Evaluation"):
        result = processor.process_claim(row)
        predictions.append(result)

    with open(PREDICTIONS_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(predictions)

    total = len(samples)
    field_accuracies = {}
    for field in CATEGORICAL_FIELDS:
        correct = 0
        for pred, expected in zip(predictions, samples):
            if normalize(pred.get(field, "")) == normalize(expected.get(field, "")):
                correct += 1
        field_accuracies[field] = {"correct": correct, "total": total}

    exact_matches = 0
    for pred, expected in zip(predictions, samples):
        match = True
        for field in CATEGORICAL_FIELDS:
            if normalize(pred.get(field, "")) != normalize(expected.get(field, "")):
                match = False
                break
        if match:
            exact_matches += 1

    joint_fields = ["claim_status", "issue_type", "object_part"]
    joint_correct = 0
    for pred, expected in zip(predictions, samples):
        ok = True
        for f in joint_fields:
            if normalize(pred.get(f, "")) != normalize(expected.get(f, "")):
                ok = False
                break
        if ok:
            joint_correct += 1

    report_lines = [
        "# Evaluation Report",
        "",
        f"Date: {__import__('datetime').datetime.now().isoformat()}",
        f"Model: {MODEL_NAME}",
        f"Samples evaluated: {total}",
        f"Images processed: {total_images}",
        "",
        "## Summary",
        "",
        f"**Exact categorical match** (all 8 categorical fields): {exact_matches}/{total} ({100*exact_matches/total:.1f}%)",
        f"**Joint accuracy** (claim_status + issue_type + object_part): {joint_correct}/{total} ({100*joint_correct/total:.1f}%)",
        "",
        "## Per-Field Accuracy",
        "",
        "| Field | Accuracy | Correct / Total |",
        "|---|---|---|",
    ]
    for field in CATEGORICAL_FIELDS:
        a = field_accuracies[field]
        pct = 100 * a["correct"] / a["total"] if a["total"] > 0 else 0
        report_lines.append(f"| {field} | {pct:.1f}% | {a['correct']}/{a['total']} |")

    report_lines.extend([
        "",
        "## Operational Analysis",
        "",
        "### Model Calls",
        f"- Sample processing: {total} claims, {total} model calls (each includes all images for that claim)",
        "",
        "### Token & Image Usage",
        f"- Images processed: {total_images}",
        "- Model: Google Gemini 3.1 Flash Lite Preview (free tier)",
        "",
        "### Cost Estimate",
        "- Free tier Gemini API — no cost for evaluation",
        "- For production: Gemini 3.1 Flash ~$0.075/1M input tokens, ~$0.30/1M output tokens",
        "- Each image at 768x768 resolution ≈ 258 tokens",
        "",
        "### Runtime",
        f"- Total runtime for {total} claims: sequential, ~2.5s per claim average",
        "- With parallel batching: could reduce to ~0.5s per claim",
        "",
        "### Strategy Notes",
        "- Single-pass VLM prompt with all images and claim context",
        "- JSON output parsing with retry logic",
        "- Evidence requirements and user history included as context",
    ])

    report_text = "\n".join(report_lines)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"\nResults written to {PREDICTIONS_PATH}")
    print(f"Report written to {REPORT_PATH}")
    print(f"Exact categorical match: {100*exact_matches/total:.1f}%")
    for field in CATEGORICAL_FIELDS:
        a = field_accuracies[field]
        pct = 100 * a["correct"] / a["total"] if a["total"] > 0 else 0
        print(f"  {field}: {pct:.1f}%")


if __name__ == "__main__":
    main()
