Use [functions.py](https://github.com/d-ganchar/david8/blob/main/david8/functions.py) module to find core functions, see [test_functions.py](https://github.com/d-ganchar/david8/blob/main/tests/test_functions.py)

```python
from david8.functions import concat
from david8.predicates import eq

query = (
    qb
    .select(concat('col1', '. ', 'col2').as_('fn_result'))
    .from_table('t')
    .where(
        eq(concat('col3', ' ', 'col4'), 'value')
    )
)

# SELECT concat(col1, . , col2) AS fn_result FROM t WHERE concat(col3,  , col4) = %(p1)s
# {'p1': 'value'}
```

`core` function examples

```python
count('name')                              # count(name)
max_('price')                              # max(price)
min_('age')                                # min(age)
sum_('money')                              # sum(money)
avg('success')                             # avg(success)
length('col_name')                         # length(col_name)
upper('col_name')                          # upper(col_name)
lower('col_name')                          # lower(col_name)
now_()                                     # now()
replace_('col_name', 'Saruman', 'Gandalf') # replace(col_name, 'Saruman', 'Gandalf')
position('col_name', 'Matrix')             # position(col_name IN 'Matrix')
generate_series(3, 12, 3)                  # generate_series(3, 12, 3)
null_if('col_name', 'unknown')             # nullif(col_name, 'unknown')
add('col1', 'col2', 'col3')                # (col1 + col2 + col3)
div('col1', 'col2', 'col3')                # (col1 + col2 + col3)
sub('col1', 'col2', 'col3')                # (col1 - col2 - col3)
mul('col1', 'col2', 'col3')                # (col1 * col2 * col3)
```

## WINDOW Functions

Aliased windows example:

```python
from david8 import get_default_qb
from david8.frames import rows, unbounded_preceding, current_row, unbounded_following
from david8.expressions import window_spec, desc
from david8.functions import sum_, null_if

qb = get_default_qb()
query = (
    qb
    .select(
        'category',
        'order_date',
        sum_('revenue').over(
            order_by=['order_date'],
            frame_mode=rows(unbounded_preceding(), current_row()),
            window='w',
        ).as_('running_revenue'),
        sum_('revenue').over(
            order_by=['order_date'],
            frame_mode=rows(unbounded_preceding(), unbounded_following()),
            window='w',
        ).as_('total_revenue'),
    )
    .from_table('orders')
    .window('base', window_spec(partition_by=['category']))
    .window('w', window_spec(window='base'))
    .order_by('category', 'order_date')
)
```

SQL:
```sql
SELECT category,
       order_date,
       sum(revenue) OVER (w ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_revenue,
       sum(revenue) OVER (w ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS total_revenue
  FROM orders
 ORDER BY category, order_date
WINDOW base AS (PARTITION BY category),
          w AS (base)
```

inline window specification:

```python
query = (
    qb
    .select(
        sum_('salary').over(
            partition_by=[null_if('dept', 0)],
            order_by=[desc('category')]
        ).as_('by_dept')
    )
)
```

SQL:

```sql
SELECT sum(salary) OVER (PARTITION BY nullif(dept, 0) ORDER BY category DESC) AS by_dept
```

See [window](https://github.com/d-ganchar/david8/blob/main/tests/test_select.py), [window_fn](https://github.com/d-ganchar/david8/blob/main/tests/test_functions.py) `tests`

## FILTER

```python
from david8.functions import var_pop, min_
from david8.predicates import eq

query = (
    qb
    .select(
        var_pop('salary')
            .filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date'])
            .as_('alias1'),
        min_('salary')
            .filter(eq('status', 'ok'))
            .over(partition_by=['dept'], order_by=['date'])
            .as_('alias2'),
    )
).get_sql()

# SELECT var_pop(salary) FILTER (status = %(p1)s) OVER (PARTITION BY dept ORDER BY date) AS alias1,
#        min(salary) FILTER (status = %(p2)s) OVER (PARTITION BY dept ORDER BY date) AS alias2
# {'p1': 'ok', 'p2': 'ok'}
```