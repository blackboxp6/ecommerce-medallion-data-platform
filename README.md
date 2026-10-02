# Medallion Architecture Data Engineering Project

A portfolio-ready local data engineering project that demonstrates the **Medallion Architecture**:

- **Raw**: source CSV exactly as received.
- **Bronze**: immutable-ish raw ingestion stored as Parquet with ingestion metadata.
- **Silver**: cleaned, typed, deduplicated, validated, enriched business-ready data.
- **Gold**: aggregated analytics marts for BI and reporting.

## Architecture

```text
CSV source
   |
   v
Raw Layer
   |
   v
Bronze Parquet
   |
   v
Silver Parquet
   |
   +--> Data Quality Checks
   |
   v
Gold Parquet + DuckDB analytics database
   |
   v
Power BI / SQL / Dashboard
```

## Tech Stack

- Python
- pandas
- PyArrow / Parquet
- DuckDB
- pytest
- VS Code

## Project Structure

```text
medallion-data-engineering/
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── logs/
├── sql/
│   └── example_queries.sql
├── src/
│   ├── config.py
│   ├── utils.py
│   ├── generate_data.py
│   ├── bronze.py
│   ├── silver.py
│   ├── data_quality.py
│   ├── gold.py
│   └── main.py
├── tests/
│   └── test_silver_rules.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Windows / VS Code Setup

### 1. Open the project

Open VS Code, then choose **File -> Open Folder** and select this project folder.

### 2. Create a virtual environment

In the VS Code terminal:

```powershell
py -3.12 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the full pipeline

```powershell
python src/main.py
```

The pipeline will automatically:

1. Generate sample raw order data.
2. Write the Bronze layer.
3. Clean and enrich the data into Silver.
4. Run data-quality checks.
5. Build Gold marts and a DuckDB analytics database.

### 5. Run tests

```powershell
pytest -q
```

## Layer Details

### Raw

`data/raw/orders.csv`

This simulates a source-system extract. Do not clean it here. The purpose is to preserve what arrived from the source.

### Bronze

`data/bronze/orders_bronze.parquet`

Bronze keeps source values close to the original representation and adds metadata:

- `_ingested_at_utc`
- `_source_file`

This gives traceability and auditability.

### Silver

`data/silver/orders_silver.parquet`

Silver performs:

- schema checks
- type conversion
- text normalization
- null handling
- duplicate removal
- invalid-price filtering
- invalid-quantity filtering
- status validation
- derived columns such as `gross_amount`, `order_date`, and `order_month`

### Gold

Gold produces business-facing marts:

- `monthly_sales.parquet`
- `category_sales.parquet`
- `region_sales.parquet`
- `status_summary.parquet`
- `analytics.duckdb`

These are intentionally shaped for downstream BI tools.

## How to Explain This in an Interview

> I built a local Medallion Architecture pipeline where raw transactional data is preserved in a Raw/Bronze layer, standardized and quality-controlled in Silver, and transformed into business-facing Gold marts. I used Parquet for columnar storage, DuckDB for analytical SQL, automated quality checks for integrity, and pytest for code-level validation. The structure is designed so the local file system can later be replaced by object storage such as Amazon S3 or Azure Data Lake while preserving the same Bronze-Silver-Gold transformation pattern.

## Suggested Portfolio Extensions

1. Replace generated CSV with an API or public dataset.
2. Add incremental ingestion using ingestion timestamps.
3. Add SODA or Great Expectations.
4. Add Airflow or Prefect orchestration.
5. Add Docker.
6. Add dbt models for Gold transformations.
7. Connect Power BI to the Gold layer.
8. Migrate storage to AWS S3 or Azure Data Lake.
9. Add CI with GitHub Actions.
10. Reimplement the same architecture in Databricks using Delta Lake.
