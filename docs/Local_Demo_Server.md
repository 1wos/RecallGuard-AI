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
