from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"
LOG_DIR = ROOT / "logs"

for path in [RAW_DIR, BRONZE_DIR, SILVER_DIR, GOLD_DIR, LOG_DIR]:
    path.mkdir(parents=True, exist_ok=True)
