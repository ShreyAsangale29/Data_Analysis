# LinkedIn Video Walkthrough (3–5 minutes)

## 1) Objective (20–30 sec)
- "I was tasked to rapidly immerse in a business dataset and produce analysis-ready data."
- Mention business use case (sales/customer/website analytics).

## 2) Data Familiarization (45–60 sec)
- Show `outputs/data_dictionary.csv`.
- Explain how each column includes:
  - Data type
  - Missingness
  - Example values
  - Business relevance hint
  - Final business definition (added manually)

## 3) Quality Issues Identified (60–90 sec)
- Show `outputs/data_quality_report.csv` and summarize:
  - Missing values hotspots
  - Duplicate rows/values
  - Formatting inconsistencies
  - Outlier-heavy numeric columns

## 4) Cleaning & Transformation Logic (60–90 sec)
- Open `scripts/02_clean_transform.py` and narrate:
  - Deduplication
  - Null handling strategy
  - Date normalization
  - Category standardization
  - Feature engineering (`customer_age`)
  - Outlier handling

## 5) Final Output & Impact (30–45 sec)
- Show `outputs/cleaned_dataset.csv`.
- Explain why this is now analysis-ready and what dashboards/models could come next.

## Suggested closing
- "A robust cleaning pipeline improves trust in insights and speeds up downstream analysis."
