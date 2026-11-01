# Global Fuel Prices & Taxation Explorer

An end-to-end student project analyzing the supplied weekly global fuel dataset with Tableau Public, SQLite, SQL, and Flask.

## Dataset

- 27,468 complete weekly records, 84 countries, and 7 regions
- Coverage: 2020-01-06 through 2026-04-06 (the source data does not extend to the end of 2026)
- 10 source fields: date, country, region, income level, subsidy level, petrol/diesel/LPG USD per litre, Brent crude USD, and tax percentage
- The source CSV contains no blank cells. The date values are day-month-year and are normalized to ISO date in SQLite.
- The dataset is descriptive. It is not population-weighted and does not prove that taxes/subsidies caused price changes.

## Run locally

1. Install Python 3.10+.
2. In this folder run `python -m venv .venv`.
3. Activate it (`.venv\\Scripts\\Activate.ps1` on Windows), then run `pip install -r requirements.txt`.
4. Import/refresh the SQLite database with `python setup_database.py`.
5. Start the site with `python app.py` and open http://127.0.0.1:5000.

The included `fuel_prices.db` is already populated. The web app has region, country, income, subsidy, date-range, and fuel-series controls. Reset restores all records.

## Project files

- `data/global_fuel_prices_Dataset.csv` — project copy of the source data
- `fuel_prices.db`, `setup_database.py` — SQLite database and repeatable import
- `sql/analysis_queries.sql` — validation and policy comparison queries
- `Fuel_Atlas_Final.twbx` — final Tableau Public workbook with a dashboard and four Tableau story points
- `app.py`, `templates/index.html` — responsive Flask dashboard and five-scene interactive policy story

## Analysis and visuals

The Flask dashboard presents five KPIs and four analytical views: monthly regional fuel trend, regional fuel/tax comparison, subsidy group comparison, and country price leaders. The five story scenes cover market context, regional patterns, tax policy, subsidies, and policy takeaway. Filters support regional/country, income/subsidy, and date comparisons. Tableau sheets are retained in the packaged workbook; the workbook also includes a local Dashboard 1 built around the petrol trend.

## Tableau workflow

Open `Fuel_Atlas_Final.twbx` in Tableau Public. The packaged workbook has an embedded extract, so it can be inspected offline. The source connection is a CSV extract (the app's analysis store is SQLite); Tableau Public does not directly connect to this local SQLite file. Use the packaged workbook's data source and worksheets for visualization, and use the supplied SQL file to document relational analysis. For an updated extract, use Data > New Data Source > Text File and select the project CSV.

Publishing to Tableau Public makes the workbook and embedded data publicly viewable. Publish only if that is acceptable. The project currently has no public Tableau URL. The local Flask app and its five-scene story work without publishing.

## Scope and limitations

The Tableau workbook contains 2 distinct analytical worksheets (regional petrol trend and regional tax comparison), 1 dashboard containing both charts, and a Tableau Story with 4 points. It has 0 custom Tableau calculated fields; averages and grouped measures are computed in SQL. The Flask dashboard contains 4 analytical views: regional monthly line, regional comparison bars, subsidy comparison bars, and a country ranking table. It includes 5 interactive story scenes. A Tableau Public URL is not embedded because no confirmed published workbook URL is available. The video walkthrough script is in `VIDEO_SCRIPT.md`; an actual recording still needs to be made. The supplied data ends in April 2026, despite the broad project brief mentioning 2026.


## Publish online with GitHub and Render

1. Create a GitHub repository named `fuel-atlas-global-fuel-prices` and push this project.
2. In Render, choose **New > Blueprint**, connect that GitHub repository, and deploy the included `render.yaml`.
3. Render installs dependencies and rebuilds the SQLite database from `data/global_fuel_prices_Dataset.csv`. The Flask app binds to Render's assigned port.

This configuration hosts the Flask dashboard/story. It does not publish the workbook to Tableau Public.
