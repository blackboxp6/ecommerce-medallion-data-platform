from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

from config import RAW_DIR, BRONZE_DIR, LOG_DIR
from utils import get_logger

logger = get_logger("bronze", LOG_DIR / "pipeline.log")


def run_bronze() -> pd.DataFrame:
    source = RAW_DIR / "orders.csv"
    target = BRONZE_DIR / "orders_bronze.parquet"

    if not source.exists():
        raise FileNotFoundError(f"Missing raw source: {source}. Run generate_data.py first.")

    df = pd.read_csv(source, dtype=str)
    df["_ingested_at_utc"] = datetime.now(timezone.utc).isoformat()
    df["_source_file"] = source.name

    df.to_parquet(target, index=False)
    logger.info("Bronze complete: %s rows -> %s", len(df), target)
    return df


if __name__ == "__main__":
    run_bronze()
