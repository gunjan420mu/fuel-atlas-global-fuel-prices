-- Global Fuel Prices: reusable SQL analysis queries (SQLite)

-- 1. Validate volume, coverage, and missing data.
SELECT COUNT(*) AS row_count,
       COUNT(DISTINCT country) AS countries,
       COUNT(DISTINCT region) AS regions,
       MIN(date) AS first_date, MAX(date) AS last_date
FROM fuel_prices;

-- 2. Monthly mean fuel prices, grouped by region.
SELECT substr(date, 1, 7) AS month, region,
       ROUND(AVG(petrol_usd_liter), 3) AS petrol_usd_liter,
       ROUND(AVG(diesel_usd_liter), 3) AS diesel_usd_liter,
       ROUND(AVG(lpg_usd_liter), 3) AS lpg_usd_liter
FROM fuel_prices
GROUP BY month, region
ORDER BY month, region;

-- 3. Compare average tax and prices by region.
SELECT region, ROUND(AVG(tax_percentage), 2) AS avg_tax_pct,
       ROUND(AVG(petrol_usd_liter), 3) AS avg_petrol_usd_liter,
       ROUND(AVG(diesel_usd_liter), 3) AS avg_diesel_usd_liter,
       COUNT(DISTINCT country) AS countries
FROM fuel_prices
GROUP BY region
ORDER BY avg_tax_pct DESC;

-- 4. Compare fuel prices by income and subsidy group.
SELECT income_level, subsidy_level,
       ROUND(AVG(petrol_usd_liter), 3) AS avg_petrol,
       ROUND(AVG(diesel_usd_liter), 3) AS avg_diesel,
       ROUND(AVG(tax_percentage), 2) AS avg_tax_pct,
       COUNT(DISTINCT country) AS countries
FROM fuel_prices
GROUP BY income_level, subsidy_level
ORDER BY income_level, subsidy_level;

-- 5. Highest average petrol price by country.
SELECT country, region, ROUND(AVG(petrol_usd_liter), 3) AS avg_petrol
FROM fuel_prices
GROUP BY country, region
ORDER BY avg_petrol DESC
LIMIT 10;
