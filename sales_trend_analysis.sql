-- ================================================================
-- TASK 6: SALES TREND ANALYSIS USING AGGREGATIONS
-- Tool: SQLite | Dataset: online_sales (orders + products tables)
-- Covers: EXTRACT/STRFTIME for month, GROUP BY year/month,
--         SUM revenue, COUNT DISTINCT orders, ORDER BY, LIMIT
-- ================================================================

-- ── TABLE OVERVIEW ────────────────────────────────────────────
SELECT name FROM sqlite_master WHERE type='table';

SELECT * FROM products LIMIT 5;
SELECT * FROM orders LIMIT 5;

-- ── Q1: MONTHLY REVENUE & ORDER VOLUME ───────────────────────
-- Use STRFTIME('%m') for month (equivalent to EXTRACT(MONTH) in PostgreSQL/MySQL)
SELECT
    STRFTIME('%Y', order_date)          AS year,
    STRFTIME('%m', order_date)          AS month,
    COUNT(DISTINCT order_id)            AS order_volume,
    ROUND(SUM(amount), 2)               AS monthly_revenue,
    ROUND(AVG(amount), 2)               AS avg_order_value
FROM orders
GROUP BY year, month
ORDER BY year, month;

-- ── Q2: TOP 3 MONTHS BY SALES ────────────────────────────────
SELECT
    STRFTIME('%Y', order_date)          AS year,
    STRFTIME('%m', order_date)          AS month,
    ROUND(SUM(amount), 2)               AS monthly_revenue,
    COUNT(DISTINCT order_id)            AS order_count
FROM orders
GROUP BY year, month
ORDER BY monthly_revenue DESC
LIMIT 3;

-- ── Q3: MONTHLY REVENUE — 2022 ONLY ──────────────────────────
SELECT
    STRFTIME('%m', order_date)          AS month,
    COUNT(DISTINCT order_id)            AS order_volume,
    ROUND(SUM(amount), 2)               AS monthly_revenue
FROM orders
WHERE order_date BETWEEN '2022-01-01' AND '2022-12-31'
GROUP BY month
ORDER BY month;

-- ── Q4: MONTHLY REVENUE — 2023 ONLY ──────────────────────────
SELECT
    STRFTIME('%m', order_date)          AS month,
    COUNT(DISTINCT order_id)            AS order_volume,
    ROUND(SUM(amount), 2)               AS monthly_revenue
FROM orders
WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY month
ORDER BY month;

-- ── Q5: YEAR-OVER-YEAR COMPARISON ────────────────────────────
SELECT
    STRFTIME('%Y', order_date)          AS year,
    COUNT(DISTINCT order_id)            AS total_orders,
    COUNT(DISTINCT customer_id)         AS unique_customers,
    ROUND(SUM(amount), 2)               AS total_revenue,
    ROUND(AVG(amount), 2)               AS avg_order_value
FROM orders
GROUP BY year
ORDER BY year;

-- ── Q6: COUNT(*) vs COUNT(DISTINCT) DEMO ─────────────────────
-- COUNT(*) counts ALL rows including duplicates
-- COUNT(DISTINCT col) counts unique values only
SELECT
    COUNT(*)                            AS count_all_rows,
    COUNT(order_id)                     AS count_non_null_orders,
    COUNT(DISTINCT order_id)            AS distinct_orders,
    COUNT(DISTINCT customer_id)         AS distinct_customers,
    COUNT(DISTINCT product_id)          AS distinct_products
FROM orders;

-- ── Q7: REVENUE BY REGION ─────────────────────────────────────
SELECT
    region,
    COUNT(DISTINCT order_id)            AS total_orders,
    ROUND(SUM(amount), 2)               AS total_revenue,
    ROUND(AVG(amount), 2)               AS avg_order_value
FROM orders
GROUP BY region
ORDER BY total_revenue DESC;

-- ── Q8: REVENUE BY PRODUCT CATEGORY (JOIN) ────────────────────
SELECT
    p.category,
    COUNT(DISTINCT o.order_id)          AS total_orders,
    SUM(o.quantity)                     AS units_sold,
    ROUND(SUM(o.amount), 2)             AS revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;

-- ── Q9: QUARTERLY REVENUE ─────────────────────────────────────
SELECT
    STRFTIME('%Y', order_date)          AS year,
    CASE
        WHEN CAST(STRFTIME('%m', order_date) AS INTEGER) BETWEEN 1 AND 3  THEN 'Q1'
        WHEN CAST(STRFTIME('%m', order_date) AS INTEGER) BETWEEN 4 AND 6  THEN 'Q2'
        WHEN CAST(STRFTIME('%m', order_date) AS INTEGER) BETWEEN 7 AND 9  THEN 'Q3'
        ELSE 'Q4'
    END                                 AS quarter,
    COUNT(DISTINCT order_id)            AS orders,
    ROUND(SUM(amount), 2)               AS quarterly_revenue
FROM orders
GROUP BY year, quarter
ORDER BY year, quarter;

-- ── Q10: NULL HANDLING IN AGGREGATES ─────────────────────────
-- NULL values are ignored by SUM, AVG, COUNT automatically
-- Use COALESCE to replace NULLs with a default before aggregation
SELECT
    SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END)        AS null_amounts,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END)   AS null_customers,
    SUM(COALESCE(amount, 0))                               AS sum_with_coalesce,
    COUNT(*)                                               AS total_rows
FROM orders;

-- ── Q11: REVENUE WITH RUNNING TOTAL ──────────────────────────
SELECT
    STRFTIME('%Y', order_date)          AS year,
    STRFTIME('%m', order_date)          AS month,
    ROUND(SUM(amount), 2)               AS monthly_revenue,
    ROUND(SUM(SUM(amount)) OVER (
        PARTITION BY STRFTIME('%Y', order_date)
        ORDER BY STRFTIME('%m', order_date)), 2) AS running_total_ytd
FROM orders
GROUP BY year, month
ORDER BY year, month;

-- ── Q12: BEST AND WORST PERFORMING MONTHS ────────────────────
-- Best month
SELECT 'Best Month' AS label,
    STRFTIME('%Y', order_date) AS year,
    STRFTIME('%m', order_date) AS month,
    ROUND(SUM(amount), 2) AS revenue
FROM orders GROUP BY year, month ORDER BY revenue DESC LIMIT 1;

-- Worst month
SELECT 'Worst Month' AS label,
    STRFTIME('%Y', order_date) AS year,
    STRFTIME('%m', order_date) AS month,
    ROUND(SUM(amount), 2) AS revenue
FROM orders GROUP BY year, month ORDER BY revenue ASC LIMIT 1;

-- ================================================================
-- END OF TASK 6 SALES TREND ANALYSIS
-- ================================================================
