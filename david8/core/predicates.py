import dataclasses

from .. import DialectProtocol
from ..protocols.sql_statement import PredicateProtocol


@dataclasses.dataclass(slots=True)
class _BasePredicate(PredicateProtocol):
    _dialect: DialectProtocol = None

    def set_dialect(self, dialect: DialectProtocol):
        self._dialect = dialect


class _ValPredicate(_BasePredicate):
    def __init__(self,  column: str, value: int | float | str, operator: str):
        self._column = column
        self._value = value
        self._operator = operator
        self._dialect: DialectProtocol | None = None

    def get_sql(self) -> str:
        placeholder = self._dialect.get_paramstyle().add_param(self._value)
        return f'{self._dialect.quote_ident(self._column)} {self._operator} {placeholder}'


class _BetweenPredicate(_BasePredicate):
    def __init__(self, column: str, start: str, end: str):
        self._column = column
        self._start = start
        self._end = end
        self._dialect: DialectProtocol | None = None

    def get_sql(self) -> str:
        start = self._dialect.get_paramstyle().add_param(self._start)
        end = self._dialect.get_paramstyle().add_param(self._end)
        column = self._dialect.quote_ident(self._column)
        return f'{column} BETWEEN {start} AND {end}'


class _IsNullPredicate(_BasePredicate):
    def __init__(self, column: str, is_null: bool):
        self._column = column
        self._dialect: DialectProtocol | None = None
        self._is_null = is_null

    def get_sql(self) -> str:
        column = self._dialect.quote_ident(self._column)
        is_null = 'NULL' if self._is_null else 'NOT NULL'
        return f'{column} IS {is_null}'


class _ColLikePredicate(_BasePredicate):
    def __init__(self, column: str, value: str):
        self._column = column
        self._dialect: DialectProtocol | None = None
        self._value = value

    def get_sql(self) -> str:
        column = self._dialect.quote_ident(self._column)
        return f"{column} LIKE '{self._value}'"


def eq_val(column: str, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '=')

def gt_val(column: str, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '>')

def ge_val(column: str, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '>=')

def lt_val(column: str, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '<')

def le_val(column: str, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '<=')

def ne_val(column: str, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '!=')

def between_val(column: str, start: str, end: str) -> PredicateProtocol:
    return _BetweenPredicate(column, start, end)

def col_is_null(column: str, is_null: bool = True) -> PredicateProtocol:
    """
    is_null=False => IS NOT NULL
    """
    return _IsNullPredicate(column, is_null)

def col_like(column: str, value: str) -> PredicateProtocol:
    return _ColLikePredicate(column, value)
