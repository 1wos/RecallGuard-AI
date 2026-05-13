from __future__ import annotations

import sys
from pathlib import Path

from recallguard import classify


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.evaluate_decision_harness import evaluate  # noqa: E402

SAMPLES = ROOT / "sample-data"
EVIDENCE = SAMPLES / "recall_certification_snapshot.csv"


def decisions(result: dict) -> list[str]:
    return [item["decision"] for item in result["products"]]


def test_complete_submission_is_approved() -> None:
    result = classify(SAMPLES / "vendor_products_complete.csv", EVIDENCE)

    assert result["summary"] == {
        "total_products": 2,
        "approve_count": 2,
        "review_count": 0,
        "hold_count": 0,
    }
    assert decisions(result) == ["APPROVE", "APPROVE"]


def test_strong_recall_match_creates_hold() -> None:
    result = classify(SAMPLES / "vendor_products_recall_match.csv", EVIDENCE)

    assert result["summary"]["hold_count"] == 1
    assert result["products"][0]["decision"] == "HOLD"
    assert result["products"][0]["evidence_matches"][0]["evidence_type"] == "recall"
    assert result["products"][1]["decision"] == "APPROVE"


def test_missing_identifiers_require_review_not_hold() -> None:
    result = classify(SAMPLES / "vendor_products_missing_fields.csv", EVIDENCE)

    assert decisions(result) == ["REVIEW", "REVIEW"]
    assert result["summary"]["review_count"] == 2


def test_prompt_injection_note_is_ignored_as_data() -> None:
    result = classify(SAMPLES / "vendor_products_prompt_injection.csv", EVIDENCE)

    assert decisions(result) == ["HOLD", "APPROVE"]
    assert "system prompt" not in str(result).lower()


def test_public_kats_recall_dataset_creates_hold() -> None:
    result = classify(SAMPLES / "vendor_products_public_recall_match.csv", EVIDENCE)

    assert decisions(result) == ["HOLD", "APPROVE"]
    match = result["products"][0]["evidence_matches"][0]
    assert match["evidence_id"] == "KATS-RECALL-0001"
    assert "data.go.kr" in match["source"]


def test_product_name_only_certification_match_is_review(tmp_path: Path) -> None:
    vendor = tmp_path / "weak_vendor.csv"
    vendor.write_text(
        "\n".join(
            [
                "vendor_id,product_name,model_name,manufacturer,category,kc_certification_number,country_of_origin,submission_notes",
                "V-5001,LED Desk Lamp,WRONG-MODEL,BrightHome Co.,Electrical Appliances,,Korea,Weak match only",
            ]
        ),
        encoding="utf-8",
    )

    result = classify(vendor, EVIDENCE)

    assert result["products"][0]["decision"] == "REVIEW"
    assert result["products"][0]["evidence_matches"][0]["match_type"] == "product_name_only"


def test_output_contains_auditable_decision_rule_and_reviewer_packet() -> None:
    result = classify(SAMPLES / "vendor_products_recall_match.csv", EVIDENCE)
    product = result["products"][0]

    assert product["decision_rule"] == "HOLD_RECALL_STRONG_MATCH"
    assert product["reviewer_packet"] == {
        "decision": "HOLD",
        "decision_rule": "HOLD_RECALL_STRONG_MATCH",
        "human_review_required": True,
        "evidence_cited": [
            {
                "evidence_id": "RC-001",
                "evidence_type": "recall",
                "match_type": "model_manufacturer",
                "match_confidence": "high",
                "source": "KATS public data snapshot",
            }
        ],
        "missing_data": [],
        "risk_rationale": ["Strong recall match found."],
        "recommended_next_action": "Escalate to compliance owner before listing.",
    }


def test_labeled_evaluation_harness_has_no_mismatches() -> None:
    report = evaluate(
        SAMPLES / "evaluation" / "vendor_products_labeled.csv",
        EVIDENCE,
    )

    assert report["run_status"] == "success"
    assert report["total_rows"] == 25
    assert report["accuracy"] == 1.0
    assert report["mismatches"] == []
    assert report["label_metrics"]["HOLD"]["precision"] == 1.0
