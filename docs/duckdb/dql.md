### FILE LOADING

The query builder implements an interface for generation queries over file-based data sources, examples:

```python
qb.select('*').from_csv('flights1.csv', 'flights2.csv')
qb.select('*').from_json('todos1.json', 'todos2.json')
qb.select('*').from_json('todos1.json', 'todos2.json')
qb.select('*').from_json_objects('todos1.json', 'todos2.json')
qb.select('*').from_ndjson_objects('todos1.json', 'todos2.json')
qb.select('*').from_json_objects_auto('todos1.json', 'todos2.json')
qb.select('*').from_parquet('file1.parquet', 'file2.parquet')
qb.select('*').from_xlsx('test.xlsx')
```

See [test_select.py](https://github.com/d-ganchar/david8_duckdb/blob/main/tests/test_select.py)

### PIVOT / UNPIVOT

```python
from david8.functions import sum_

query = (
    qb
    .pivot('cities')
    .on('country', 'name')
    .using(
        sum_('population').as_('total'),
        sum_('population').as_('max'),
    )
    .group_by('country')
    .limit(10)
).get_sql()

# PIVOT cities
# ON country, name
# USING sum(population) AS total, sum(population) AS max
# GROUP BY country
# ORDER BY country
# LIMIT 10

(
    qb
    .unpivot('monthly_sales')
    .on('jan', 'feb', 'mar', 'apr', 'may', 'jun')
    .into('month', 'sales')
    .order_by('sales')
    .limit(10)
).get_sql()

#  UNPIVOT monthly_sales
#  ON jan, feb, mar, apr, may, jun
#  INTO NAME month
#  VALUE sales
#  ORDER BY sales
#  LIMIT 10
```

See [test_dql.py](https://github.com/d-ganchar/david8_duckdb/blob/main/tests/test_dql.py)

### JOINS

[positional](https://duckdb.org/docs/stable/sql/query_syntax/from#positional-joins)

```python
from david8_duckdb.joins import positional

qb.select('*').from_table('table1').join(positional('pos_table')).get_sql()
# SELECT * FROM table1 POSITIONAL JOIN pos_table
```

### EXCLUDE

```python
from david8_duckdb.expressions import exclude as e

qb.select(e('salary', 'ssn')) # SELECT * EXCLUDE (salary, ssn)
```

### REPLACE

```python
from david8.functions import trim
from david8_duckdb.expressions import replace as r

qb.select(r(
    trim('col1').as_('col1'),
    trim('col2').as_('col2'),
))
# SELECT * REPLACE (trim(col1) AS col1, trim(col2) AS col2)
```

### RENAME

```python
from david8_duckdb.expressions import rename as r

qb.select(r(
    ('a', 'b'),
    ('c', 'd'),
))
# SELECT * RENAME (a AS b, c AS d)
```

### COLUMNS

```python
from david8_duckdb.expressions import columns as c
from david8.expressions import val as v
from david8.functions import trim
from david8.predicates import is_null

qb.select(c('*'))                # SELECT COLUMNS(*)
qb.select(c(v('(id|numbers?)'))) # SELECT COLUMNS('(id|numbers?)')
qb.select(trim(c('*')))          # SELECT trim(COLUMNS(*))
qb.select(is_null(c('*')))       # SELECT COLUMNS(*) IS NULL
```
