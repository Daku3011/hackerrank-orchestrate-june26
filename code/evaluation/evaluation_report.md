# Evaluation Report

Date: 2026-06-19T15:46:25.833205
Model: gemini-3.1-flash-lite-preview
Samples evaluated: 20
Images processed: 29

## Summary

**Exact categorical match** (all 8 categorical fields): 11/20 (55.0%)
**Joint accuracy** (claim_status + issue_type + object_part): 15/20 (75.0%)

## Per-Field Accuracy

| Field | Accuracy | Correct / Total |
|---|---|---|
| evidence_standard_met | 95.0% | 19/20 |
| risk_flags | 70.0% | 14/20 |
| issue_type | 80.0% | 16/20 |
| object_part | 90.0% | 18/20 |
| claim_status | 85.0% | 17/20 |
| supporting_image_ids | 85.0% | 17/20 |
| valid_image | 95.0% | 19/20 |
| severity | 80.0% | 16/20 |

## Operational Analysis

### Model Calls
- Sample processing: 20 claims, 20 model calls (each includes all images for that claim)

### Token & Image Usage
- Images processed: 29
- Model: Google Gemini 3.1 Flash Lite Preview (free tier)

### Cost Estimate
- Free tier Gemini API — no cost for evaluation
- For production: Gemini 3.1 Flash ~$0.075/1M input tokens, ~$0.30/1M output tokens
- Each image at 768x768 resolution ≈ 258 tokens

### Runtime
- Total runtime for 20 claims: sequential, ~2.5s per claim average
- With parallel batching: could reduce to ~0.5s per claim

### Strategy Notes
- Single-pass VLM prompt with all images and claim context
- JSON output parsing with retry logic
- Evidence requirements and user history included as context