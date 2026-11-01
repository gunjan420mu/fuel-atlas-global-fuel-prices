"""Flask application for the Global Fuel Prices project."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("FUEL_DB_PATH", BASE_DIR / "fuel_prices.db"))
app = Flask(__name__)


def db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def read_filters():
    clauses = ["date BETWEEN ? AND ?"]
    params: list[object] = [request.args.get("start", "1900-01-01"), request.args.get("end", "2999-12-31")]
    for key, column in (("region", "region"), ("country", "country"), ("income", "income_level"), ("subsidy", "subsidy_level")):
        value = request.args.get(key, "All")
        if value and value != "All":
            clauses.append(f"{column} = ?")
            params.append(value)
    return " AND ".join(clauses), params


@app.route("/")
def home():
    with db_connection() as db:
        record = db.execute("SELECT COUNT(*) AS rows, MIN(date) AS first_date, MAX(date) AS last_date, COUNT(DISTINCT country) AS countries, COUNT(DISTINCT region) AS regions FROM fuel_prices").fetchone()
        regions = [row[0] for row in db.execute("SELECT DISTINCT region FROM fuel_prices ORDER BY region")]
        countries = [row[0] for row in db.execute("SELECT DISTINCT country FROM fuel_prices ORDER BY country")]
        incomes = [row[0] for row in db.execute("SELECT DISTINCT income_level FROM fuel_prices ORDER BY income_level")]
        subsidies = [row[0] for row in db.execute("SELECT DISTINCT subsidy_level FROM fuel_prices ORDER BY subsidy_level")]
    return render_template("index.html", meta=dict(record), regions=regions, countries=countries, incomes=incomes, subsidies=subsidies)


@app.get("/api/overview")
def overview():
    where, params = read_filters()
    with db_connection() as db:
        kpis = db.execute(f"""SELECT COUNT(*) AS rows, COUNT(DISTINCT country) AS countries,
            ROUND(AVG(petrol_usd_liter), 3) AS petrol, ROUND(AVG(diesel_usd_liter), 3) AS diesel,
            ROUND(AVG(lpg_usd_liter), 3) AS lpg, ROUND(AVG(tax_percentage), 2) AS tax
            FROM fuel_prices WHERE {where}""", params).fetchone()
        trend = db.execute(f"""SELECT substr(date,1,7) AS month, region,
            AVG(petrol_usd_liter) AS petrol, AVG(diesel_usd_liter) AS diesel,
            AVG(lpg_usd_liter) AS lpg, AVG(brent_crude_usd) AS crude
            FROM fuel_prices WHERE {where} GROUP BY month, region ORDER BY month, region""", params).fetchall()
        regions = db.execute(f"""SELECT region, ROUND(AVG(petrol_usd_liter),3) AS petrol,
            ROUND(AVG(diesel_usd_liter),3) AS diesel, ROUND(AVG(lpg_usd_liter),3) AS lpg,
            ROUND(AVG(tax_percentage),2) AS tax, COUNT(DISTINCT country) AS countries
            FROM fuel_prices WHERE {where} GROUP BY region ORDER BY petrol DESC""", params).fetchall()
        countries = db.execute(f"""SELECT country, region, ROUND(AVG(petrol_usd_liter),3) AS petrol,
            ROUND(AVG(diesel_usd_liter),3) AS diesel, ROUND(AVG(lpg_usd_liter),3) AS lpg,
            ROUND(AVG(tax_percentage),2) AS tax FROM fuel_prices WHERE {where}
            GROUP BY country, region ORDER BY petrol DESC LIMIT 12""", params).fetchall()
        subsidy = db.execute(f"""SELECT subsidy_level, ROUND(AVG(petrol_usd_liter),3) AS petrol,
            ROUND(AVG(diesel_usd_liter),3) AS diesel, ROUND(AVG(tax_percentage),2) AS tax,
            COUNT(DISTINCT country) AS countries FROM fuel_prices WHERE {where}
            GROUP BY subsidy_level ORDER BY subsidy_level""", params).fetchall()
    return jsonify({"kpis": dict(kpis), "trend": [dict(x) for x in trend], "regions": [dict(x) for x in regions], "countries": [dict(x) for x in countries], "subsidy": [dict(x) for x in subsidy]})


@app.get("/health")
def health():
    with db_connection() as db:
        count = db.execute("SELECT COUNT(*) FROM fuel_prices").fetchone()[0]
    return jsonify({"status": "ok", "rows": count})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
