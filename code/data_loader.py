import csv
import os
from pathlib import Path

DATASET_DIR = Path(__file__).resolve().parent.parent / "dataset"


def load_csv(filename):
    path = DATASET_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_claims():
    return load_csv("claims.csv")


def load_sample_claims():
    return load_csv("sample_claims.csv")


def load_user_history():
    return load_csv("user_history.csv")


def load_evidence_requirements():
    return load_csv("evidence_requirements.csv")


def build_user_history_map():
    rows = load_user_history()
    return {r["user_id"]: r for r in rows}


def build_evidence_requirements_map(claim_object):
    rows = load_evidence_requirements()
    applicable = []
    for r in rows:
        obj = r["claim_object"]
        if obj == "all" or obj == claim_object:
            applicable.append(r)
    return applicable


def resolve_image_path(image_path):
    full_path = (DATASET_DIR / image_path).resolve()
    if full_path.exists():
        return str(full_path)
    alt_path = DATASET_DIR / "images" / image_path
    if alt_path.exists():
        return str(alt_path)
    return None


def get_image_id(image_path):
    return Path(image_path).stem
