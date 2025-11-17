import dataclasses

from david8.core.base_aliased import BaseAliased, Parameter, Value
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import FunctionProtocol


class _StrArgsFunction(FunctionProtocol, BaseAliased):
    def __init__(self, name: str, args: tuple) -> None:
        super().__init__()
        self._name = name
        self._args = args

    def _get_sql(self, dialect: DialectProtocol) -> str:
        items = ()

        for item in self._args:
            if isinstance(item, str):
                items += (dialect.quote_ident(item),)
                continue
            if isinstance(item, float | int):
                items += (f"'{item}'",)
                continue

            items += (item.get_sql(dialect),)

        return f"{self._name}({', '.join(items)})"


@dataclasses.dataclass(slots=True)
class StrArgsCallableFactory:
    """
    str works as column name. concat('col_name', 2, 0.5, val('test')) -> concat(col_name, '2', '0.5', 'test')
    """
    name: str

    def __call__(self, *args: FunctionProtocol | int | float | str | Parameter | Value) -> FunctionProtocol:
        return _StrArgsFunction(self.name, args)


class _OneArgDistinctFunction(FunctionProtocol, BaseAliased):
    """
    SUM(DISTINCT price)
    AVG(DISTINCT quantity)
    STDDEV(DISTINCT score)
    """
    def __init__(self, name: str, column: str = '', distinct: bool = False) -> None:
        super().__init__()
        self._name = name
        self._distinct = distinct
        self._column = column

    def _get_sql(self, dialect: DialectProtocol) -> str:
        name = f"{self._name}({'DISTINCT ' if self._distinct else ''}"
        return f"{name}{dialect.quote_ident(self._column)})"


@dataclasses.dataclass(slots=True)
class OneArgDistinctCallableFactory:
    name: str

    def __call__(self, column: str, distinct: bool = False) -> FunctionProtocol:
        return _OneArgDistinctFunction(self.name, column, distinct)
