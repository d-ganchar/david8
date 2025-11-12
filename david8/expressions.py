import dataclasses

from .protocols.dialect import DialectProtocol
from .protocols.sql import AsExpressionProtocol, SqlExpressionProtocol, SqlFunctionProtocol, SqlPredicateProtocol


@dataclasses.dataclass(slots=True)
class Column(SqlExpressionProtocol):
    name: str

    def get_sql(self, dialect: DialectProtocol) -> str:
        return f'{dialect.quote_ident(self.name)}'


@dataclasses.dataclass(slots=True)
class Parameter(SqlExpressionProtocol):
    value: str | int | float

    def get_sql(self, dialect: DialectProtocol) -> str:
        value = dialect.get_paramstyle().add_param(self.value)
        return value


@dataclasses.dataclass(slots=True)
class _AsExpression(AsExpressionProtocol):
    _value: str | int | float | SqlExpressionProtocol | SqlPredicateProtocol | Column | Parameter
    _alias: str

    def get_sql(self, dialect: DialectProtocol) -> str:
        alias = dialect.quote_ident(self._alias)
        if isinstance(self._value, str):
            return f"'{self._value}' AS {alias}"
        elif isinstance(self._value, (int, float)):
            return f'{self._value} AS {alias}'

        return f'{self._value.get_sql(dialect)} AS {alias}'


def as_(
    value: str | int | float | SqlFunctionProtocol | SqlPredicateProtocol | Column | Parameter,
    alias: str
) -> AsExpressionProtocol:
    return _AsExpression(value, alias)
