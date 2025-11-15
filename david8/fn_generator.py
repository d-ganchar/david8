from typing import NamedTuple, cast

from david8.expressions import Column, Parameter
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import SqlFunctionProtocol


class _StrArgsFunction(NamedTuple):
    name: str
    args: tuple

    def get_sql(self, dialect: DialectProtocol) -> str:
        items = ()

        for item in self.args:
            if isinstance(item, str | float | int):
                items += (f"'{item}'",)
                continue

            items += (item.get_sql(dialect),)

        return f"{self.name}({', '.join(items)})"


class StrArgsCallableFactory(NamedTuple):
    name: str

    def __call__(self, *args: SqlFunctionProtocol | int | float | str | Column | Parameter) -> SqlFunctionProtocol:
        return cast(SqlFunctionProtocol, _StrArgsFunction(self.name, args))


class _AggDistinctFunction(NamedTuple):
    """
    SUM(DISTINCT price)
    AVG(DISTINCT quantity)
    STDDEV(DISTINCT score)
    """
    name: str
    column: str = ''
    distinct: bool = False

    def get_sql(self, dialect: DialectProtocol) -> str:
        name = f"{self.name}({'DISTINCT ' if self.distinct else ''}"
        return f"{name}{dialect.quote_ident(self.column)})"


class AggDistinctCallableFactory(NamedTuple):
    name: str

    def __call__(self, column: str, distinct: bool = False) -> SqlFunctionProtocol:
        return cast(SqlFunctionProtocol, _AggDistinctFunction(self.name, column, distinct))
