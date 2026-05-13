# RecallGuard AI

Governed multi-agent product safety compliance checker for the Microsoft Foundry final activity.

## What Is Implemented

- **Knowledge Agent**: `recallguard-knowledge-agent` grounded with File Search over `knowledge-base/`.
- **Task Agent**: `recallguard-task-agent-v7-public-data` using Code Interpreter plus deterministic CSV evidence checks.
- **Sequential Workflow**: Knowledge Agent first, then Task Agent for evidence-check review requests, with a HITL note for `HOLD`.
- **Governance Evidence**: Microsoft DefaultV2 RAI policy evidence, guardrail notes, trace runbook, Entra Agent IDs, CLI setup evidence, and final build report.
- **Requirement Evidence**: explicit requirement-to-artifact coverage for quick review.
- **Runnable Checker**: Python package under `src/recallguard/` with pytest coverage for approve, review, hold, and prompt-injection edge cases.
- **Audit Layer**: product-level `decision_rule` and `reviewer_packet` outputs, plus a 25-row labeled evaluation harness.
- **Local Demo Server**: browser-based CSV checker for trying samples, pasted data, reviewer packets, and evaluation metrics.
- **Public Dataset Pipeline**: downloads and normalizes Korea Data Portal/KATS domestic recall CSV evidence into the Foundry demo snapshot.
- **Submission Assets**: PDF/DOCX report, MP4 demo, editable PPT deck, narration scripts, and packaged zip under `final/`.

## Current Azure Setup

- Subscription: Azure for Students
- Resource group: `rg-recallguard-foundry-je`
- Region: `japaneast`
- Foundry resource: `recallguard-somi-20260513`
- Foundry project: `recallguard-ai`
- Model deployment: `gpt-4o-mini`
- Demo model deployment: `gpt-4o-mini-100`
- Model SKU: `GlobalStandard`

## Submission-Focused Build Path

1. Use the files in `knowledge-base/` as the grounded knowledge source.
2. Use the files in `sample-data/` as Task Agent demo inputs.
3. Create two Foundry agents:
   - `RecallGuard Knowledge Agent`
   - `RecallGuard Task Agent public-data`
4. Create a Sequential workflow:
   - Knowledge Agent first
   - Task Agent second for evidence-check review requests
   - Human-in-the-loop note for `HOLD`
5. Capture Preview, Traces, Guardrails, and Entra Agent ID evidence.

See `docs/RecallGuard_AI_PRD.md` and `docs/Foundry_Final_Activity_Checklist.md`.

## Run Local Tests

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Run Decision Evaluation Harness

```bash
python scripts/evaluate_decision_harness.py
```

This evaluates 25 labeled vendor rows across `APPROVE`, `REVIEW`, and `HOLD`, then writes per-label precision/recall and mismatch details to `outputs/evaluation/decision_harness_report.json`. See `docs/Decision_Audit_and_Evaluation.md` for the decision table, recall-match thresholds, and human reviewer packet format.

## Run Local Browser Demo

```bash
python scripts/run_local_server.py
```

Then open `http://127.0.0.1:8765`. The local UI lets you run sample vendor CSVs, paste your own CSV rows, inspect `decision_rule` and `reviewer_packet` outputs, and load the 25-row evaluation metrics. See `docs/Local_Demo_Server.md`.

## Regenerate Public Recall Evidence

```bash
python scripts/prepare_public_recall_dataset.py
```

This downloads the KATS domestic product safety recall dataset from the Korea Data Portal, writes the original CSV to `data/raw/`, normalizes it under `data/processed/`, and appends a compact KATS recall snapshot to `sample-data/recall_certification_snapshot.csv` for Foundry Code Interpreter demos.

## Regenerate Artifacts

```bash
python scripts/build_submission_package.py
python scripts/build_ppt_video.py
node scripts/record_playwright_demo.cjs
```

The Foundry provisioning script is `scripts/setup_foundry_agents.sh`. It expects Azure CLI login and reads the AI Services key at runtime; no API keys are stored in this repository.
