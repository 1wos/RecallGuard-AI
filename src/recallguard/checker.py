from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_FIELDS = ["product_name", "model_name", "manufacturer"]


def find_file(filename: str | Path) -> Path:
    path = Path(filename)
    if path.exists():
        return path

    basename = path.name
    candidates = list(Path(".").rglob(basename))
    if not candidates and Path("/mnt/data").exists():
        candidates = list(Path("/mnt/data").rglob(basename))
    if not candidates:
        raise FileNotFoundError(f"Could not find {filename}")
    return candidates[0]


def norm(value: Any) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().casefold()


def classify(vendor_csv: str | Path, evidence_csv: str | Path = "recall_certification_snapshot.csv") -> dict[str, Any]:
    vendor = pd.read_csv(find_file(vendor_csv)).fillna("")
    evidence = pd.read_csv(find_file(evidence_csv)).fillna("")

    products = []
    for index, row in vendor.iterrows():
        product_name = norm(row.get("product_name", ""))
        model_name = norm(row.get("model_name", ""))
        manufacturer = norm(row.get("manufacturer", ""))
        cert_number = norm(row.get("kc_certification_number", ""))

        missing_fields = [field for field in REQUIRED_FIELDS if norm(row.get(field, "")) == ""]
        recall_matches = []
        certification_matches = []

        for _, ev in evidence.iterrows():
            ev_type = norm(ev.get("evidence_type", ""))
            ev_product = norm(ev.get("product_name", ""))
            ev_model = norm(ev.get("model_name", ""))
            ev_manufacturer = norm(ev.get("manufacturer", ""))
            ev_cert = norm(ev.get("kc_certification_number", ""))

            exact_cert = bool(cert_number and ev_cert and cert_number == ev_cert)
            exact_model_mfr = bool(
                model_name
                and manufacturer
                and ev_model
                and ev_manufacturer
                and model_name == ev_model
                and manufacturer == ev_manufacturer
            )
            product_only = bool(product_name and ev_product and product_name == ev_product)

            if not (exact_cert or exact_model_mfr or product_only):
                continue

            match = {
                "evidence_id": ev.get("evidence_id", ""),
                "evidence_type": ev.get("evidence_type", ""),
                "match_type": (
                    "certification_number"
                    if exact_cert
                    else "model_manufacturer"
                    if exact_model_mfr
                    else "product_name_only"
                ),
                "match_confidence": "high" if exact_cert or exact_model_mfr else "low",
            }

            if ev_type == "recall" and (exact_cert or exact_model_mfr):
                recall_matches.append(match)
            elif ev_type == "certification":
                certification_matches.append(match)

        if recall_matches:
            decision = "HOLD"
            reasons = ["Strong recall match found."]
            evidence_matches = recall_matches
        elif missing_fields:
            decision = "REVIEW"
            reasons = ["Missing required product identifiers."]
            evidence_matches = certification_matches
        elif any(match["match_confidence"] == "high" for match in certification_matches):
            decision = "APPROVE"
            reasons = ["Certification evidence found and no recall match detected."]
            evidence_matches = [
                match for match in certification_matches if match["match_confidence"] == "high"
            ]
        elif certification_matches:
            decision = "REVIEW"
            reasons = ["Only weak product-name certification evidence found."]
            evidence_matches = certification_matches
        else:
            decision = "REVIEW"
            reasons = ["No strong certification or recall evidence found."]
            evidence_matches = []

        products.append(
            {
                "row_id": str(index + 1),
                "vendor_id": row.get("vendor_id", ""),
                "product_name": row.get("product_name", ""),
                "model_name": row.get("model_name", ""),
                "manufacturer": row.get("manufacturer", ""),
                "decision": decision,
                "risk_reasons": reasons,
                "evidence_matches": evidence_matches,
                "missing_fields": missing_fields,
                "recommended_action": (
                    "Escalate to compliance owner before listing."
                    if decision == "HOLD"
                    else "Request missing vendor evidence."
                    if decision == "REVIEW"
                    else "Proceed with standard approval record."
                ),
            }
        )

    summary = {
        "total_products": len(products),
        "approve_count": sum(item["decision"] == "APPROVE" for item in products),
        "review_count": sum(item["decision"] == "REVIEW" for item in products),
        "hold_count": sum(item["decision"] == "HOLD" for item in products),
    }
    return {"run_status": "success", "summary": summary, "products": products}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("vendor_csv")
    parser.add_argument("--evidence", default="recall_certification_snapshot.csv")
    args = parser.parse_args()

    print(json.dumps(classify(args.vendor_csv, args.evidence), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
