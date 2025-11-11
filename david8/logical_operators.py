import dataclasses
from typing import Union

from .protocols.dialect import DialectProtocol as _DialectProtocol
from .protocols.sql import LogicalOperatorProtocol as LogicalOperatorProtocol
from .protocols.sql import SqlExpressionProtocol


@dataclasses.dataclass(slots=True)
class _LogicalOperator(LogicalOperatorProtocol):
    _name: str
    _conditions: Union[SqlExpressionProtocol, 'LogicalOperatorProtocol', ...]

    def get_sql(self, dialect: _DialectProtocol) -> str:
        conditions = f' {self._name} '.join(c.get_sql(dialect) for c in self._conditions)
        return f'({conditions})'


def or_(*args: Union[SqlExpressionProtocol, 'LogicalOperatorProtocol']):
    return _LogicalOperator(_name='OR', _conditions=args)


def and_(*args: Union[SqlExpressionProtocol, 'LogicalOperatorProtocol']):
    return _LogicalOperator(_name='AND', _conditions=args)


def xor(*args: Union[SqlExpressionProtocol, 'LogicalOperatorProtocol']):
    return _LogicalOperator(_name='XOR', _conditions=args)
