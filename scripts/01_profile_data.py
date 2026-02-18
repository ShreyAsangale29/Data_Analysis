
Usage:
  python scripts/01_profile_data.py --input data/raw_dataset.csv --output-dir outputs
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def infer_business_relevance(column_name: str) -> str:
    """Simple heuristic prompt to help intern think about business meaning."""
    lowered = column_name.lower()
    if "id" in lowered:
        return "Likely unique identifier useful for joins, deduplication, and traceability."
    if "date" in lowered or "time" in lowered:
        return "Supports trend analysis, seasonality checks, and cohort reporting."
    if any(k in lowered for k in ["amount", "price", "revenue", "cost", "sales"]):
        return "Core financial metric for KPI tracking and profitability analysis."
    if any(k in lowered for k in ["customer", "user", "client"]):
        return "Entity descriptor useful for segmentation and retention analysis."
    if any(k in lowered for k in ["country", "city", "region", "state"]):
        return "Geographic segmentation and regional performance reporting."
    return "Review with domain expert to define business relevance."


def profile_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    missing_counts = df.isna().sum()
    missing_pct = (missing_counts / len(df) * 100).round(2) if len(df) > 0 else 0
    duplicate_rows = int(df.duplicated().sum())

    data_dictionary = pd.DataFrame(
        {
            "column_name": df.columns,
            "data_type": [str(dtype) for dtype in df.dtypes],
            "non_null_count": [int(df[col].notna().sum()) for col in df.columns],
            "missing_count": [int(missing_counts[col]) for col in df.columns],
            "missing_pct": [float(missing_pct[col]) if len(df) > 0 else 0.0 for col in df.columns],
            "unique_count": [int(df[col].nunique(dropna=True)) for col in df.columns],
            "sample_values": [", ".join(map(str, df[col].dropna().head(3).tolist())) for col in df.columns],
            "business_relevance_hint": [infer_business_relevance(col) for col in df.columns],
            "variable_definition": "",
        }
    )

    quality_records = []
    for col in df.columns:
        series = df[col]
        rec = {
            "column_name": col,
            "missing_count": int(series.isna().sum()),
            "duplicate_value_count": int(series.duplicated().sum()),
            "inconsistent_whitespace_count": int(series.astype(str).str.contains(r"^\s|\s$", regex=True, na=False).sum())
            if pd.api.types.is_string_dtype(series)
            else 0,
            "outlier_count_iqr": 0,
        }
        if pd.api.types.is_numeric_dtype(series):
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            if pd.notna(iqr) and iqr > 0:
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                rec["outlier_count_iqr"] = int(series[(series < lower) | (series > upper)].count())
        quality_records.append(rec)

    quality_summary = pd.DataFrame(quality_records)
    quality_summary.insert(0, "dataset_row_count", len(df))
    quality_summary.insert(1, "dataset_duplicate_rows", duplicate_rows)

    return data_dictionary, quality_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate data dictionary and quality profile outputs.")
    parser.add_argument("--input", required=True, help="Path to raw CSV dataset.")
    parser.add_argument("--output-dir", default="outputs", help="Directory for generated outputs.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    data_dictionary, quality_summary = profile_dataframe(df)

    data_dict_path = output_dir / "data_dictionary.csv"
    quality_path = output_dir / "data_quality_report.csv"

    data_dictionary.to_csv(data_dict_path, index=False)
    quality_summary.to_csv(quality_path, index=False)

    print(f"Generated data dictionary: {data_dict_path}")
    print(f"Generated data quality report: {quality_path}")


if __name__ == "__main__":
    main()
