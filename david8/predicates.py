import dataclasses

from .core.base_aliased import BaseAliased
from .protocols.dialect import DialectProtocol
from .protocols.sql import ExprProtocol, ParameterProtocol, PredicateProtocol


class _ValPredicate(PredicateProtocol, BaseAliased):
    def __init__(
        self,
        column: str | ExprProtocol,
        value: int | float | str | ParameterProtocol,
        operator: str,
        add_param: bool = True
    ) -> None:
        super().__init__()
        self._column = column
        self._value = value
        self._operator = operator
        self._add_param = add_param

    def _get_sql(self, dialect: DialectProtocol) -> str:
        if self._add_param:
            if isinstance(self._value, ParameterProtocol):
                placeholder = self._value.get_sql(dialect)
            else:
                _, placeholder = dialect.get_paramstyle().add_param(self._value)
        elif isinstance(self._value, str):
            placeholder = f"'{self._value}'"
        else:
            placeholder = self._value

        if isinstance(self._column, str):
            col = dialect.quote_ident(self._column)
        else:
            col = self._column.get_sql(dialect)

        return f'{col} {self._operator} {placeholder}'


class _ColPredicate(PredicateProtocol, BaseAliased):
    def __init__(self, left_column: str, right_column: str, operator: str) -> None:
        super().__init__()
        self._left_column = left_column
        self._right_column = right_column
        self._operator = operator

    def _get_sql(self, dialect: DialectProtocol) -> str:
        if dialect.is_quote_mode():
            left_col = '.'.join([dialect.quote_ident(c) for c in self._left_column.split('.')])
            right_col = '.'.join([dialect.quote_ident(c) for c in self._right_column.split('.')])
        else:
            left_col = dialect.quote_ident(self._left_column)
            right_col = dialect.quote_ident(self._right_column)

        return f'{left_col} {self._operator} {right_col}'


@dataclasses.dataclass(slots=True)
class _BetweenPredicate(PredicateProtocol):
    def __init__(
        self,
        column: str,
        start: str,
        end: str,
        add_param: bool = True,
    ):
        self._column = column
        self._start = start
        self._end = end
        self._add_param = add_param

    def get_sql(self, dialect: DialectProtocol) -> str:
        if self._add_param:
            if isinstance(self._start, ParameterProtocol):
                start = self._start.get_sql(dialect)
            else:
                _, start = dialect.get_paramstyle().add_param(self._start)

            if isinstance(self._end, ParameterProtocol):
                end = self._end.get_sql(dialect)
            else:
                _, end = dialect.get_paramstyle().add_param(self._end)
        else:
            if isinstance(self._start, str):
                start = f"'{self._start}'"
            else:
                start = self._start
            if isinstance(self._end, str):
                end = f"'{self._end}'"
            else:
                end = self._end

        return f'{dialect.quote_ident(self._column)} BETWEEN {start} AND {end}'


@dataclasses.dataclass(slots=True)
class _IsNullPredicate(PredicateProtocol):
    def __init__(self, column: str, is_null: bool) -> None:
        self._column = column
        self._is_null = is_null

    def get_sql(self, dialect: DialectProtocol) -> str:
        column = dialect.quote_ident(self._column)
        is_null = 'NULL' if self._is_null else 'NOT NULL'
        return f'{column} IS {is_null}'


@dataclasses.dataclass(slots=True)
class _ColLikePredicate(PredicateProtocol):
    def __init__(self, column: str, value: str) -> None:
        self._column = column
        self._value = value

    def get_sql(self, dialect: DialectProtocol) -> str:
        column = dialect.quote_ident(self._column)
        return f"{column} LIKE '{self._value}'"

# compare columns with query param => WHERE category = %(p1)s
def eq_val(column: str | ExprProtocol, value: int | float | str | ParameterProtocol) -> PredicateProtocol:
    return _ValPredicate(column, value, '=')

def gt_val(column: str | ExprProtocol, value: int | float | str | ParameterProtocol) -> PredicateProtocol:
    return _ValPredicate(column, value, '>')

def ge_val(column: str | ExprProtocol, value: int | float | str | ParameterProtocol) -> PredicateProtocol:
    return _ValPredicate(column, value, '>=')

def lt_val(column: str | ExprProtocol, value: int | float | str | ParameterProtocol) -> PredicateProtocol:
    return _ValPredicate(column, value, '<')

def le_val(column: str | ExprProtocol, value: int | float | str | ParameterProtocol) -> PredicateProtocol:
    return _ValPredicate(column, value, '<=')

def ne_val(column: str | ExprProtocol, value: int | float | str | ParameterProtocol) -> PredicateProtocol:
    return _ValPredicate(column, value, '!=')

def between_val(
    column: str,
    start: str | float | int | ParameterProtocol,
    end: str | float | int | ParameterProtocol
) -> PredicateProtocol:
    return _BetweenPredicate(column, start, end)

def col_is_null(column: str, is_null: bool = True) -> PredicateProtocol:
    """
    is_null=False => IS NOT NULL
    """
    return _IsNullPredicate(column, is_null)

def col_like(column: str, value: str) -> PredicateProtocol:
    return _ColLikePredicate(column, value)

# compare column with a value => WHERE category = 'one'
def eq(column: str | ExprProtocol, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '=', False)

def gt(column: str | ExprProtocol, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '>', False)

def ge(column: str | ExprProtocol, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '>=', False)

def lt(column: str | ExprProtocol, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '<', False)

def le(column: str | ExprProtocol, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '<=', False)

def ne(column: str | ExprProtocol, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '!=', False)

def between(column: str, start: str | float | int, end: str | float | int) -> PredicateProtocol:
    return _BetweenPredicate(column, start, end, False)

def eq_col(left_column: str, right_column: str) -> PredicateProtocol:
    return _ColPredicate(left_column, right_column, '=')
