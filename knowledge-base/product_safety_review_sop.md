# Product Safety Review SOP

## Purpose

This SOP defines how RecallGuard AI triages vendor-submitted products before marketplace listing or procurement approval.

## Decision Labels

- `APPROVE`: Required product identifiers are present and no recall or certification risk is detected in available evidence.
- `REVIEW`: Evidence is incomplete, product identifiers are missing, or match confidence is weak.
- `HOLD`: A product strongly matches a recall notice, prohibited status, or unresolved safety risk.

## Required Review Evidence

The reviewer should check:

1. Product name
2. Model name or model number
3. Manufacturer or importer
4. Product category
5. KC certification number when the category is safety-regulated
6. Recall status
7. Corrective action or publication date when recall evidence exists

## Conservative Approval Rule

RecallGuard AI must not approve a product based only on product display name. If model name, manufacturer, or certification number is missing, the product should be classified as `REVIEW` unless recall evidence creates a stronger `HOLD` decision.

## Human Review Rule

Any `HOLD` decision requires human compliance review before vendor onboarding or listing approval.
