## COPY TO

```python
qb.copy_to(
    qb.select('name', 'value').from_table('events'),
    'events.csv',
    {'DELIMITER': "','", 'APPEND': True},
)
# COPY (SELECT name, value FROM events) TO 'events.csv' (DELIMITER ',', APPEND true)
```

see: [test_copy_to.py](https://github.com/d-ganchar/david8_duckdb/blob/main/tests/test_copy_to.py)

## EXPORT / IMPORT DATABASE

```python
qb.export_db('target_directory', {'FORMAT': 'csv', 'DELIMITER': "'|'"}
# EXPORT DATABASE 'target_directory' (FORMAT csv, DELIMITER '|')
```

see: [test_export_db.py](https://github.com/d-ganchar/david8_duckdb/blob/main/tests/test_export_db.py)