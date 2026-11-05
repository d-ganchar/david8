from collections.abc import Iterable
from dataclasses import dataclass

from .core.arg_convertors import to_col_or_expr
from .protocols.dialect import DialectProtocol
from .protocols.sql import ExprProtocol, LogicalOperatorProtocol


@dataclass(slots=True)
class _ArgsLogicalOperator(LogicalOperatorProtocol):
    _name: str
    _conditions: Iterable[ExprProtocol | LogicalOperatorProtocol]

    def get_sql(self, dialect: DialectProtocol) -> str:
        conditions = f' {self._name} '.join(c.get_sql(dialect) for c in self._conditions)
        return f'({conditions})'


@dataclass(slots=True)
class _NotLogicalOperator(LogicalOperatorProtocol):
    _value: str | ExprProtocol

    def get_sql(self, dialect: DialectProtocol) -> str:
        return f'NOT {to_col_or_expr(self._value, dialect)}'


def or_(*args: ExprProtocol | LogicalOperatorProtocol) -> LogicalOperatorProtocol:
    return _ArgsLogicalOperator(_name='OR', _conditions=args)


def and_(*args: ExprProtocol | LogicalOperatorProtocol) -> LogicalOperatorProtocol:
    return _ArgsLogicalOperator(_name='AND', _conditions=args)


def xor(*args: ExprProtocol | LogicalOperatorProtocol) -> LogicalOperatorProtocol:
    return _ArgsLogicalOperator(_name='XOR', _conditions=args)


def not_(value: str | ExprProtocol) -> LogicalOperatorProtocol:
    """
    .where(not_('column_name')) => WHERE NOT column_name
    """
    return _NotLogicalOperator(_value=value)
