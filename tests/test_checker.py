from __future__ import annotations

from pathlib import Path

from recallguard import classify


ROOT = Path(__file__).resolve().parents[1]
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
