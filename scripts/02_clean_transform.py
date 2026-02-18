#!/usr/bin/env python3
"""Clean and transform a raw dataset into an analysis-ready dataset.

Usage:
  python scripts/02_clean_transform.py --input data/raw_dataset.csv --output outputs/cleaned_dataset.csv
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


POSSIBLE_DATE_COLUMNS = ["date", "transaction_date", "signup_date", "created_at"]
POSSIBLE_DOB_COLUMNS = ["dob", "date_of_birth", "birth_date"]


def normalize_strings(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if pd.api.types.is_object_dtype(df[col]):
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({"": np.nan, "nan": np.nan, "None": np.nan})
    return df


def standardize_dates(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if any(token in col.lower() for token in ["date", "time"]):
            converted = pd.to_datetime(df[col], errors="coerce")
            if converted.notna().sum() > 0:
                df[col] = converted.dt.strftime("%Y-%m-%d")
    return df


def cap_numeric_outliers(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        series = df[col]
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        if pd.notna(iqr) and iqr > 0:
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            df[col] = series.clip(lower=lower, upper=upper)
    return df


def categorize_text_fields(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if pd.api.types.is_object_dtype(df[col]) and df[col].nunique(dropna=True) < 20:
            df[col] = df[col].str.lower()
    return df


def create_customer_age(df: pd.DataFrame, reference_date: str | None = None) -> pd.DataFrame:
    dob_col = next((c for c in df.columns if c.lower() in POSSIBLE_DOB_COLUMNS), None)
    if not dob_col:
        return df

    dob = pd.to_datetime(df[dob_col], errors="coerce")
    if reference_date:
        ref = pd.to_datetime(reference_date)
    else:
        ref = pd.Timestamp(datetime.today().date())

    age = (ref - dob).dt.days // 365
    df["customer_age"] = age.where(age.between(0, 120), np.nan)
    return df


def clean_dataset(df: pd.DataFrame, reference_date: str | None = None) -> pd.DataFrame:
    df = df.copy()

    # 1) Deduplicate exact duplicate rows
    df = df.drop_duplicates()

    # 2) Standardize strings and dates
    df = normalize_strings(df)
    df = standardize_dates(df)

    # 3) Handle missing values
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            mode_vals = df[col].mode(dropna=True)
            if len(mode_vals) > 0:
                df[col] = df[col].fillna(mode_vals.iloc[0])

    # 4) Categorize low-cardinality text fields
    df = categorize_text_fields(df)

    # 5) Feature engineering
    df = create_customer_age(df, reference_date=reference_date)

    # 6) Outlier treatment for numeric columns
    df = cap_numeric_outliers(df)

    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean and transform raw CSV dataset.")
    parser.add_argument("--input", required=True, help="Path to raw CSV dataset.")
    parser.add_argument("--output", required=True, help="Path to cleaned output CSV.")
    parser.add_argument("--reference-date", default=None, help="Reference date for age calculation (YYYY-MM-DD).")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    raw_df = pd.read_csv(input_path)
    cleaned_df = clean_dataset(raw_df, reference_date=args.reference_date)
    cleaned_df.to_csv(output_path, index=False)

    print(f"Saved cleaned dataset to: {output_path}")
    print(f"Rows: {len(cleaned_df)}, Columns: {len(cleaned_df.columns)}")


if __name__ == "__main__":
    main()
