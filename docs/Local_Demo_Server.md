# RecallGuard Local Demo Server

RecallGuard AI can be run locally as a lightweight browser demo. The server uses Python's standard HTTP server and the existing deterministic checker, so no web framework is required.

## Start the Server

```bash
python scripts/run_local_server.py
```

Open:

```text
http://127.0.0.1:8765
```

## What You Can Test

- Load the sample vendor CSVs from `sample-data/`
- Paste or edit CSV rows directly in the browser
- Run the checker and inspect `APPROVE`, `REVIEW`, and `HOLD` decisions
- View `decision_rule` and `reviewer_packet` output for each product
- Load the 25-row evaluation harness metrics from `outputs/evaluation/decision_harness_report.json`
- Use the Reviewer Copilot panel to ask why a decision was made, what evidence is missing, how guardrails apply, or to draft a reviewer memo

## Useful Samples

| Sample | Expected behavior |
|---|---|
| `vendor_products_complete.csv` | Two `APPROVE` decisions |
| `vendor_products_missing_fields.csv` | Two `REVIEW` decisions |
| `vendor_products_recall_match.csv` | One `HOLD`, one `APPROVE` |
| `vendor_products_prompt_injection.csv` | Treats embedded instructions as data |
| `vendor_products_public_recall_match.csv` | Creates `HOLD` from public KATS recall evidence |
| `evaluation/vendor_products_labeled.csv` | 25-row labeled evaluation set |

## API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | `GET` | Browser UI |
| `/api/samples` | `GET` | Lists sample CSV files |
| `/api/sample?name=<file>` | `GET` | Loads a sample CSV |
| `/api/classify` | `POST` | Runs the checker against pasted CSV text |
| `/api/evaluation` | `GET` | Returns saved evaluation harness metrics |
| `/api/decision-rules` | `GET` | Returns deterministic decision rules |

## Reviewer Copilot UX

The right-side Reviewer Copilot is a local deterministic prototype of the CopilotKit-style product experience. It does not replace Microsoft Foundry. Instead, it demonstrates how a future CopilotKit layer could sit on top of the governed Foundry workflow:

- Foundry remains responsible for grounded knowledge, tool execution, workflow traces, guardrails, and Entra governance.
- The local copilot panel explains the current selected product using the already-audited `decision_rule` and `reviewer_packet`.
- Future V2 work can replace the local panel with CopilotKit React components connected to the RecallGuard API and Foundry workflow.
