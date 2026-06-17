from .core.base_aliased import BaseAliased
from .core.base_aliased import Column as _Column
from .core.base_aliased import Parameter as _Parameter
from .core.base_aliased import Value as _Value
from .protocols.dialect import DialectProtocol
from .protocols.sql import (
    AliasedProtocol,
    ExprProtocol,
    IntervalProtocol,
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


class _Interval(BaseAliased, IntervalProtocol):
    def __init__(self, as_int: bool = True):
        super().__init__()
        self._as_int = as_int
        self._second: int | None = None
        self._minute: int | None = None
        self._hour: int | None = None
        self._day: int | None = None
        self._week: int | None = None
        self._month: int | None = None
        self._year: int | None = None
        self._quarter: int | None = None

    def second(self, value: int) -> 'IntervalProtocol':
        self._second = value
        return self

    def minute(self, value: int) -> 'IntervalProtocol':
        self._minute = value
        return self

    def hour(self, value: int) -> 'IntervalProtocol':
        self._hour = value
        return self

    def day(self, value: int) -> 'IntervalProtocol':
        self._day = value
        return self

    def week(self, value: int) -> 'IntervalProtocol':
        self._week = value
        return self

    def month(self, value: int) -> 'IntervalProtocol':
        self._month = value
        return self

    def quarter(self, value: int) -> 'IntervalProtocol':
        self._quarter = value
        return self

    def year(self, value: int) -> 'IntervalProtocol':
        self._year = value
        return self

    def _get_sql(self, dialect: DialectProtocol) -> str:
        values = []
        for prop in ('year', 'quarter', 'month', 'week', 'day', 'hour', 'minute', 'second'):
            value = getattr(self, f'_{prop}')
            if isinstance(value, int):
                values.append(f'{value} {prop.upper()}')

        if self._as_int:
            return f'INTERVAL {" ".join(values)}'
        return f'INTERVAL \'{" ".join(values)}\''


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

def interval(as_int: bool = True) -> IntervalProtocol:
    return _Interval(as_int=as_int)
