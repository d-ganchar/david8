"""
Benchmarks SQL query:

SELECT
    p.product_name AS pn,
    c.country AS cy,
    s.shipper_name AS sn,
    SUM(o.order_quantity) AS tqs,
    MIN(o.order_date) AS eod,
    MAX(o.order_date) AS lod
FROM
    products AS p
INNER JOIN
    orders AS o ON p.product_id = o.product_id
LEFT JOIN
    customers AS c ON o.customer_id = c.customer_id
RIGHT JOIN
    shippers AS s ON o.shipper_id = s.shipper_id
WHERE
    p.category = 'Beverages'
GROUP BY
    p.product_name, c.country, s.shipper_name
ORDER BY
    tqs DESC, pn;
"""
from typing import Callable


def run_david8():
    from .select_david8 import generate_sql
    generate_sql()

def run_sqlalchemy():
    from .select_sqlalchemy import generate_sql
    generate_sql()

def run_pypika():
    from .select_pypika import generate_sql
    generate_sql()


ROUNDS = 20
ITERATIONS = 1000

def run_benchmark(benchmark, fn: Callable):
    benchmark.pedantic(
        lambda: fn(),
        rounds=20,
        iterations=1000,
    )

def test_david8(benchmark):
    run_benchmark(benchmark, run_david8)


def test_sqlalchemy(benchmark):
    run_benchmark(benchmark, run_sqlalchemy)

def test_pypika(benchmark):
    run_benchmark(benchmark, run_pypika)
