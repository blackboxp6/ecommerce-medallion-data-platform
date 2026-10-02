from __future__ import annotations

import pandas as pd

from config import SILVER_DIR, LOG_DIR
from utils import get_logger

logger = get_logger("data_quality", LOG_DIR / "pipeline.log")


def run_quality_checks() -> None:
    source = SILVER_DIR / "orders_silver.parquet"
    df = pd.read_parquet(source)

    checks = {
        "order_id_unique": df["order_id"].is_unique,
        "order_id_not_null": df["order_id"].notna().all(),
        "positive_quantity": (df["quantity"] > 0).all(),
        "positive_unit_price": (df["unit_price"] > 0).all(),
        "valid_status": df["status"].isin(["completed", "cancelled", "pending"]).all(),
        "gross_amount_consistent": (
            (df["gross_amount"] - (df["quantity"].astype(float) * df["unit_price"])).abs() < 1e-9
        ).all(),
    }

    failed = [name for name, passed in checks.items() if not passed]
    for name, passed in checks.items():
        logger.info("DQ check %-25s : %s", name, "PASS" if passed else "FAIL")

    if failed:
        raise AssertionError(f"Data quality checks failed: {failed}")
