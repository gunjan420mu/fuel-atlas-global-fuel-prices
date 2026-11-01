# Project demonstration video script (5–7 minutes)

## 1. Opening (30 sec)
“Hello, this project explores global petrol, diesel and LPG prices alongside crude benchmarks, taxes and subsidy categories. It uses 27,468 weekly records from 84 countries across seven regions, from January 2020 to April 2026.”

## 2. Problem and dataset (45 sec)
“Policy analysts need to compare how pump prices and tax structures vary by country and region. The source CSV contains ten fields and has no blank cells. I normalized its day-month-year dates and loaded the rows into SQLite. These comparisons are descriptive and do not establish causation.” Show the CSV preview and project folder.

## 3. Database and SQL (45 sec)
“Here is the SQLite import script and database. The SQL file checks row coverage and calculates monthly regional averages, regional tax summaries, and comparisons by income and subsidy group.” Show `setup_database.py`, `fuel_prices.db`, and `sql/analysis_queries.sql`.

## 4. Tableau workbook (60 sec)
“Tableau Public reads the packaged data extract. The workbook includes worksheets for the regional petrol trend and average regional tax, along with a dashboard view. The date and region dimensions support comparison. This local workbook has not been published to Tableau Public.” Open `Global_Fuel_Prices_Updated.twbx`; show Data Source, worksheets, and Dashboard 1. If your saved copy has changed, describe only what is visible.

## 5. Flask dashboard demo (90 sec)
“Now I’ll open the Flask dashboard. The KPI cards summarize the selected records. I can filter region, country, income level, subsidy level and date range, then compare petrol, diesel, LPG or Brent crude. The charts show the monthly trend, regional prices and tax, subsidy group averages and country leaders. Reset returns to the complete dataset.” Demonstrate changing a region/date and then Reset.

## 6. Interactive story (45 sec)
“The five policy scenes guide the reader from market context through regional patterns, taxation, subsidy categories and a final policy takeaway. Each scene is grounded in the charts and includes a caution about interpretation.” Click through all five scenes.

## 7. Performance and close (30 sec)
“Local checks returned the main page and health endpoint successfully. The full overview query returned in about 98 milliseconds and a filtered query in about 10 milliseconds on this machine; these are single-run local timings, not a formal load test. The project can be rerun from the README. Thank you.”

## Recording checklist

- Start the local Flask site before recording (`python app.py`).
- Capture Tableau workbook, CSV/SQLite/SQL, dashboard filters, Reset, and all five story scenes.
- Avoid showing account credentials or unrelated browser tabs.
- Save the video file in this project folder and update this README if its filename needs to be listed.
