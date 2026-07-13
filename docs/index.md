## Install and Initialization

```bash
$ pip install david8
```

```python
from logging.config import dictConfig
from david8 import get_default_qb
# enable logging if you need
dictConfig({
    'version': 1,
    'formatters': {'standard': {'format': '[%(levelname)s]: %(message)s'}},
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {'handlers': ['default'], 'level': 'INFO'},
        'david8': {'propagate': True},
    }
})

qb = get_default_qb()
```

## Placeholders and quote mode
By default `david8` will use `PyFormatParamStyle` with disabled `quote_mode`. Use [param_styles.py](https://github.com/d-ganchar/david8/blob/main/david8/param_styles.py) to change query _parameter / placeholder style_ or enable `quote_mode`.

<details>
  <summary>How to change parameter style or quote mode</summary>

```python
from david8 import get_default_qb
from david8.expressions import param
from david8.param_styles import *

for _qb in [
    get_default_qb(),
    get_default_qb(is_quote_mode=True),
    get_default_qb(QMarkParamStyle()),
    get_default_qb(NumericParamStyle()),
    get_default_qb(NamedParamStyle()),
    get_default_qb(FormatParamStyle()),
]:
    query = (
        _qb.select(
            param('one').as_('first_param'),
            param(2).as_('second_param'),
            'column_name'
        )
        .from_table('table_name')
    )

    # to see logging info and generate query parameters
    query.get_sql()
    # to get Query parameters
    # print(query.get_parameters()) will return dict from log
    print(query.get_tuple_parameters())
    print(query.get_list_parameters())

# [INFO]: SELECT %(p1)s AS first_param, %(p2)s AS second_param, column_name FROM table_name
# {'p1': 'one', 'p2': 2}
# ('one', 2)
# ['one', 2]
# [INFO]: SELECT %(p1)s AS "first_param", %(p2)s AS "second_param", "column_name" FROM "table_name"
# {'p1': 'one', 'p2': 2}
# ('one', 2)
# ['one', 2]
# [INFO]: SELECT ? AS first_param, ? AS second_param, column_name FROM table_name
# {'1': 'one', '2': 2}
# ('one', 2)
# ['one', 2]
# [INFO]: SELECT $1 AS first_param, $2 AS second_param, column_name FROM table_name
# {'1': 'one', '2': 2}
# ('one', 2)
# ['one', 2]
# [INFO]: SELECT :p1 AS first_param, :p2 AS second_param, column_name FROM table_name
# {'p1': 'one', 'p2': 2}
# ('one', 2)
# ['one', 2]
# [INFO]: SELECT %s AS first_param, %s AS second_param, column_name FROM table_name
# {'1': 'one', '2': 2}
# ('one', 2)
# ['one', 2]
```
</details>

## SQL formatter

Use [Filter Object](https://docs.python.org/3/library/logging.html#filter-objects) to format SQL. [sql-formatter](https://pypi.org/project/sql-formatter/) example:

<details>
  <summary>David8Filter + sql-formatter</summary>

```python
from logging import Filter, LogRecord
from logging.config import dictConfig
from sql_formatter.core import format_sql

from david8 import get_default_qb
from david8.functions import count
from david8.joins import left
from david8.predicates import ne

class David8Filter(Filter):
    def filter(self, record: LogRecord) -> bool:
        if record.name.startswith('david8'):
            record.msg = f'SQL query:\n%s\n\nQuery parameters: %s'
            record.args = (format_sql(record.args[0]), record.args[1])
        return True

dictConfig({
    'version': 1,
    'formatters': {'standard': {'format': '[%(levelname)s]: %(message)s'}},
    "filters": {
        "david8_filter": {
            "()": "__main__.David8Filter",
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'filters': ['david8_filter'],
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {'handlers': ['default'], 'level': 'INFO'},
        'david8': {'propagate': True},
    }
})

query = (
    get_default_qb()
    .select(
        'relkind',
        'name',
        count('*').as_('obj_counter'),
    )
    .from_table('pg_class', db_name='pg_catalog')
    .join(left().table('names').using('relkind'))
    .where(ne('relkind', 't'))
    .group_by('relkind', 'name')
    .order_by('relkind')
).get_sql()
# [INFO]: SQL query:
# SELECT relkind,
#        name,
#        count(*) as obj_counter
# FROM pg_catalog.pg_class
#     LEFT JOIN names using (relkind)
# WHERE relkind != %(p1)s
# GROUP BY relkind, name
# ORDER BY relkind
# 
# Query parameters: {'p1': 't'}
```
</details>
