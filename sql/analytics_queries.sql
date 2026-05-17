-- Revenue trend analysis
SELECT DATE_FORMAT(purchase_date, '%Y-%m') AS month, SUM(revenue) AS monthly_revenue
FROM transactions_processed
GROUP BY DATE_FORMAT(purchase_date, '%Y-%m')
ORDER BY month;

-- Product category performance
SELECT product_category, SUM(revenue) AS category_revenue, COUNT(*) AS transactions
FROM transactions_processed
GROUP BY product_category
ORDER BY category_revenue DESC;

-- Repeat customer analysis
SELECT
    SUM(CASE WHEN transaction_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    COUNT(*) AS total_customers
FROM (
    SELECT customer_id, COUNT(*) AS transaction_count
    FROM transactions_processed
    GROUP BY customer_id
) c;
