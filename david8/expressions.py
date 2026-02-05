from david8.core.base_aliased import BaseAliased
from david8.core.base_aliased import Column as _Column
from david8.core.base_aliased import Parameter as _Parameter
from david8.core.base_aliased import Value as _Value
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import (
    AliasedProtocol,
    ExprProtocol,
    LogicalOperatorProtocol,
    PredicateProtocol,
    ValueProtocol,
)


class _BaseCase(BaseAliased):
    def __init__(
        self,
        conditions: tuple[
            tuple[str | ExprProtocol, str | int | float | ExprProtocol],
            ...
        ],
        else_: str | int | float | ExprProtocol,
    ):
        super().__init__()
        self._conditions = conditions
        self._else_ = else_

    def _get_sql(self, dialect: DialectProtocol) -> str:
        conditions = ()
        for condition in self._conditions:
            when, then = condition
            conditions += (' '.join([
                'WHEN',
                dialect.quote_ident(when) if isinstance(when, str) else when.get_sql(dialect),
                'THEN',
                then.get_sql(dialect) if isinstance(then, ExprProtocol) else param(then).get_sql(dialect),
            ]),)

        if isinstance(self._else_, ExprProtocol):
            else_ = self._else_.get_sql(dialect)
        else:
            else_ = param(self._else_).get_sql(dialect)

        return f'CASE {" ".join(conditions)} ELSE {else_} END'

def val(value: str | int | float) -> ValueProtocol:
    return _Value(value)

def col(name: str) -> _Column:
    return _Column(name)

def param(value: str | int | float, fixed_name: bool = False) -> _Parameter:
    return _Parameter(value, fixed_name)

def case(
    *conditions: tuple[str | PredicateProtocol | LogicalOperatorProtocol, str | int | float | PredicateProtocol],
    else_: str | int | float | ExprProtocol,
) -> AliasedProtocol:
    return _BaseCase(conditions=conditions, else_=else_)
