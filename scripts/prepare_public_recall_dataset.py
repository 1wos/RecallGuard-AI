from __future__ import annotations

import argparse
import csv
import urllib.request
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_GO_DETAIL_URL = "https://www.data.go.kr/data/15040696/fileData.do"
DATA_GO_DOWNLOAD_URL = (
    "https://www.data.go.kr/cmm/cmm/fileDownload.do"
    "?atchFileId=FILE_000000002784452&fileDetailSn=1&insertDataPrcus=N"
)

RAW_PATH = ROOT / "data/raw/kats_product_safety_domestic_recall_20230809.csv"
NORMALIZED_PATH = ROOT / "data/processed/kats_domestic_recall_normalized.csv"
PUBLIC_EVIDENCE_PATH = ROOT / "data/processed/kats_domestic_recall_evidence_snapshot.csv"
FOUNDRY_EVIDENCE_PATH = ROOT / "sample-data/recall_certification_snapshot.csv"

SOURCE_NAME = "KATS public data: domestic product safety recall information"
SOURCE_CITATION = f"{SOURCE_NAME} ({DATA_GO_DETAIL_URL})"


def download_public_csv(destination: Path = RAW_PATH) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        DATA_GO_DOWNLOAD_URL,
        headers={"User-Agent": "Mozilla/5.0 RecallGuardAI/1.0"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        destination.write_bytes(response.read())
    return destination


def read_korean_csv(path: Path) -> pd.DataFrame:
    for encoding in ("utf-8-sig", "cp949", "euc-kr"):
        try:
            return pd.read_csv(path, encoding=encoding).fillna("")
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("unknown", b"", 0, 1, f"Could not decode {path}")


def join_non_empty(*parts: object, separator: str = " | ") -> str:
    values = [str(part).strip() for part in parts if str(part).strip()]
    return separator.join(dict.fromkeys(values))


def normalize_recall_dataset(raw_csv: Path = RAW_PATH) -> pd.DataFrame:
    raw = read_korean_csv(raw_csv)
    records: list[dict[str, str]] = []

    for index, row in raw.iterrows():
        evidence_id = f"KATS-RECALL-{index + 1:04d}"
        manufacturer = str(row.get("리콜사업자명", "")).strip() or str(row.get("제조사명", "")).strip()
        recall_reason = join_non_empty(row.get("위해유형", ""), row.get("리콜종류", ""))

        records.append(
            {
                "evidence_id": evidence_id,
                "evidence_type": "recall",
                "product_name": str(row.get("제품명", "")).strip(),
                "model_name": str(row.get("모델명", "")).strip(),
                "manufacturer": manufacturer,
                "kc_certification_number": str(row.get("인증번호", "")).strip(),
                "recall_reason": recall_reason,
                "corrective_action": str(row.get("리콜방법", "")).strip(),
                "publication_date": str(row.get("등록일", "")).strip(),
                "source": SOURCE_CITATION,
                "brand_name": str(row.get("브랜드명", "")).strip(),
                "business_type": str(row.get("사업자구분", "")).strip(),
                "legal_category": str(row.get("법정제품분류", "")).strip(),
                "manufacturer_country": str(row.get("제조사국가명", "")).strip(),
                "raw_source_row": str(index + 1),
            }
        )

    return pd.DataFrame.from_records(records)


def write_csv(df: pd.DataFrame, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8", quoting=csv.QUOTE_MINIMAL)
    return path


def update_foundry_evidence(public_evidence: pd.DataFrame, rows: int) -> Path:
    existing = pd.read_csv(FOUNDRY_EVIDENCE_PATH).fillna("")
    keep_existing = existing[
        ~existing["evidence_id"].astype(str).str.startswith("KATS-RECALL-")
    ].copy()

    foundry_columns = list(existing.columns)
    public_subset = public_evidence.head(rows).reindex(columns=foundry_columns, fill_value="")
    combined = pd.concat([keep_existing, public_subset], ignore_index=True)
    return write_csv(combined, FOUNDRY_EVIDENCE_PATH)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download and normalize the KATS domestic product safety recall public dataset."
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Reuse the existing raw CSV instead of downloading from data.go.kr.",
    )
    parser.add_argument(
        "--foundry-snapshot-rows",
        type=int,
        default=30,
        help="Number of public recall rows to append to sample-data/recall_certification_snapshot.csv.",
    )
    args = parser.parse_args()

    raw_path = RAW_PATH
    if not args.skip_download or not raw_path.exists():
        raw_path = download_public_csv()

    normalized = normalize_recall_dataset(raw_path)
    write_csv(normalized, NORMALIZED_PATH)
    write_csv(normalized.head(args.foundry_snapshot_rows), PUBLIC_EVIDENCE_PATH)
    update_foundry_evidence(normalized, args.foundry_snapshot_rows)

    print(
        "\n".join(
            [
                f"download_url={DATA_GO_DOWNLOAD_URL}",
                f"raw_csv={RAW_PATH}",
                f"raw_rows={len(normalized)}",
                f"normalized_csv={NORMALIZED_PATH}",
                f"public_evidence_snapshot={PUBLIC_EVIDENCE_PATH}",
                f"foundry_evidence_snapshot={FOUNDRY_EVIDENCE_PATH}",
            ]
        )
    )


if __name__ == "__main__":
    main()
