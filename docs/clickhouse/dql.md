### WITH expression

```python
from david8.expressions import col as c
from david8.expressions import interval
from david8.expressions import val as v
from david8.functions import sub
from david8.predicates import between, eq_c

from david8_clickhouse.functions import to_date

(
    qb
    .with_expr(
        v('2026-06-01 15:23:00').as_('ts_upper_bound'),
        to_date('ts_upper_bound').as_('event_date'),
        sub('ts_upper_bound', interval().hour(1)).as_('ts_lower_bound'),
    )
    .select('*')
    .from_table('hits')
    .where(
        eq_c('EventDate', 'event_date'),
        between('EventTime', c('ts_lower_bound'), c('ts_upper_bound'))
    )
).get_sql()
# WITH '2026-06-01 15:23:00' AS ts_upper_bound,
#      toDate(ts_upper_bound) AS event_date,
#     (ts_upper_bound - INTERVAL 1 HOUR) AS ts_lower_bound
#   SELECT * FROM hits
#    WHERE EventDate = event_date AND
#  EventTime BETWEEN ts_lower_bound AND ts_upper_bound

```

### ARRAY JOIN

```python
from david8.expressions import col, val
from david8_clickhouse import get_qb
from david8_clickhouse.joins import array_join, left_array_join

query = (
    qb
    .select('column', 'array_column')
    .from_table('table_name')
    .join(array_join('array_column'))
)
# SELECT column, array_column FROM table_name ARRAY JOIN array_column
```

### LEFT ARRAY JOIN

```python
query = (
    qb
    .select('column', 'array_column', 'array_column2')
    .from_table('table_name')
    .join(left_array_join(
        col('array_column').as_('alias1'),
        col('array_column2').as_('alias2'))
    )
)
# SELECT column, array_column, array_column2 FROM table_name
# LEFT ARRAY JOIN array_column AS alias1, array_column2 AS alias2
```

### FINAL

```python
qb.select('name').from_table('events', final=True)  # SELECT name FROM events FINAL
```

### SAMPLE

```python
qb.select('*').from_table('visits').sample(10000000) # SELECT * FROM visits SAMPLE 10000000
qb.select('*').from_table('visits').sample(0.1, 0.5) # SELECT * FROM visits SAMPLE 0.1 OFFSET 0.5
```

### LIMIT BY

```python
qb.select('*').from_table('tbl').limit_by()
# SELECT * FROM tbl LIMIT BY ALL

qb.select('*').from_table('tbl').limit_by('col1', limit=10, offset=50).limit(100)
# SELECT * FROM tbl LIMIT 10, 50 BY col1 LIMIT 100
```
