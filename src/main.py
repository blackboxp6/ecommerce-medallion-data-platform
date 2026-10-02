from generate_data import main as generate_raw
from bronze import run_bronze
from silver import run_silver
from data_quality import run_quality_checks
from gold import run_gold


def main() -> None:
    print("\n=== MEDALLION PIPELINE START ===")
    generate_raw()
    run_bronze()
    run_silver()
    run_quality_checks()
    marts = run_gold()

    print("\n=== PIPELINE COMPLETE ===")
    for name, df in marts.items():
        print(f"\n{name}")
        print(df.head())


if __name__ == "__main__":
    main()
