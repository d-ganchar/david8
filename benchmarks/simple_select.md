SELECT
    order_type,
    seller_type,
    COUNT(order_type) AS order_type_count,
    SUM(total) AS total_spent,
    MAX(created_at) AS last_order,
    MIN(created_at) AS first_order
FROM orders
WHERE order_type != 'canceled'
  AND seller_type != 'unknown'
GROUP BY order_type, seller_type
ORDER BY total_spent DESC, order_type_count DESC
LIMIT 100;
