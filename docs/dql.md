## SELECT

By default, the method uses string `args` as column names:

```python
query1 = qb.select('col1', 'col2').from_table('table1', 'alias', 'db2')
query2 = qb.select('*').from_expr(query1)
query1.get_sql()
query2.get_sql()
# SELECT col1, col2 FROM db2.table1 AS alias
# SELECT * FROM (SELECT col1, col2 FROM db2.table1 AS alias)

data = {
    'name': True,
    'last_name': True,
    'age': None,
    'nationality': None,
}

query = qb.select().from_table('users')
for col, flag in data.items():
    if flag:
        query.select(col)

query.get_sql()
# SELECT name, last_name FROM users
```

Use `val()`, `col()` and `param()` from [expressions.py](https://github.com/d-ganchar/david8/blob/main/david8/expressions.py) module to put specific expressions into a query. Example:

```python
from david8.expressions import val as v, param as p, col as c

qb.select(
    v('static-text').as_('alias1'),
    p('one').as_('alias2'),
    c('col1').as_('alias3'),
    p(0.5),
    p(1),
).get_sql()
# [INFO]: SELECT 'static-text' AS alias1, %(p1)s AS alias2, col1 AS alias3, %(p2)s, %(p3)s
# {'p1': 'one', 'p2': 0.5, 'p3': 1}
```

## DISTINCT

```python
from david8.functions import lower
from david8.expressions import distinct as d

qb.select(d('customer_id', lower('amount'), 'created_at'))
# SELECT DISTINCT customer_id, lower(amount), created_at

qb.select(d('customer_id', lower('amount'), 'created_at', on=['customer_id']))
# SELECT DISTINCT ON (customer_id) customer_id, lower(amount), created_at

qb.select(d('*', on=[lower('customer_id'), 'customer_id']))
# SELECT DISTINCT ON (lower(customer_id), customer_id) *
```

## LIMIT, OFFSET

```python
qb.select('*').from_table('events').limit(100).offset(100)
# SELECT * FROM events LIMIT 100 OFFSET 100
```

## UNION

```python
(
    qb
    .select('col1').from_table('table1')
    .union(
       qb.select('col2').from_table('table2'),
       qb.select('col3').from_table('table3'),
    )
    .union(
       qb.select('col4').from_table('table4'),
       qb.select('col5').from_table('table5'),
       all_flag=False,
    )
).get_sql()
# SELECT col1 FROM table1
# UNION ALL SELECT col2 FROM table2
# UNION ALL SELECT col3 FROM table3 
# UNION SELECT col4 FROM table4
# UNION SELECT col5 FROM table5
```

## WITH

```python
(
    qb
    .with_(
        ('alias1', qb.select(col('col1').as_('fixed')).from_table('table1')),
        ('alias2', qb.select(col('col2').as_('fixed')).from_table('table2')),
        # ...
    )
    .select('*').from_table('alias1')
    .union(qb.select('*').from_table('alias2'))
).get_sql()
# WITH alias1 AS (SELECT col1 AS fixed FROM table1),
#      alias2 AS (SELECT col2 AS fixed FROM table2) 
#  SELECT * FROM alias1 UNION ALL SELECT * FROM alias2
# {}
```

## JOIN

Use `joins` from [joins.py](https://github.com/d-ganchar/david8/blob/main/david8/joins.py) module to join tables:

```python
from david8.joins import left, right, inner, lateral
from david8.predicates import eq_c, lt_c
# inner
(
    qb
    .select('*')
    .from_table('order_contacts', alias='oc')
    .join(inner().table('order_details').as_('od').using('order_id', 'user_id'))
).get_sql()
# SELECT * FROM order_contacts AS oc
# INNER JOIN order_details AS od USING (order_id, user_id)

# left + right
(
    qb
    .select('*')
    .from_table('table1', alias='t1')
    .join(left().table('table2').as_('t2').on(
        eq_c('t1.col1', 't2.col1'),
        eq_c('t1.col2', 't2.col2'))
    )
    .join(right().table('table3').as_('t3').on(
        eq_c('t1.col1', 't3.col3'),
        eq_c('t1.col2', 't3.col3'))
    )
).get_sql()
# SELECT * FROM table1 AS t1
# LEFT JOIN table2 AS t2 ON (t1.col1 = t2.col1 AND t1.col2 = t2.col2)
# RIGHT JOIN table3 AS t3 ON (t1.col1 = t3.col3 AND t1.col2 = t3.col3)

# lateral
(
    qb.select('*')
    .from_table('customers', alias='c')
    .join(
        lateral()
        .expression(
            qb
           .select('store_id', 'distance')
           .from_table('stores', alias='s')
        )
        .as_('nearby')
        .on(lt_c('nearby.distance', 'c.max_km'))
    )
)
# SELECT * FROM customers AS c 
# INNER JOIN LATERAL (
#      SELECT store_id, distance
#        FROM stores AS s
# ) AS nearby ON (nearby.distance < c.max_km)

# join query example
(
    qb
    .select('*')
    .from_table('users', 'u')
    .join(
        left()
        .query(qb.select('*').from_table('orders'))
        .on(eq_c('o.user_id', 'u.id'))
        .as_('o')
    )
).get_sql()
# SELECT * FROM users AS u
# LEFT JOIN (SELECT * FROM orders) AS o ON (o.user_id = u.id)
```

multiple `joins` as a positional argument:
```python
from david8.expressions import col as c
from david8.expressions import desc as d
from david8.expressions import val as v
from david8.joins import asof, asof_left, inner, lateral, left, right
from david8.predicates import between, eq, eq_c, ge_c, gt, le_c

query = (
    qb
    .select('*')
    .from_table('orders', alias='o')
    .join(
        inner().table('customers').as_('c').on(eq_c('o.user_id', 'c.user_id')),
        left().table('shipping').as_('s').on(eq_c('o.order_id', 's.order_id')),
        right().table('discounts').as_('d').on(
            eq_c('o.product_id', 'd.product_id'),
            between('o.order_ts', c('d.valid_from'), c('d.valid_to'))
        ),
        asof().table('prices').as_('pr').on(
            eq_c('o.product_id', 'pr.product_id'),
            ge_c('o.order_ts', 'pr.price_ts')
        ),
        asof_left().table('order_status_history').as_('hist').on(
            eq_c('o.order_id', 'hist.order_id'),
            ge_c('o.order_ts', 'hist.status_ts')
        ),
        lateral().expression(
            qb.select('note', 'distance')
            .from_table('manager_notes', alias='mn')
            .where(
                eq_c('mn.user_id', 'c.user_id'),
                le_c('mn.note_ts', 'o.order_ts')
            )
            .order_by(d('mn.note_ts'))
            .limit(1)
        ).on(eq(v(1), v(1)))
    )
    .where(gt('o.order_ts', 1767225661))
    .order_by('o.order_id')
)
# SELECT * FROM orders AS o
# INNER JOIN customers AS c ON (o.user_id = c.user_id)
# LEFT JOIN shipping AS s ON (o.order_id = s.order_id)
# RIGHT JOIN discounts AS d ON (
#       o.product_id = d.product_id AND 
#       o.order_ts BETWEEN d.valid_from AND d.valid_to
# )
# ASOF JOIN prices AS pr ON (
#   o.product_id = pr.product_id AND o.order_ts >= pr.price_ts
# )
# ASOF LEFT JOIN order_status_history AS hist ON (
#   o.order_id = hist.order_id AND o.order_ts >= hist.status_ts
# )
# INNER JOIN LATERAL (
#       SELECT note, distance
#         FROM manager_notes AS mn
#        WHERE mn.user_id = c.user_id AND mn.note_ts <= o.order_ts
#        ORDER BY mn.note_ts DESC
#        LIMIT 1
# ) AS ON (1 = 1)
# WHERE o.order_ts > %(p1)s
# ORDER BY o.order_id
# {'p1': 1767225661}
```

## WHERE

By default `where()` will process conditions using `AND` operator. You can change behavior using [logical_operators.py](https://github.com/d-ganchar/david8/blob/main/david8/logical_operators.py) module:

```python
from david8.predicates import eq
from david8.logical_operators import xor, or_

(
    qb
    .select('*')
    .from_table('t')
    .where(
        xor(
            eq('col1', 1),
            eq('col1', 2),
            or_(
                eq('col2', 3),
                eq('col2', 4),
            ),
        ),
        eq('col3', 5),
    )
).get_sql()
# SELECT * FROM t WHERE (col1 = %(p1)s XOR col1 = %(p2)s XOR (col2 = %(p3)s OR col2 = %(p4)s)) 
# AND col3 = %(p5)s 
# {'p1': 1, 'p2': 2, 'p3': 3, 'p4': 4, 'p5': 5}


query = qb.select('*').from_table('t')
user_data = {
    'col1': 'val1',
    'col2': None,
    'col3': 65,
}

for col, value in user_data.items():
    if value:
        query.where(eq(col, value))

query.get_sql()
# SELECT * FROM t WHERE col1 = %(p1)s AND col3 = %(p2)s
# {'p1': 'val1', 'p2': 65}
```

## CASE

```python
from david8.expressions import case

qb.select(
    case(
       ('col_name', -1),
       ('col_name2', -2),
       else_=1,
    )
).get_sql()

# SELECT CASE WHEN col_name THEN %(p1)s WHEN col_name2 THEN %(p2)s ELSE %(p3)s END
# {'p1': -1, 'p2': -2, 'p3': 1}
```

See [test_case()](https://github.com/d-ganchar/david8/blob/main/tests/test_expressions.py)

## CAST

```python
from david8.cast_types import integer
from david8.functions import cast

qb.select(cast('col_name', integer)).get_sql()  # SELECT CAST(col_name AS INTEGER)
```

## INTERVAL

```python
from david8.expressions import interval

qb.select(
   interval().year(2020),
   interval()
      .year(2026)
      .quarter(2)
      .month(3)
      .week(4)
      .day(5)
      .hour(6)
      .minute(7)
      .second(8)
      .as_('interval_expr'),
   # interval as string
   interval(False).week(1).as_('week_value')
).get_sql()
# SELECT INTERVAL 2020 YEAR,
#        INTERVAL 2026 YEAR 2 QUARTER 3 MONTH 4 WEEK 5 DAY 6 HOUR 7 MINUTE 8 SECOND AS interval_expr,
#        INTERVAL '1 WEEK' AS week_value
```
