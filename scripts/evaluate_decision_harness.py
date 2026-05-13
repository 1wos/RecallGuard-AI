from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from recallguard import classify  # noqa: E402


DEFAULT_VENDOR = ROOT / "sample-data" / "evaluation" / "vendor_products_labeled.csv"
DEFAULT_EVIDENCE = ROOT / "sample-data" / "recall_certification_snapshot.csv"
DEFAULT_OUTPUT = ROOT / "outputs" / "evaluation" / "decision_harness_report.json"


def calculate_label_metrics(pairs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    labels = sorted({row["expected"] for row in pairs} | {row["predicted"] for row in pairs})
    metrics: dict[str, dict[str, Any]] = {}
    for label in labels:
        true_positive = sum(
            row["expected"] == label and row["predicted"] == label for row in pairs
        )
        predicted_count = sum(row["predicted"] == label for row in pairs)
        expected_count = sum(row["expected"] == label for row in pairs)
        metrics[label] = {
            "expected_count": expected_count,
            "predicted_count": predicted_count,
            "correct_count": true_positive,
            "precision": round(true_positive / predicted_count, 4) if predicted_count else None,
            "recall": round(true_positive / expected_count, 4) if expected_count else None,
        }
    return metrics


def evaluate(
    vendor_csv: str | Path = DEFAULT_VENDOR,
    evidence_csv: str | Path = DEFAULT_EVIDENCE,
) -> dict[str, Any]:
    labeled = pd.read_csv(vendor_csv).fillna("")
    expected = [str(value).strip().upper() for value in labeled["expected_decision"]]
    case_types = [str(value).strip() for value in labeled.get("case_type", [])]
    result = classify(vendor_csv, evidence_csv)

    pairs = []
    mismatches = []
    for index, product in enumerate(result["products"]):
        predicted = product["decision"]
        row = {
            "row_id": product["row_id"],
            "vendor_id": product["vendor_id"],
            "case_type": case_types[index] if index < len(case_types) else "",
            "expected": expected[index],
            "predicted": predicted,
            "decision_rule": product["decision_rule"],
            "correct": expected[index] == predicted,
        }
        pairs.append(row)
        if not row["correct"]:
            mismatches.append(
                {
                    **row,
                    "product_name": product["product_name"],
                    "model_name": product["model_name"],
                    "manufacturer": product["manufacturer"],
                    "reviewer_packet": product["reviewer_packet"],
                }
            )

    by_case_type: dict[str, Counter[str]] = defaultdict(Counter)
    for row in pairs:
        by_case_type[row["case_type"]]["total"] += 1
        by_case_type[row["case_type"]]["correct"] += int(row["correct"])

    return {
        "run_status": "success" if not mismatches else "needs_review",
        "total_rows": len(pairs),
        "correct_rows": sum(row["correct"] for row in pairs),
        "accuracy": round(sum(row["correct"] for row in pairs) / len(pairs), 4)
        if pairs
        else None,
        "label_metrics": calculate_label_metrics(pairs),
        "case_type_metrics": {
            case_type: {
                "total": counts["total"],
                "correct": counts["correct"],
                "accuracy": round(counts["correct"] / counts["total"], 4)
                if counts["total"]
                else None,
            }
            for case_type, counts in sorted(by_case_type.items())
        },
        "mismatches": mismatches,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vendor", default=str(DEFAULT_VENDOR))
    parser.add_argument("--evidence", default=str(DEFAULT_EVIDENCE))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    report = evaluate(args.vendor, args.evidence)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
