# Data Immersion & Wrangling Starter Pack

This repository is structured to help an intern complete the **data access, familiarization, quality assessment, cleaning, and transformation** workflow quickly and in a repeatable way.

## Deliverables mapping

- **GitHub Deliverables**
  - `outputs/data_dictionary.csv` → variable meaning, type, sample values, business relevance hints.
  - `scripts/02_clean_transform.py` → data cleaning and transformation script.
  - `outputs/cleaned_dataset.csv` → final analysis-ready dataset.
- **LinkedIn video (3–5 min)**
  - Use the guide in `docs/linkedin_walkthrough_outline.md`.

## Recommended workflow

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

## Notes

- If your dataset uses different date/DOB column names, update constants at the top of `scripts/02_clean_transform.py`.
- You can adapt this workflow to SQL by implementing equivalent staging + cleaning queries.
