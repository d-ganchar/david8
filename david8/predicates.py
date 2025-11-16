import dataclasses

from .protocols.dialect import DialectProtocol
from .protocols.sql import ExprProtocol, PredicateProtocol


@dataclasses.dataclass(slots=True)
class _ValPredicate(PredicateProtocol):
    column: str | ExprProtocol
    value: int | float | str
    operator: str
    add_param: bool = True

    def get_sql(self, dialect: DialectProtocol) -> str:
        if self.add_param:
            placeholder = dialect.get_paramstyle().add_param(self.value)
        elif isinstance(self.value, str):
            placeholder = f"'{self.value}'"
        else:
            placeholder = self.value

        if isinstance(self.column, str):
            col = dialect.quote_ident(self.column)
        else:
            col = self.column.get_sql(dialect)

        return f'{col} {self.operator} {placeholder}'


@dataclasses.dataclass(slots=True)
class _ColPredicate(PredicateProtocol):
    _left_column: str
    _right_column: str
    _operator: str

    def get_sql(self, dialect: DialectProtocol) -> str:
        left_col = dialect.quote_ident(self._left_column)
        right_col = dialect.quote_ident(self._right_column)
        return f'{left_col} {self._operator} {right_col}'


@dataclasses.dataclass(slots=True)
class _BetweenPredicate(PredicateProtocol):
    column: str
    start: str
    end: str
    add_param: bool = True

    def get_sql(self, dialect: DialectProtocol) -> str:
        if self.add_param:
            start = dialect.get_paramstyle().add_param(self.start)
            end = dialect.get_paramstyle().add_param(self.end)
        else:
            if isinstance(self.start, str):
                start = f"'{self.start}'"
            else:
                start = self.start
            if isinstance(self.end, str):
                end = f"'{self.end}'"
            else:
                end = self.end

        return f'{dialect.quote_ident(self.column)} BETWEEN {start} AND {end}'


@dataclasses.dataclass(slots=True)
class _IsNullPredicate(PredicateProtocol):
    column: str
    is_null: bool

    def get_sql(self, dialect: DialectProtocol) -> str:
        column = dialect.quote_ident(self.column)
        is_null = 'NULL' if self.is_null else 'NOT NULL'
        return f'{column} IS {is_null}'


@dataclasses.dataclass(slots=True)
class _ColLikePredicate(PredicateProtocol):
    column: str
    value: str

    def get_sql(self, dialect: DialectProtocol) -> str:
        column = dialect.quote_ident(self.column)
        return f"{column} LIKE '{self.value}'"

# values as SQL parameters
def eq_val(column: str | ExprProtocol, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '=')

def gt_val(column: str | ExprProtocol, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '>')

def ge_val(column: str | ExprProtocol, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '>=')

def lt_val(column: str | ExprProtocol, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '<')

def le_val(column: str | ExprProtocol, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '<=')

def ne_val(column: str | ExprProtocol, value: int | float | str) -> PredicateProtocol:
    return _ValPredicate(column, value, '!=')

def between_val(column: str, start: str | float | int, end: str | float | int) -> PredicateProtocol:
    return _BetweenPredicate(column, start, end)

def col_is_null(column: str, is_null: bool = True) -> PredicateProtocol:
    """
    is_null=False => IS NOT NULL
    """
    return _IsNullPredicate(column, is_null)

def col_like(column: str, value: str) -> PredicateProtocol:
    return _ColLikePredicate(column, value)

# values as columns
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
