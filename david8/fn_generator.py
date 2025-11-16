import dataclasses

from david8.expressions import Column, Parameter
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import FunctionProtocol


@dataclasses.dataclass(slots=True)
class _StrArgsFunction(FunctionProtocol):
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


@dataclasses.dataclass(slots=True)
class StrArgsCallableFactory:
    name: str

    def __call__(self, *args: FunctionProtocol | int | float | str | Column | Parameter) -> FunctionProtocol:
        return _StrArgsFunction(self.name, args)


@dataclasses.dataclass(slots=True)
class _AggDistinctFunction(FunctionProtocol):
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


@dataclasses.dataclass(slots=True)
class AggDistinctCallableFactory:
    name: str

    def __call__(self, column: str, distinct: bool = False) -> FunctionProtocol:
        return _AggDistinctFunction(self.name, column, distinct)
