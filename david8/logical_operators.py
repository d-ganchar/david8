import dataclasses
from typing import Union

from .protocols.dialect import DialectProtocol
from .protocols.sql import ExprProtocol, LogicalOperatorProtocol


@dataclasses.dataclass(slots=True)
class _LogicalOperator(LogicalOperatorProtocol):
    _name: str
    _conditions: Union[ExprProtocol, 'LogicalOperatorProtocol', ...]

    def get_sql(self, dialect: DialectProtocol) -> str:
        conditions = f' {self._name} '.join(c.get_sql(dialect) for c in self._conditions)
        return f'({conditions})'


def or_(*args: ExprProtocol | LogicalOperatorProtocol):
    return _LogicalOperator(_name='OR', _conditions=args)


def and_(*args: ExprProtocol | LogicalOperatorProtocol):
    return _LogicalOperator(_name='AND', _conditions=args)


def xor(*args: ExprProtocol | LogicalOperatorProtocol):
    return _LogicalOperator(_name='XOR', _conditions=args)
