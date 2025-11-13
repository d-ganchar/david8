import dataclasses
from copy import deepcopy

from david8.expressions import Column, Parameter
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import SqlFunctionProtocol


@dataclasses.dataclass(slots=True)
class StrArgsFunction(SqlFunctionProtocol):
    _name: str
    _args: tuple = dataclasses.field(default_factory=tuple)

    def __call__(self, *args: SqlFunctionProtocol | int | float | str | Column | Parameter) -> SqlFunctionProtocol:
        self._args = args
        return deepcopy(self)

    def get_sql(self, dialect: DialectProtocol) -> str:
        items = []
        for item in self._args:
            if isinstance(item, str | float | int):
                items.append(f"'{item}'")
                continue

            items.append(item.get_sql(dialect))

        return f"{self._name}({', '.join(items)})"


@dataclasses.dataclass(slots=True)
class AggDistinctFunction(SqlFunctionProtocol):
    """
    SUM(DISTINCT price)
    AVG(DISTINCT quantity)
    STDDEV(DISTINCT score)
    """
    _name: str
    _column: str = ''
    _distinct: bool = False

    def __call__(self, column: str, distinct: bool = False) -> SqlFunctionProtocol:
        self._column = column
        self._distinct = distinct
        return deepcopy(self)

    def get_sql(self, dialect: DialectProtocol) -> str:
        name = f"{self._name}({'DISTINCT ' if self._distinct else ''}"
        return f"{name}{dialect.quote_ident(self._column)})"


@dataclasses.dataclass(slots=True)
class CountFunction(AggDistinctFunction):
    """
    COUNT()
    """
    _name: str = 'count'
    _column: str = ''
    _distinct: bool = False

    def __call__(self, column: str = '', distinct: bool = False) -> SqlFunctionProtocol:
        return AggDistinctFunction.__call__(self, column=column, distinct=distinct)
