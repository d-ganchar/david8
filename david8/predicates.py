import dataclasses

from .protocols.dialect import DialectProtocol
from .protocols.sql import SqlExpressionProtocol


@dataclasses.dataclass(slots=True)
class _ValPredicate(SqlExpressionProtocol):
    def __init__(self,  column: str, value: int | float | str, operator: str):
        self._column = column
        self._value = value
        self._operator = operator

    def get_sql(self, dialect: DialectProtocol) -> str:
        placeholder = dialect.get_paramstyle().add_param(self._value)
        return f'{dialect.quote_ident(self._column)} {self._operator} {placeholder}'


@dataclasses.dataclass(slots=True)
class _BetweenPredicate(SqlExpressionProtocol):
    def __init__(self, column: str, start: str, end: str):
        self._column = column
        self._start = start
        self._end = end

    def get_sql(self, dialect: DialectProtocol) -> str:
        start = dialect.get_paramstyle().add_param(self._start)
        end = dialect.get_paramstyle().add_param(self._end)
        column = dialect.quote_ident(self._column)
        return f'{column} BETWEEN {start} AND {end}'


@dataclasses.dataclass(slots=True)
class _IsNullPredicate(SqlExpressionProtocol):
    def __init__(self, column: str, is_null: bool):
        self._column = column
        self._is_null = is_null

    def get_sql(self, dialect: DialectProtocol) -> str:
        column = dialect.quote_ident(self._column)
        is_null = 'NULL' if self._is_null else 'NOT NULL'
        return f'{column} IS {is_null}'


@dataclasses.dataclass(slots=True)
class _ColLikePredicate(SqlExpressionProtocol):
    def __init__(self, column: str, value: str):
        self._column = column
        self._value = value

    def get_sql(self, dialect: DialectProtocol) -> str:
        column = dialect.quote_ident(self._column)
        return f"{column} LIKE '{self._value}'"


def eq_val(column: str, value: int | float | str) -> SqlExpressionProtocol:
    return _ValPredicate(column, value, '=')

def gt_val(column: str, value: int | float | str) -> SqlExpressionProtocol:
    return _ValPredicate(column, value, '>')

def ge_val(column: str, value: int | float | str) -> SqlExpressionProtocol:
    return _ValPredicate(column, value, '>=')

def lt_val(column: str, value: int | float | str) -> SqlExpressionProtocol:
    return _ValPredicate(column, value, '<')

def le_val(column: str, value: int | float | str) -> SqlExpressionProtocol:
    return _ValPredicate(column, value, '<=')

def ne_val(column: str, value: int | float | str) -> SqlExpressionProtocol:
    return _ValPredicate(column, value, '!=')

def between_val(column: str, start: str, end: str) -> SqlExpressionProtocol:
    return _BetweenPredicate(column, start, end)

def col_is_null(column: str, is_null: bool = True) -> SqlExpressionProtocol:
    """
    is_null=False => IS NOT NULL
    """
    return _IsNullPredicate(column, is_null)

def col_like(column: str, value: str) -> SqlExpressionProtocol:
    return _ColLikePredicate(column, value)
