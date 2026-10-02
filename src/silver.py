from __future__ import annotations

import pandas as pd

from config import BRONZE_DIR, SILVER_DIR, LOG_DIR
from utils import get_logger

logger = get_logger("silver", LOG_DIR / "pipeline.log")

REQUIRED_COLUMNS = [
    "order_id",
    "order_timestamp",
    "customer_id",
    "region",
    "product_id",
    "category",
    "quantity",
    "unit_price",
    "status",
]


def run_silver() -> pd.DataFrame:
    source = BRONZE_DIR / "orders_bronze.parquet"
    target = SILVER_DIR / "orders_silver.parquet"

    df = pd.read_parquet(source)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Standardize data types.
    df["order_id"] = pd.to_numeric(df["order_id"], errors="coerce").astype("Int64")
    df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce").astype("Int64")
    df["product_id"] = pd.to_numeric(df["product_id"], errors="coerce").astype("Int64")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").astype("Int64")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["order_timestamp"] = pd.to_datetime(df["order_timestamp"], errors="coerce")

    # Normalize text fields.
    df["status"] = df["status"].str.strip().str.lower()
    df["category"] = df["category"].str.strip().str.title()
    df["region"] = df["region"].fillna("Unknown").str.strip()

    before = len(df)
    df = df.drop_duplicates(subset=["order_id"], keep="first")
    duplicates_removed = before - len(df)

    # Business/data-quality rules.
    df = df.dropna(subset=["order_id", "order_timestamp", "customer_id", "product_id"])
    df = df[df["quantity"] > 0]
    df = df[df["unit_price"] > 0]
    df = df[df["status"].isin(["completed", "cancelled", "pending"])]

    df["gross_amount"] = df["quantity"].astype(float) * df["unit_price"]
    df["order_date"] = df["order_timestamp"].dt.date
    df["order_month"] = df["order_timestamp"].dt.to_period("M").astype(str)

    df.to_parquet(target, index=False)
    logger.info(
        "Silver complete: %s valid rows -> %s; duplicates removed=%s",
        len(df),
        target,
        duplicates_removed,
    )
    return df


if __name__ == "__main__":
    run_silver()
