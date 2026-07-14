### Functions

See available [functions](https://github.com/d-ganchar/david8_clickhouse/blob/main/david8_clickhouse/functions.py). Tests and use cases:  [test_functions](https://github.com/d-ganchar/david8_clickhouse/blob/main/tests/test_functions.py), [test_table_functions.py](https://github.com/d-ganchar/david8_clickhouse/blob/main/tests/test_table_functions.py)

example:

```python
from david8.expressions import interval
from david8.expressions import val as v
from david8.functions import now_, sub
from david8.predicates import eq
from david8.predicates import eq_c

from david8_clickhouse import get_qb
from david8_clickhouse.cast_types import string, uint8
from david8_clickhouse.functions import iceberg_s3, postgresql, prometheus_query_range, redis_
from david8_clickhouse.functions import multi_if, dict_get, yyyymmdd_to_date, parse_datetime_best_effort
from david8_clickhouse.functions_table import s3, url_
from david8_clickhouse.input_output_formats import CSV

qb = get_qb()
(
    qb
    .select(
        multi_if(
            (eq('status', 'unknown'), 'new_status'),
            (eq('status', 'old_status'), v('legacy')),
            else_='status',
        ).as_('fixed_status'),
        dict_get('dicts.currencies', 'full_name', 'currency_char').as_('currency'),
        yyyymmdd_to_date(20260101).as_('date'),
        parse_datetime_best_effort(v('2026-01-01')).as_('date')
    )
).get_sql()
# SELECT multiIf(status = %(p1)s, new_status, status = %(p2)s, 'legacy', status) AS fixed_status,
#        dictGet('dicts.currencies', 'full_name', currency_char) AS currency,
#        YYYYMMDDToDate(20260101) AS date,
#        parseDateTimeBestEffort('2026-01-01') AS date
# {'p1': 'unknown', 'p2': 'old_status'}
```

## Table functions

```python
qb.select('*').from_expr(
    url_(
        'http://data/path/date=*/country=*/code=*/*.parquet',
        CSV,
        [
            ('name', string),
            ('price', uint8),
        ],
        {
            'Accept': 'text/csv; charset=utf-8',
            'Accept-Language': 'en-US,en;',
        }
    )
).get_sql()
# SELECT * FROM url(
#  'http://data/path/date=*/country=*/code=*/*.parquet',
#  'CSV',
#  'name String, price UInt8',
#  headers=('Accept'='text/csv; charset=utf-8', 'Accept-Language'='en-US,en;'
#  ))

(
    qb
    .insert()
    .into_table_fn(url_('http://data/path/date=*/country=*/code=*/*.parquet'))
    .from_select(qb.select('*').from_table('t'))
).get_sql()
# INSERT INTO FUNCTION url('http://data/path/date=*/country=*/code=*/*.parquet') SELECT * FROM t

qb.select('*').from_expr(s3(
    'https://public-datasets.com/test.csv',
    'creds',
    data_format=CSV,
    structure=[
        ('name', string),
        ('price', uint8),
    ],
    compression_method='gzip',
)).get_sql()
# SELECT * FROM s3(
#      creds,
#      url='https://public-datasets.com/test.csv',
#      format='CSV',
#      structure='name String, price UInt8',
#      compression_method='gzip'
# )

qb.select('*').from_expr(iceberg_s3(creds='creds', compression_method='gzip', filename='test_table')).get_sql()
# SELECT * FROM icebergS3(creds, filename='test_table', compression_method='gzip')

(
    qb
    .select('*')
    .from_expr(postgresql(
        creds='mypg',
        table=qb.select('*').from_table('tbl1').where(eq_c('col1', 'col2')))
    )
).get_sql()
# SELECT * FROM postgresql(mypg, table=(SELECT * FROM tbl1 WHERE col1 = col2))

(
    qb.insert().into_table_fn(redis_(
        'redis1:6379',
        'metrics',
        [
            ('name', string),
            ('value', uint8),
        ],
    ))
    .from_select(qb.select('name', 'value').from_table('t'))
).get_sql()
# INSERT INTO FUNCTION redis('redis1:6379', 'metrics', 'name String, value UInt8') SELECT name, value FROM t

(
    qb
    .select('*')
    .from_expr(prometheus_query_range(
        'table',
        'rate(http_requests{job="prometheus"}[10m])[1h:10m]',
        sub(now_(), interval().minute(10)),
        now_(),
        interval().minute(1),
        'db'
    ))
).get_sql()
# SELECT * FROM prometheusQueryRange(
# 'db',
# 'table',
# 'rate(http_requests{job="prometheus"}[10m])[1h:10m]',
# (now() - INTERVAL 10 MINUTE),
# now(),
# INTERVAL 1 MINUTE)
```
