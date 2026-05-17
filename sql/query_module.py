"""Reusable SQL query module for analytics dashboards."""

TOP_CUSTOMERS_QUERY = """
SELECT customer_id, SUM(revenue) AS total_revenue
FROM transactions_processed
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 10;
"""

MONTHLY_REVENUE_QUERY = """
SELECT DATE_FORMAT(purchase_date, '%Y-%m') AS month, SUM(revenue) AS monthly_revenue
FROM transactions_processed
GROUP BY DATE_FORMAT(purchase_date, '%Y-%m')
ORDER BY month;
"""

RETENTION_QUERY = """
SELECT customer_id, COUNT(*) AS transaction_count
FROM transactions_processed
GROUP BY customer_id;
"""
