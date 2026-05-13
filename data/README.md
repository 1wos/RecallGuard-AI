# Public Recall Dataset

RecallGuard uses the Korean public dataset below as the real-world recall evidence source for the task agent.

- Source: Korea Data Portal, `산업통상부_국가기술표준원_제품안전_국내리콜정보`
- Detail page: https://www.data.go.kr/data/15040696/fileData.do
- Provider: Ministry of Trade, Industry and Energy / Korean Agency for Technology and Standards
- File format: CSV
- Rows in downloaded file: 881
- Last modified on the portal: 2025-09-05
- License scope shown on the portal: no usage restriction

## Files

- `raw/kats_product_safety_domestic_recall_20230809.csv`: original CP949-encoded CSV downloaded from data.go.kr.
- `processed/kats_domestic_recall_normalized.csv`: UTF-8 normalized evidence table used for analysis and repeatability.
- `processed/kats_domestic_recall_evidence_snapshot.csv`: compact snapshot appended to the Foundry demo evidence file.

## Regeneration

```bash
python scripts/prepare_public_recall_dataset.py
```

Use `--skip-download` to reuse the existing raw CSV and regenerate the normalized files only.
