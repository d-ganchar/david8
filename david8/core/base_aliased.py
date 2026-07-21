import dataclasses

from ..protocols.dialect import DialectProtocol
from ..protocols.sql import (
    AliasedProtocol,
    ColumnProtocol,
    ExprProtocol,
    IntervalProtocol,
    ParameterProtocol,
    PredicateProtocol,
    SelectProtocol,
    ValueProtocol,
)
from .arg_convertors import to_col_or_expr


@dataclasses.dataclass(slots=True, kw_only=True)
class BaseAliased(AliasedProtocol):
    alias: str = ''

    def as_(self, alias: str) -> AliasedProtocol:
        self.alias = alias
        return self

    def _get_sql(self, dialect: DialectProtocol) -> str:
        raise NotImplementedError()

    def get_sql(self, dialect: DialectProtocol) -> str:
        sql = self._get_sql(dialect)
        if self.alias:
            return f'{sql} AS {dialect.quote_ident(self.alias)}'

        return sql


class Value(BaseAliased, ValueProtocol):
    def __init__(self, value: str | int | float) -> None:
        super().__init__()
        self._value = value

    def _get_sql(self, dialect: DialectProtocol) -> str:
        if isinstance(self._value, str):
            return f"'{self._value}'"
        return f'{self._value}'


class SqlType(BaseAliased):
    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name

    def _get_sql(self, dialect: DialectProtocol) -> str:
        return f'{self._name}'


class Parameter(BaseAliased, ParameterProtocol):
    def __init__(self, value: str | int | float, fixed_name: bool = False) -> None:
        super().__init__()
        self._value = value
        self._fixed_name = fixed_name
        self._key = ''
        self._placeholder = ''

    def _get_sql(self, dialect: DialectProtocol) -> str:
        params = dialect.get_paramstyle()
        if self._fixed_name:
            if not params.was_param_added(self._key):
                key, placeholder = params.add_param(self._value)
                self._key = key
                self._placeholder = placeholder

            return self._placeholder

        _, placeholder = params.add_param(self._value)
        return placeholder


class Column(BaseAliased, ColumnProtocol):
    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name

    def get_name(self) -> str:
        return self._name

    def _get_sql(self, dialect: DialectProtocol) -> str:
        return f'{dialect.quote_ident(self._name)}'


class BaseCase(BaseAliased):
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
                then.get_sql(dialect) if isinstance(then, ExprProtocol) else create_parameter(then).get_sql(dialect),
            ]),)

        if isinstance(self._else_, ExprProtocol):
            else_ = self._else_.get_sql(dialect)
        else:
            else_ = create_parameter(self._else_).get_sql(dialect)

        return f'CASE {" ".join(conditions)} ELSE {else_} END'


class BaseInterval(BaseAliased, IntervalProtocol):
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


def create_parameter(value: str | int | float, fixed_name: bool = False) -> Parameter:
    return Parameter(value, fixed_name)


def create_value(value: str | int | float) -> ValueProtocol:
    return Value(value)


class IsPredicate(PredicateProtocol, BaseAliased):
    def __init__(self, left: str | ExprProtocol, right: None | str | bool |  ExprProtocol, not_: bool = False):
        super().__init__()
        self._left = left
        self._right = right
        self._predicate = 'IS NOT' if not_ else 'IS'

    def _get_sql(self, dialect: DialectProtocol) -> str:
        left = to_col_or_expr(self._left, dialect)
        if isinstance(self._right, bool):
            right = str(self._right).upper()
        elif self._right is None:
            right = 'NULL'
        else:
            right = to_col_or_expr(self._right, dialect)

        return f'{left} {self._predicate} {right}'


class InPredicate(PredicateProtocol, BaseAliased):
    def __init__(
        self,
        left_expr: str | ExprProtocol,
        right_expr: SelectProtocol | ExprProtocol | list[int | float | str | ExprProtocol],
        list_item_as_param: bool = False
    ) -> None:
        super().__init__()
        self._left_expr = left_expr
        self._right_expr = right_expr
        self._list_item_as_param = list_item_as_param

    def _get_sql(self, dialect: DialectProtocol) -> str:
        left = to_col_or_expr(self._left_expr, dialect)
        if isinstance(self._right_expr, (ExprProtocol, SelectProtocol)):
            return f'{left} IN ({self._right_expr.get_sql(dialect)})'

        items = ()

        for item in self._right_expr:
            if isinstance(item, ExprProtocol):
                items += (item.get_sql(dialect),)
                continue

            if self._list_item_as_param:
                items += (create_parameter(item).get_sql(dialect), )
            else:
                items += (create_value(item).get_sql(dialect), )

        right = ', '.join(items)
        return f'{left} IN ({right})'


class LeftColRightParamPredicate(PredicateProtocol, BaseAliased):
    def __init__(
        self,
        left: str,
        right: int | float | str | ExprProtocol,
        operator: str,
    ) -> None:
        super().__init__()
        self._left = left
        self._right = right
        self._operator = operator

    def _get_sql(self, dialect: DialectProtocol) -> str:
        if isinstance(self._left, ExprProtocol):
            col = self._left.get_sql(dialect)
        else:
            col = dialect.quote_ident(self._left)

        if isinstance(self._right, ExprProtocol):
            placeholder = self._right.get_sql(dialect)
            return f'{col} {self._operator} {placeholder}'

        _, placeholder = dialect.get_paramstyle().add_param(self._right)
        return f'{col} {self._operator} {placeholder}'


class LeftColRightColPredicate(PredicateProtocol, BaseAliased):
    def __init__(self, left_column: str, right_column: str, operator: str) -> None:
        super().__init__()
        self._left_column = left_column
        self._right_column = right_column
        self._operator = operator

    def _get_sql(self, dialect: DialectProtocol) -> str:
        left_col = dialect.quote_ident(self._left_column)
        right_col = dialect.quote_ident(self._right_column)

        return f'{left_col} {self._operator} {right_col}'


class BetweenPredicate(PredicateProtocol, BaseAliased):
    def __init__(
        self,
        column: str,
        start: str,
        end: str,
    ):
        super().__init__()
        self._column = column
        self._start = start
        self._end = end

    def _get_sql(self, dialect: DialectProtocol) -> str:
        if isinstance(self._start, ExprProtocol):
            start = self._start.get_sql(dialect)
        else:
            _, start = dialect.get_paramstyle().add_param(self._start)

        if isinstance(self._end, ExprProtocol):
            end = self._end.get_sql(dialect)
        else:
            _, end = dialect.get_paramstyle().add_param(self._end)

        return f'{dialect.quote_ident(self._column)} BETWEEN {start} AND {end}'
