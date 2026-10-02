from __future__ import annotations

import duckdb
import pandas as pd

from config import SILVER_DIR, GOLD_DIR, LOG_DIR
from utils import get_logger

logger = get_logger("gold", LOG_DIR / "pipeline.log")


def run_gold() -> dict[str, pd.DataFrame]:
    source = SILVER_DIR / "orders_silver.parquet"
    db_path = GOLD_DIR / "analytics.duckdb"

    con = duckdb.connect(str(db_path))
    source_sql = str(source).replace("\\", "/").replace("'", "''")
    con.execute(f"CREATE OR REPLACE VIEW silver_orders AS SELECT * FROM read_parquet('{source_sql}')")

    monthly_sales = con.execute(
        """
        SELECT
            order_month,
            COUNT(DISTINCT order_id) AS orders,
            SUM(CASE WHEN status = 'completed' THEN gross_amount ELSE 0 END) AS completed_revenue,
            AVG(CASE WHEN status = 'completed' THEN gross_amount END) AS avg_order_value
        FROM silver_orders
        GROUP BY order_month
        ORDER BY order_month
        """
    ).df()

    category_sales = con.execute(
        """
        SELECT
            category,
            COUNT(DISTINCT CASE WHEN status = 'completed' THEN order_id END) AS completed_orders,
            SUM(CASE WHEN status = 'completed' THEN gross_amount ELSE 0 END) AS revenue
        FROM silver_orders
        GROUP BY category
        ORDER BY revenue DESC
        """
    ).df()

    region_sales = con.execute(
        """
        SELECT
            region,
            COUNT(DISTINCT CASE WHEN status = 'completed' THEN order_id END) AS completed_orders,
            SUM(CASE WHEN status = 'completed' THEN gross_amount ELSE 0 END) AS revenue
        FROM silver_orders
        GROUP BY region
        ORDER BY revenue DESC
        """
    ).df()

    status_summary = con.execute(
        """
        SELECT
            status,
            COUNT(*) AS order_count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_orders
        FROM silver_orders
        GROUP BY status
        ORDER BY order_count DESC
        """
    ).df()

    tables = {
        "monthly_sales": monthly_sales,
        "category_sales": category_sales,
        "region_sales": region_sales,
        "status_summary": status_summary,
    }

    for name, df in tables.items():
        df.to_parquet(GOLD_DIR / f"{name}.parquet", index=False)
        con.register("tmp_df", df)
        con.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM tmp_df")
        con.unregister("tmp_df")

    con.close()
    logger.info("Gold complete: %s marts created in %s", len(tables), GOLD_DIR)
    return tables


if __name__ == "__main__":
    run_gold()
