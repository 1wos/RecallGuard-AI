# Public Data Dataset Evidence

## Dataset Selected

RecallGuard AI uses the Korea Data Portal KATS domestic product safety recall dataset as the public recall evidence source.

- Detail page: https://www.data.go.kr/data/15040696/fileData.do
- Direct CSV download captured from the portal metadata: `https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000002784452&fileDetailSn=1&insertDataPrcus=N`
- Provider: Ministry of Trade, Industry and Energy / Korean Agency for Technology and Standards
- Portal description: domestic product safety recall information including product name, model name, manufacturer/importer, and recall information.
- Portal metadata observed: CSV, 881 rows, registered 2023-08-10, modified 2025-09-05.

## Local Processing

The source CSV is CP949 encoded. The script below downloads the file, normalizes it to UTF-8, and maps Korean source columns to the evidence schema used by the RecallGuard Task Agent.

```bash
python scripts/prepare_public_recall_dataset.py
```

Column mapping:

| Source column | RecallGuard field |
| --- | --- |
| `인증번호` | `kc_certification_number` |
| `제품명` | `product_name` |
| `모델명` | `model_name` |
| `리콜사업자명` / `제조사명` | `manufacturer` |
| `위해유형` + `리콜종류` | `recall_reason` |
| `리콜방법` | `corrective_action` |
| `등록일` | `publication_date` |

## Foundry Usage

The full normalized dataset is stored under `data/processed/`. A compact public-data snapshot is appended to `sample-data/recall_certification_snapshot.csv` so the Foundry Code Interpreter task agent can run quickly during a live demo while still carrying real KATS recall evidence.
