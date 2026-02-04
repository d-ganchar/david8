"""
Benchmarks SQL query:

WITH base_data AS (
    SELECT user_id,
           event_type,
           event_day,
           amount
      FROM events
     WHERE event_day BETWEEN '2023-01-01' AND '2025-01-01'
     UNION ALL
    SELECT user_id,
           event_type,
           event_day,
           amount
      FROM events_v2
     WHERE event_day BETWEEN %(p1)s AND %(p2)s
)
SELECT bd.user_id,
       bd.event_type,
       m.category,
       COUNT(*)          AS cnt_events,
       SUM(bd.amount)    AS sum_amount,
       MIN(bd.amount)    AS min_amount,
       MAX(bd.amount)    AS max_amount,
       MIN(bd.event_day) AS first_event_day,
       MAX(bd.event_day) AS last_event_day
  FROM base_data bd
  LEFT JOIN event_metadata m USING (user_id, event_type)
 GROUP BY bd.user_id,
          bd.event_type,
          m.category
 ORDER BY bd.event_type DESC,
          bd.user_id
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
