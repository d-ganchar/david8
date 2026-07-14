### Functions

See [functions](https://github.com/d-ganchar/david8_postgresql/blob/main/david8_postgresql/functions.py) and [test_functions](https://github.com/d-ganchar/david8_postgresql/blob/main/tests/test_functions.py)

Examples:

```python
qb.select(concat(
    'col1',
    1, 
    'col2',
    0.5,
    concat(v('static'), p(2))
).as_('new_field'))
# SELECT concat(col1 || '1' || col2 || '0.5' || concat('static' || %(p1)s)) 
# AS new_field
# {'p1': 2}

qb.select(extract_field('meta', 'version', 'name'))
# SELECT meta->'version'->'name'

qb.select(has_key('meta', 'version'))
# SELECT meta?'version'

qb.select(jsonb_set('meta', ['version', 'major'], 22))
# SELECT jsonb_set(meta, '{version,major}', '22'::jsonb)

qb.select(unnest('column1', 'column2', 'column3'))
# SELECT unnest(column1, column2, column3)

qb.select(array_remove('column1', 1))
# SELECT array_remove(column1, 1))

qb.select(array_replace('column1', 'Legacy', 'Fixed'))
# SELECT array_replace(column1, 'Legacy', 'Fixed'
...
```