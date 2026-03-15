
-- Customer Revenue Analysis SQL Queries

-- Total Revenue
SELECT SUM(revenue) AS total_revenue
FROM sales;

-- Revenue by Region
SELECT region, SUM(revenue) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- Top 10 Customers
SELECT customer_name, SUM(revenue) AS total_spent
FROM sales
GROUP BY customer_name
ORDER BY total_spent DESC
LIMIT 10;

-- Revenue by Category
SELECT category, SUM(revenue) AS revenue
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- Monthly Revenue Trend
SELECT
DATE_TRUNC('month', order_date) AS month,
SUM(revenue) AS revenue
FROM sales
GROUP BY month
ORDER BY month;
