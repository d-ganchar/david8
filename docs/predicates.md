## Overview
Use [predicates.py](https://github.com/d-ganchar/david8/blob/main/david8/predicates.py) module to compare _columns, values, parameters or function results_. Basic predicates (_without suffix_) compares a column with SQL parameter / value / expression. Example:

```python
from david8.predicates import eq
from david8.expressions import val as v, param as p
from david8.functions import concat

(
    qb.select(
        eq('movie', 'Aliens').as_('is_aliens'),
        eq('beer', v(0.5)).as_('is_zero_five'),
        eq('age', p(27)).as_('is_27'),
        eq('full_name', concat('name', val(' '), 'last_name')).as_('is_the_same'),
    )
).get_sql()

# SELECT movie = %(p1)s AS is_aliens,
#        beer = 0.5 AS is_zero_five,
#        age = %(p2)s AS is_27, 
#        full_name = concat(name, ' ', last_name) AS is_the_same
# {'p1': 'Aliens', 'p2': 27}
```

Use `col()` expression or predicates with the `_c`(_columns_) suffix to compare columns:

```python
from david8.predicates import ne, eq_c
from david8.expressions import col as c

qb.select(eq_c('name', 'last_name').as_('is_the_same')).get_sql()
# SELECT name = last_name AS is_the_same

qb.select(ne('column_1', c('column_2')).as_('alias')).get_sql()
# SELECT column_1 != column_2 AS alias
```

## Predicates table
<table>
  <thead>
    <tr>
      <th>python</th>
      <th>sql</th>
      <th>parameters</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>between('last_visit', '2023-01-01', '2024-01-01')</code></td>
      <td><code>last_visit BETWEEN %(p1)s AND %(p2)s</code></td>
      <td>see <a href="https://github.com/d-ganchar/david8/blob/main/tests/test_where_predicates.py">test</a> <code>{'p1': '2023-01-01', 'p2': '2024-01-01'}</code></td>
    </tr>
    <tr>
      <td><code>eq('col_name', 'parameter')</code></td>
      <td><code>col_name = %(p1)s</code></td>
      <td><code>{'p1': 'parameter'}</code></td>
    </tr>
    <tr>
      <td><code>le('col_name', 65)</code></td>
      <td><code>col_name &lt;= %(p1)s</code></td>
      <td><code>{'p1': 65}</code></td>
    </tr>
    <tr>
      <td><code>gt('col_name', 7)</code></td>
      <td><code>col_name &gt; %(p1)s</code></td>
      <td><code>{'p1': 7}</code></td>
    </tr>
    <tr>
      <td><code>ge('col_name', 9)</code></td>
      <td><code>col_name &gt;= %(p1)s</code></td>
      <td><code>{'p1': 9}</code></td>
    </tr>
    <tr>
      <td><code>ge(length('name'), length('last_name'))</code></td>
      <td><code>length(name) >= length(last_name)</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>lt('col_name', 27)</code></td>
      <td><code>col_name &lt; %(p1)s</code></td>
      <td><code>{'p1': 27}</code></td>
    </tr>
    <tr>
      <td><code>ne('col_name', 'name')</code></td>
      <td><code>col_name != %(p1)s</code></td>
      <td><code>{'p1': 'name'}</code></td>
    </tr>
    <tr>
      <td><code>eq_c('column1', 'column2')</code></td>
      <td><code>column1 = column2</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>le_c('column1', 'column2')</code></td>
      <td><code>column1 &lt;= column2</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>gt_c('column1', 'column2')</code></td>
      <td><code>column1 &gt; column2</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>ge_c('column1', 'column2')</code></td>
      <td><code>column1 &gt;= column2</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>lt_c('column1', 'column2')</code></td>
      <td><code>column1 &lt; column2</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>ne_c('column1', 'column2')</code></td>
      <td><code>column1 != column2</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>is_true('is_active')</code></td>
      <td><code>is_active IS TRUE</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>is_not_true('is_active')</code></td>
      <td><code>is_active IS NOT TRUE</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>is_false('is_active')</code></td>
      <td><code>is_active IS FALSE</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>is_not_false('is_active')</code></td>
      <td><code>is_active IS NOT FALSE</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>is_null('is_active')</code></td>
      <td><code>is_active IS NULL</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>is_not_null('is_active')</code></td>
      <td><code>is_active IS NOT NULL</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>in_('status', [1, 2, 3])</code></td>
      <td><code>status IN (1, 2, 3)</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>in_('status', [1, 2, 3], True)</code></td>
      <td><code>status IN (%(p1)s, %(p2)s, %(p3)s)</code></td>
      <td><code>{'p1': 1, 'p2': 2, 'p3': 3}</code></td>
    </tr>
    <tr>
      <td><pre><code>in_(
  'new_movie',
  [
   lower('movie'),
   lower(param('Ridley')),
   lower(val('James'))
  ]
 )</code></pre></td>
      <td><code>new_movie IN (lower(movie), lower(%(p1)s), lower('James'))</code></td>
      <td><code>{'p1': 'Ridley'}</code></td>
    </tr>
  </tbody>
</table>
