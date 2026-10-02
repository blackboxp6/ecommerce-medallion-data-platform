import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from generate_data import build_orders


def test_generated_orders_have_expected_columns():
    df = build_orders(n=20)
    expected = {"order_id", "customer_id", "product_id", "quantity", "unit_price", "status"}
    assert expected.issubset(df.columns)


def test_generated_data_contains_rows():
    df = build_orders(n=20)
    assert len(df) >= 20
