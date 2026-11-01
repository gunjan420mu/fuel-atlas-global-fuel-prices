"""Load the supplied CSV into a local SQLite database for the Flask project."""
from __future__ import annotations

import csv
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "data" / "global_fuel_prices_Dataset.csv"
DB_PATH = ROOT / "fuel_prices.db"


def main() -> None:
    if not CSV_PATH.exists():
        raise SystemExit(f"Dataset not found: {CSV_PATH}")
    with sqlite3.connect(DB_PATH) as db, CSV_PATH.open(encoding="utf-8-sig", newline="") as source:
        db.execute("DROP TABLE IF EXISTS fuel_prices")
        db.execute("""CREATE TABLE fuel_prices (
            date TEXT NOT NULL, country TEXT NOT NULL, region TEXT NOT NULL,
            income_level TEXT NOT NULL, subsidy_level TEXT NOT NULL,
            petrol_usd_liter REAL NOT NULL, diesel_usd_liter REAL NOT NULL,
            lpg_usd_liter REAL NOT NULL, brent_crude_usd REAL NOT NULL,
            tax_percentage REAL NOT NULL
        )""")
        reader = csv.DictReader(source)
        rows = []
        for row in reader:
            rows.append((
                datetime.strptime(row["date"], "%d-%m-%Y").date().isoformat(),
                row["country"], row["region"], row["income_level"], row["subsidy_level"],
                float(row["petrol_usd_liter"]), float(row["diesel_usd_liter"]),
                float(row["lpg_usd_liter"]), float(row["brent_crude_usd"]),
                float(row["tax_percentage"]),
            ))
        db.executemany("INSERT INTO fuel_prices VALUES (?,?,?,?,?,?,?,?,?,?)", rows)
        db.execute("CREATE INDEX idx_fuel_date ON fuel_prices(date)")
        db.execute("CREATE INDEX idx_fuel_region_country ON fuel_prices(region,country)")
        db.execute("CREATE INDEX idx_fuel_policy ON fuel_prices(income_level,subsidy_level)")
        db.commit()
    print(f"Loaded {len(rows):,} rows into {DB_PATH}")


if __name__ == "__main__":
    main()
