### UPDATE

```python
from david8.expressions import val
from david8.functions import concat, max_
from david8.predicates import eq


(
    qb
    .update()
    .table('tbl')
    # by default second argument works as a SQL parameter
    .set_('name', 'new name')
    .set_('age', 27)
    # but you can also use functions
    .set_('full_address', concat('billing', val('. '), 'shipping'))
    # ... and subqueries
    .set_(
        'max_spend',
        qb.select(max_('spend')).from_table('orders').where(eq('user_id', 1))
    )
    .where(eq('name', ''))
).get_sql()
# UPDATE tbl SET name = %(p1)s, age = %(p2)s, 
#                full_address = (concat(billing, '. ', shipping)),
#                max_spend = (SELECT max(spend) FROM orders WHERE user_id = %(p3)s)
#  WHERE name = %(p4)s
# {'p1': 'new name', 'p2': 27, 'p3': 1, 'p4': ''}


(
   qb
   .update()
   .table('movie')
   .set_('name', 'aliens')
   .set_record({'year': 1986, 'killer': 'Ripley'})
   .set_('cat', 'Jones')
   .where(eq('movie', '')
)

# UPDATE movie SET name = %(p1)s, year = %(p2)s, killer = %(p3)s, cat = %(p4)s WHERE movie = %(p5)s'
# {'p1': 'aliens', 'p2': 1986, 'p3': 'Ripley', 'p4': 'Jones', 'p5': ''}
```

### DELETE

```python
(
   qb
   .delete()
   .from_table('movie')
   .where(eq('name', ''), le('year', 1888))
).get_sql()
# DELETE FROM movie WHERE name = %(p1)s AND year <= %(p2)s
# {'p1': '', 'p2': 1888}
```

### INSERT

Insert a record / dictionary
```python
qb.insert().into('movie', 'art').record({'name': 'Aliens', 'year': 1986})
# INSERT INTO art.movie (name, year) VALUES (%(p1)s, %(p2)s)
# {'p1': 'Aliens', 'p2': 1986}
```

Insert data by column names:

```python
qb.insert().into('movie', 'art').values(
    ['name', 'year'],
    [['Aliens', 1986], ['Prometheus', 2012]],
)
# INSERT INTO art.movie (name, year) VALUES (%(p1)s, %(p2)s), (%(p3)s, %(p4)s)
# {'p1': 'Aliens', 'p2': 1986, 'p3': 'Prometheus', 'p4': 2012}
```

Insert from SELECT:
```python
qb.insert().into('movie', 'art').from_expr(
   ['name', 'year'],
   qb.select('name', 'year').from_table('old_movie').where(eq('name', 'Aliens'))
)

# INSERT INTO art.movie (name, year) SELECT name, year FROM old_movie WHERE name = %(p1)s',
# {'p1': 'Aliens'}
```

`insert().from_select()`, `insert().value()`, `insert().columns()` are deprecated since [1.5.0b1](https://github.com/d-ganchar/david8/releases/tag/1.5.0b1) ([#44](https://github.com/d-ganchar/david8/issues/44))