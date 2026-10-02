from __future__ import annotations

import random
from datetime import datetime, timedelta

import pandas as pd

from config import RAW_DIR, LOG_DIR
from utils import get_logger

logger = get_logger("generate_data", LOG_DIR / "pipeline.log")

CUSTOMERS = [
    (1, "Ana Cruz", "Metro Manila"),
    (2, "Ben Santos", "Cebu"),
    (3, "Cara Lim", "Davao"),
    (4, "Diego Reyes", "Metro Manila"),
    (5, "Ella Tan", "Iloilo"),
    (6, "Francis Yu", "Cebu"),
    (7, "Grace Ong", "Metro Manila"),
    (8, "Henry Ramos", "Davao"),
]

PRODUCTS = [
    (101, "Mechanical Keyboard", "Electronics", 3200.0),
    (102, "Wireless Mouse", "Electronics", 1400.0),
    (103, "USB-C Hub", "Electronics", 2200.0),
    (201, "Notebook", "Office", 180.0),
    (202, "Desk Organizer", "Office", 650.0),
    (301, "Water Bottle", "Lifestyle", 900.0),
    (302, "Backpack", "Lifestyle", 2500.0),
]


def build_orders(n: int = 500, seed: int = 42) -> pd.DataFrame:
    random.seed(seed)
    start = datetime(2026, 1, 1)
    rows = []

    for order_id in range(1, n + 1):
        customer = random.choice(CUSTOMERS)
        product = random.choice(PRODUCTS)
        quantity = random.randint(1, 4)
        order_date = start + timedelta(days=random.randint(0, 270))
        status = random.choices(
            ["completed", "cancelled", "pending"], weights=[0.82, 0.10, 0.08], k=1
        )[0]

        # Inject a few deliberately messy values so Silver has real work to do.
        unit_price = product[3]
        if order_id % 111 == 0:
            unit_price = -unit_price
        region = customer[2]
        if order_id % 97 == 0:
            region = None

        rows.append(
            {
                "order_id": order_id,
                "order_timestamp": order_date.strftime("%Y-%m-%d %H:%M:%S"),
                "customer_id": customer[0],
                "customer_name": customer[1],
                "region": region,
                "product_id": product[0],
                "product_name": product[1],
                "category": product[2],
                "quantity": quantity,
                "unit_price": unit_price,
                "status": status,
            }
        )

    # Add duplicates to simulate ingestion problems.
    rows.extend([rows[10].copy(), rows[25].copy(), rows[25].copy()])
    return pd.DataFrame(rows)


def main() -> None:
    output = RAW_DIR / "orders.csv"
    df = build_orders()
    df.to_csv(output, index=False)
    logger.info("Generated %s raw rows at %s", len(df), output)


if __name__ == "__main__":
    main()
