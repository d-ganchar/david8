### MERGE INTO

An example of how to update `PostgreSQL` table via `csv` file + `MERGE INTO`

```python
import duckdb
from david8.expressions import param as p
from david8.predicates import eq, ne
from david8.logical_operators import or_, and_
from david8_duckdb import get_qb

con = duckdb.connect()
con.execute('INSTALL postgres')
con.execute('LOAD postgres')
con.execute("""
    ATTACH 'host=127.0.0.1 port=5432 user=david8 password=david8 dbname=david8'
    AS pg
    (TYPE postgres);
""")

query = (qb
    .merge_into('pg.metrics')
    .using(
        qb.select('category_name').from_csv('fixed_data.csv').where(ne('category_name', 'skip')),
        as_='update_metrics',
        columns=['category_name'],
    )
    .update_when_matched(
        or_(eq('name', 'a'), eq('name', 'b')),
        {'score': p(3)}
    )
    .update_when_matched(
        and_(eq('name', 'c')),
        {'score': p(4)}
    )
).get_sql()

# MERGE INTO pg.metrics
# USING (
#   SELECT category_name FROM read_csv('fixed_data.csv') WHERE category_name != ?
# ) AS update_metrics
# USING (category_name)
# WHEN MATCHED AND (name = ? OR name = ?) THEN UPDATE SET score = ?
# WHEN MATCHED AND (name = ?) THEN UPDATE SET score = ?

# ('skip', 'a', 'b', 3, 'c', 4)
```

See [test_dml.py](https://github.com/d-ganchar/david8_duckdb/blob/main/tests/test_dml.py)