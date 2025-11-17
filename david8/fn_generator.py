import dataclasses

from david8.core.base_aliased import BaseAliased
from david8.expressions import Column, Parameter
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import FunctionProtocol


class _StrArgsFunction(FunctionProtocol, BaseAliased):
    def __init__(self, name: str, args: tuple) -> None:
        super().__init__()
        self.name = name
        self.args = args

    def _get_sql(self, dialect: DialectProtocol) -> str:
        items = ()

        for item in self.args:
            if isinstance(item, str | float | int):
                items += (f"'{item}'",)
                continue

            items += (item.get_sql(dialect),)

        return f"{self.name}({', '.join(items)})"


@dataclasses.dataclass(slots=True)
class StrArgsCallableFactory:
    name: str

    def __call__(self, *args: FunctionProtocol | int | float | str | Column | Parameter) -> FunctionProtocol:
        return _StrArgsFunction(self.name, args)


class _AggDistinctFunction(FunctionProtocol, BaseAliased):
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
class AggDistinctCallableFactory:
    name: str

    def __call__(self, column: str, distinct: bool = False) -> FunctionProtocol:
        return _AggDistinctFunction(self.name, column, distinct)
