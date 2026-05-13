# RecallGuard Decision Audit and Evaluation

This document captures the post-review assurance layer for RecallGuard AI. It makes the deterministic Task Agent behavior easier to audit by documenting the decision table, recall-match thresholds, human reviewer packet, and labeled evaluation harness.

## Decision Table

| Rule ID | Decision | Trigger | Human review | Rationale |
|---|---|---|---|---|
| `HOLD_RECALL_STRONG_MATCH` | `HOLD` | Evidence row has `evidence_type = recall` and either exact KC certification number match or exact model + manufacturer match | Required | A strong recall match creates a safety stop before listing or procurement approval. |
| `REVIEW_MISSING_IDENTIFIERS` | `REVIEW` | Required product identifiers are missing: `product_name`, `model_name`, or `manufacturer` | Required | Missing identifiers make matching unreliable, so approval is blocked until evidence is complete. |
| `APPROVE_CERTIFICATION_HIGH_CONFIDENCE` | `APPROVE` | Certification evidence has high-confidence exact KC certification number or exact model + manufacturer match, with no strong recall match | Not required | The item has sufficient certification evidence and no recall evidence in the available snapshot. |
| `REVIEW_WEAK_CERTIFICATION_MATCH` | `REVIEW` | Only product-name certification evidence is found | Required | Product-name-only matching is ambiguous and cannot justify approval by itself. |
| `REVIEW_NO_EVIDENCE` | `REVIEW` | No strong certification evidence and no strong recall evidence are found | Required | The workflow needs more evidence or manual review before approval. |

Decision precedence is intentionally conservative:

1. Strong recall match creates `HOLD`.
2. Missing required identifiers create `REVIEW`.
3. High-confidence certification match can create `APPROVE`.
4. Weak product-name-only evidence creates `REVIEW`.
5. No evidence creates `REVIEW`.

## Recall Match Thresholds

RecallGuard treats recall evidence as safety-critical. A recall row can create `HOLD` only when the match is strong:

| Match signal | Confidence | Can create `HOLD`? | Notes |
|---|---:|---|---|
| Exact KC certification number match against `evidence_type = recall` | High | Yes | Certification number is treated as a unique product evidence key when present. |
| Exact model + manufacturer match against `evidence_type = recall` | High | Yes | Requires both model and manufacturer to match after normalization. |
| Product-name-only match against `evidence_type = recall` | Low | No | Product names are often reused or translated; this creates `REVIEW`, not `HOLD`. |
| Category-only match | Low | No | Category is useful context but never enough for a decision. |
| Manufacturer-only match | Low | No | Manufacturer-only evidence is too broad for a product-level decision. |
| Fuzzy product name or partial model match | Low | No | Current MVP intentionally avoids fuzzy auto-holds. These cases should be escalated through `REVIEW`. |

Normalization is case-insensitive and trims whitespace. Korean public KATS recall rows are supported as exact-string evidence rows in the snapshot.

## Human Reviewer Packet

Each product-level result now includes a `reviewer_packet` object so a compliance owner can inspect the decision without reading raw agent traces.

```json
{
  "decision": "HOLD",
  "decision_rule": "HOLD_RECALL_STRONG_MATCH",
  "human_review_required": true,
  "evidence_cited": [
    {
      "evidence_id": "RC-001",
      "evidence_type": "recall",
      "match_type": "model_manufacturer",
      "match_confidence": "high",
      "source": "KATS public data snapshot"
    }
  ],
  "missing_data": [],
  "risk_rationale": ["Strong recall match found."],
  "recommended_next_action": "Escalate to compliance owner before listing."
}
```

## Before and After: False HOLD Fix

| Version | Behavior | Risk | Fix |
|---|---|---|---|
| Early classifier | Certification evidence could be interpreted as a safety hold | False `HOLD` could delay safe products and reduce trust in the workflow | Split evidence handling by `evidence_type`; only recall evidence can create `HOLD`. |
| Current classifier | Certification evidence supports `APPROVE` or `REVIEW`; recall evidence creates `HOLD` only on strong matches | More auditable, less over-blocking | Deterministic decision rules are encoded in `src/recallguard/checker.py` and tested. |

## Labeled Evaluation Harness

The labeled harness is stored at:

```text
sample-data/evaluation/vendor_products_labeled.csv
```

It contains 25 rows covering:

- High-confidence certification approvals
- Strong recall holds
- Public KATS recall evidence
- Missing identifier reviews
- Weak product-name-only matches
- Prompt-injection text treated as data
- Case-insensitive normalization
- No-evidence reviews

Run it with:

```bash
python scripts/evaluate_decision_harness.py
```

The script writes:

```text
outputs/evaluation/decision_harness_report.json
```

The report includes total accuracy, per-label precision and recall, case-type metrics, and mismatch details with reviewer packets for any failed row.
