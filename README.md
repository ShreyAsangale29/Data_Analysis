# Data Immersion & Wrangling 

This repository is about the **data access, familiarization, quality assessment, cleaning, and transformation** workflow quickly and in a repeatable way.

## 1) Data Access & Familiarization

1. Put the raw file in `data/raw_dataset.csv`.
2. Run profiling script:

```bash
python scripts/01_profile_data.py --input data/raw_dataset.csv --output-dir outputs
```

3. Open `outputs/data_dictionary.csv` and complete the `variable_definition` column with domain knowledge.

## 2) Data Quality Assessment

Review `outputs/data_quality_report.csv` for:
- Missing values
- Duplicates (dataset-level and column-level)
- Inconsistent leading/trailing whitespace
- Potential outliers (IQR-based count for numeric fields)

## 3) Data Cleaning & Transformation

Run:

```bash
python scripts/02_clean_transform.py --input data/raw_dataset.csv --output outputs/cleaned_dataset.csv
```

What the cleaning script does:
- Removes exact duplicate rows
- Standardizes string whitespace and null-like values
- Converts date/time-like columns to `YYYY-MM-DD`
- Imputes missing values (median for numeric, mode for categorical)
- Lowercases low-cardinality text categories
- Creates `customer_age` when a DOB-like column exists
- Caps numeric outliers using IQR fences

## Optional setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install pandas numpy
```


