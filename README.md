# 📅 Task 6: Sales Trend Analysis Using Aggregations
**Tool: SQLite | Dataset: Online Sales (orders + products tables)**

## 📌 Objective
Analyze monthly revenue and order volume trends using SQL aggregations — demonstrating GROUP BY time periods, SUM for revenue, COUNT DISTINCT for volume, and ORDER BY for ranking.

## 🛠️ Tools Used
- **SQLite** — run free at https://sqliteonline.com
- **Python** — to generate the database and screenshots
- **Dataset** — Online Sales: 1,930 orders across 2022–2023, 15 products, 5 regions

## 📂 Project Structure
```
task6-sales-trend-sql/
├── online_sales.db               ← SQLite database
├── sales_trend_analysis.sql      ← All 12 SQL queries (main deliverable)
├── create_and_generate.py        ← Script to recreate DB + screenshots
├── screenshots/
│   ├── 01_monthly_revenue_table.png
│   ├── 02_monthly_trend_chart.png
│   ├── 03_top3_months.png
│   ├── 04_revenue_by_region.png
│   ├── 05_revenue_by_region.png
│   ├── 06_category_revenue.png
│   ├── 07_count_demo.png
│   ├── 08_yoy_comparison.png
│   ├── 09_h1_2023.png
│   └── 10_null_check.png
└── README.md
```

## 🗄️ Database Schema
```sql
products (product_id, product_name, category, unit_price)
orders   (order_id, customer_id, product_id, order_date, quantity, amount, region)
```
- 15 products across 5 categories
- 1,930 orders spanning Jan 2022 – Dec 2023
- 5 regions: North, South, East, West, Central

## 📊 SQL Queries Covered

| # | Query | Concept |
|---|-------|---------|
| Q1 | Monthly revenue + order volume | GROUP BY year/month, SUM, COUNT DISTINCT |
| Q2 | Top 3 months by sales | ORDER BY + LIMIT |
| Q3 | 2022 monthly breakdown | WHERE date range + GROUP BY |
| Q4 | 2023 monthly breakdown | WHERE date range + GROUP BY |
| Q5 | Year-over-year comparison | GROUP BY year, multiple aggregates |
| Q6 | COUNT(*) vs COUNT(DISTINCT) | Understanding counting differences |
| Q7 | Revenue by region | GROUP BY + ORDER BY |
| Q8 | Revenue by category | JOIN + GROUP BY |
| Q9 | Quarterly revenue | CASE WHEN for quarter logic |
| Q10 | NULL handling in aggregates | COALESCE + CASE WHEN |
| Q11 | Running total (YTD) | Window function SUM OVER |
| Q12 | Best and worst month | Subquery + ORDER BY |

## 💡 Key Business Insights
1. **Q4 consistently peaks** — October–December = highest revenue months (holiday effect)
2. **2023 revenue grew 12%** year-over-year vs 2022
3. **Electronics drives 40%** of total revenue despite being one of 5 categories
4. **All 5 regions perform comparably** — no single region dominates significantly
5. **Average order value stable** at ~$280 across both years

## 🚀 How to Run
**Online (No install):**
1. Go to https://sqliteonline.com
2. Upload `online_sales.db`
3. Paste queries from `sales_trend_analysis.sql`

**Recreate locally:**
```bash
python3 create_and_generate.py
```

## ❓ Interview Q&A

**Q: How do you group data by month and year?**
> In SQLite: `GROUP BY STRFTIME('%Y', date_col), STRFTIME('%m', date_col)`. In MySQL/PostgreSQL: `GROUP BY YEAR(date_col), MONTH(date_col)` or `GROUP BY EXTRACT(YEAR FROM date_col), EXTRACT(MONTH FROM date_col)`.

**Q: COUNT(*) vs COUNT(DISTINCT col)?**
> COUNT(*) counts every row including duplicates and NULLs. COUNT(col) counts non-NULL values. COUNT(DISTINCT col) counts unique non-NULL values only. Example: 1,930 rows but only 500 unique customers.

**Q: How to calculate monthly revenue?**
> `SELECT STRFTIME('%Y-%m', order_date) AS month, ROUND(SUM(amount), 2) AS revenue FROM orders GROUP BY month ORDER BY month;`

**Q: What are aggregate functions?**
> Functions that compute a single result from multiple input rows: SUM (total), AVG (mean), COUNT (frequency), MAX/MIN (extremes). Always used with GROUP BY when breaking down by category or time period.

**Q: How to handle NULLs in aggregates?**
> Aggregate functions (SUM, AVG, COUNT) automatically ignore NULL values. To treat NULLs as zero, use `SUM(COALESCE(col, 0))`. To detect NULLs: `SUM(CASE WHEN col IS NULL THEN 1 ELSE 0 END)`.

**Q: Role of ORDER BY and GROUP BY?**
> GROUP BY collapses rows with the same value into one group for aggregation. ORDER BY sorts the final result set. ORDER BY runs AFTER GROUP BY. They work together: group first, then sort the grouped result.

**Q: Top 3 months by sales?**
> `SELECT STRFTIME('%Y',order_date) AS year, STRFTIME('%m',order_date) AS month, ROUND(SUM(amount),2) AS revenue FROM orders GROUP BY year, month ORDER BY revenue DESC LIMIT 3;`
