import dataclasses

from .protocols.dialect import DialectProtocol
from .protocols.sql import AsExpressionProtocol, SqlExpressionProtocol


@dataclasses.dataclass(slots=True)
class _AsExpression(AsExpressionProtocol):
    _value: str | SqlExpressionProtocol
    _alias: str

    def get_sql(self, dialect: DialectProtocol) -> str:
        alias = dialect.quote_ident(self._alias)
        if isinstance(self._value, str):
            value = dialect.quote_ident(self._value)
            return f'{value} AS {alias}'

        return f'{self._value.get_sql(dialect)} AS {alias}'


def as_(value: str | SqlExpressionProtocol, alias: str) -> AsExpressionProtocol:
    return _AsExpression(value, alias)
