WITH order_features AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT sale_id) AS frequency,
        SUM(quantity * unit_price) AS monetary,
        DATEDIFF(DAY, MAX(sale_date), GETDATE()) AS recency_days,
        DATEDIFF(DAY, MIN(sale_date), GETDATE()) AS tenure_days
    FROM fact_sales
    GROUP BY customer_id
)
SELECT * INTO customer_features FROM order_features;