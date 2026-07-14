### CREATE TABLE AS SELECT

```python
qb.create_table_as(
   qb.select('*').from_table('users').where(eq('status', 'active')),
   'active_users',
)
# CREATE TABLE active_users AS SELECT * FROM users WHERE status = %(p1)s
# {'p1': 'active'}
```

See [test_create_table](https://github.com/d-ganchar/david8/blob/main/tests/test_create_table.py)

### DROP TABLE

```python
qb.drop().table('events')                          # DROP TABLE events
qb.drop().table('events', 'game', if_exists=True)  # DROP TABLE IF EXISTS game.events
```

### DROP VIEW

```python
drop().view('events')                             # DROP VIEW events
qb.drop().view('events', 'game', if_exists=True)  # DROP VIEW IF EXISTS game.events
```

See [test_drop_table.py](https://github.com/d-ganchar/david8/blob/main/tests/test_drop_table.py)