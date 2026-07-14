### Functions

See [functions](https://github.com/d-ganchar/david8_duckdb/blob/main/david8_duckdb/functions.py) and [test_functions](https://github.com/d-ganchar/david8_duckdb/blob/main/tests/test_functions.py), example:

```python
age('start', 'end')       # age(start, end)
json_keys('column_name')  # json_keys(column_name)

# json_keys(column_name, '$.ducks.country')
json_keys('column_name', '$.ducks.country')

# json_extract(column_name, '$.ducks.country[0]')
json_extract('column_name', '$.ducks.country[0]')

# regexp_extract_all(column_name, '(\\w+):\\s*(\\d+)')
regexp_extract_all('column_name', r'(\w+):\s*(\d+)')

# entropy(category) OVER (PARTITION BY user_id ORDER BY ts)
entropy('category').over(partition_by=['user_id'], order_by=['ts'])

# kurtosis(category) OVER (PARTITION BY user_id ORDER BY ts)
kurtosis('category').over(partition_by=['user_id'], order_by=['ts'])
```
