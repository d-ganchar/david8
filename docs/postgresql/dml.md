### UPDATE

`UPDATE FROM`

```python
(
   qb
   .update()
   .table('users', alias='u')
   .set_('age', 27)
   .from_table('data', alias='d')
   .where(eq_c('u.ud', 'd.id'))
).get_sql()
# UPDATE users AS u SET age = %(p1)s FROM data AS d WHERE u.ud = d.id
# {'p1': 27}
```

`RETURNING`

```python
(
   qb
   .update()
   ...
   .returning('id', 'name')
).get_sql()
# UPDATE ... RETURNING id, name
```

### ON CONFLICT

See [test_insert.py](https://github.com/d-ganchar/david8_postgresql/blob/main/tests/test_insert.py)

```python
from david8.predicates import eq_c

from david8_postgresql.on_conflict import do_nothing, do_update, excluded as e

query = (
    qb
    .insert()
    .into('t')
    .record({'id': 1, 'name': 'a'})
    .on_conflict(['id'], do_nothing(), [eq_c('col1', 'col2')])
    .returning('*')
).get_sql()
# INSERT INTO t (id, name) VALUES (%(p1)s, %(p2)s) ON CONFLICT (id) 
# WHERE col1 = col2 DO NOTHING RETURNING *
# {'p1': 1, 'p2': 'a'}

(
    qb
    .insert()
    .into('t')
    .record({'id': 1, 'name': 'a', 'val': 10})
    .on_conflict(
        ['id'],
        do_update({
            'name': e('name'),
            'val': e('val'),
        }),
        [eq_c('col1', 'col2')]
    )
).get_sql()
# INSERT INTO t (id, name, val) VALUES (%(p1)s, %(p2)s, %(p3)s) ON CONFLICT (id)
# WHERE col1 = col2 DO UPDATE SET name = EXCLUDED.name, val = EXCLUDED.val
# {'p1': 1, 'p2': 'a', 'p3': 10}

(
    qb
    .insert()
    .into('t')
    .record({'email': 'name@test.com', 'name': 'david8'})
    .on_conflict_constraint(
        'users_email_key',
        do_update({
            'name': e('name'),
            'val': e('val'),
        }),
    )
).get_sql()
# INSERT INTO t (email, name) VALUES (%(p1)s, %(p2)s) ON CONFLICT ON CONSTRAINT users_email_key
# DO UPDATE SET name = EXCLUDED.name, val = EXCLUDED.val
# {'p1': 'name@test.com', 'p2': 'david8'}
```

### Row-level locks

```python
qb.select('*').from_table('users').limit(1).for_update()
# SELECT * FROM users LIMIT 1 FOR UPDATE
```

see [test_select_with_lock](https://github.com/d-ganchar/david8_postgresql/blob/main/tests/test_select_with_lock.py)
