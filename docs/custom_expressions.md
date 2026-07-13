### Query

An example of how to create any custom parameterized query

```python
import dataclasses

from david8 import get_default_qb
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import ExprProtocol


@dataclasses.dataclass(slots=True)
class CustomQuery(ExprProtocol):
    static_param: int
    dynamic_param: str

    def get_sql(self, dialect: DialectProtocol) -> str:
        # or you can use param
        # from david8.expressions import param as p
        # alias = p(self.dynamic_param).get_sql(dialect)
        _, alias = dialect.get_paramstyle().add_param(self.dynamic_param)

        col_name = dialect.quote_ident('col_name')
        return f'CUSTOM SQL ... SELECT {self.static_param}, {alias}, {col_name}'

query = get_default_qb().query(CustomQuery(static_param=1, dynamic_param='test'))
print(query.get_sql())         # CUSTOM SQL ... SELECT 1, %(p1)s, col_name
print(query.get_parameters())  # {'p1': 'test'}
```

### SELECT expression

```python
import dataclasses

from david8.protocols.dialect import DialectProtocol
from david8.expressions import param as p
from david8.protocols.sql import ExprProtocol

@dataclasses.dataclass(slots=True)
class InsertCat(ExprProtocol):
    cat: str
    age: int

    def get_sql(self, dialect: DialectProtocol) -> str:
        cat = p(self.cat).get_sql(dialect)
        age = p(self.age).get_sql(dialect)

        return f"insert_cat({cat}, {age})"

qb.select(InsertCat('Baksya', 2))
# SELECT insert_cat(%(p1)s, %(p2)s)
# {'p1': 'Baksya', 'p2': 2}
```

### INSERT expression

```python
import dataclasses

from david8.functions import sum_
from david8.predicates import between, ne
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import ExprProtocol


@dataclasses.dataclass(slots=True)
class SelectTotalRevenue(ExprProtocol):
    start: str
    end: str

    def get_sql(self, dialect: DialectProtocol) -> str:
        return (
            qb
            .select(
                'provider',
                sum_('revenue').as_('total_revenue'),
            )
            .from_table('table1')
            .where(between('date', self.start, self.end))
            .group_by('provider')
            .union(qb
                .select(
                    'provider',
                     sum_('revenue').as_('total_revenue'),
                )
                .from_table('table2')
                .where(
                    between('date', self.start, self.end),
                    ne('category', 'bug')
                )
                .group_by('provider')
            )
            .get_sql(dialect)
        )

qb.insert().into('total_revenue').from_expr(
    ['provider_name', 'total_revenue'],
    SelectTotalRevenue('2026-01-01', '2026-12-31')
).get_sql()

# INSERT INTO total_revenue (provider_name, total_revenue)
# SELECT provider, sum(revenue) AS total_revenue
#   FROM table1
#  WHERE date BETWEEN %(p1)s AND %(p2)s
#  GROUP BY provider
#  UNION ALL
# SELECT provider, sum(revenue) AS total_revenue
#   FROM table2
#  WHERE date BETWEEN %(p3)s AND %(p4)s AND category != %(p5)s
#  GROUP BY provider
# {'p1': '2026-01-01', 'p2': '2026-12-31', 'p3': '2026-01-01', 'p4': '2026-12-31', 'p5': 'bug'}
```

### Function

PostgreSQL expression `CAST(json_field->>'id' AS INTEGER) > 3`: extract `id` key from `json field` and compare with an integer value:

```python
from dataclasses import dataclass
from david8 import get_default_qb
from david8.protocols.dml import FunctionProtocol
from david8.expressions import param

@dataclass(slots=True)
class MyFunction(FunctionProtocol):
    col_name: str
    json_key: str
    value: int | str

    def get_sql(self, dialect: DialectProtocol) -> str:
        return f"CAST({dialect.quote_ident(self.col_name)}->>'{self.json_key}' AS INTEGER) > {int(self.value)}"


@dataclass(slots=True)
class MyParametrizedFunction(MyFunction):
    def get_sql(self, dialect: DialectProtocol) -> str:
        quoted_col = dialect.quote_ident(self.col_name)
        parameter = param(self.value).get_sql(dialect)
        return f"CAST({quoted_col}->>'{self.json_key}' AS INTEGER) > {parameter}"


qb = get_default_qb()
qb.select(MyFunction('json_field', 'id', 3)).from_table('table').get_sql()
qb.select(MyParametrizedFunction('json_field', 'id', 3)).from_table('table').get_sql()
# [INFO]: SELECT CAST(json_field->>'id' AS INTEGER) > 3 FROM table
# {}
# [INFO]: SELECT CAST(json_field->>'id' AS INTEGER) > %(p1)s FROM table
# {'p1': 3}
```