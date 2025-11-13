import dataclasses

from .protocols.dialect import DialectProtocol
from .protocols.sql import SqlExpressionProtocol, SqlPredicateProtocol


@dataclasses.dataclass(slots=True)
class _ValSqlPredicate(SqlPredicateProtocol):
    column: str | SqlExpressionProtocol
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
class _BetweenSqlPredicate(SqlPredicateProtocol):
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
class _IsNullSqlPredicate(SqlPredicateProtocol):
    column: str
    is_null: bool

    def get_sql(self, dialect: DialectProtocol) -> str:
        column = dialect.quote_ident(self.column)
        is_null = 'NULL' if self.is_null else 'NOT NULL'
        return f'{column} IS {is_null}'


@dataclasses.dataclass(slots=True)
class _ColLikeSqlPredicate(SqlPredicateProtocol):
    column: str
    value: str

    def get_sql(self, dialect: DialectProtocol) -> str:
        column = dialect.quote_ident(self.column)
        return f"{column} LIKE '{self.value}'"


def eq_val(column: str | SqlExpressionProtocol, value: int | float | str) -> SqlPredicateProtocol:
    return _ValSqlPredicate(column, value, '=')

def gt_val(column: str | SqlExpressionProtocol, value: int | float | str) -> SqlPredicateProtocol:
    return _ValSqlPredicate(column, value, '>')

def ge_val(column: str | SqlExpressionProtocol, value: int | float | str) -> SqlPredicateProtocol:
    return _ValSqlPredicate(column, value, '>=')

def lt_val(column: str | SqlExpressionProtocol, value: int | float | str) -> SqlPredicateProtocol:
    return _ValSqlPredicate(column, value, '<')

def le_val(column: str | SqlExpressionProtocol, value: int | float | str) -> SqlPredicateProtocol:
    return _ValSqlPredicate(column, value, '<=')

def ne_val(column: str | SqlExpressionProtocol, value: int | float | str) -> SqlPredicateProtocol:
    return _ValSqlPredicate(column, value, '!=')

def between_val(column: str, start: str | float | int, end: str | float | int) -> SqlPredicateProtocol:
    return _BetweenSqlPredicate(column, start, end)

def col_is_null(column: str, is_null: bool = True) -> SqlPredicateProtocol:
    """
    is_null=False => IS NOT NULL
    """
    return _IsNullSqlPredicate(column, is_null)

def col_like(column: str, value: str) -> SqlPredicateProtocol:
    return _ColLikeSqlPredicate(column, value)


def eq(column: str | SqlExpressionProtocol, value: int | float | str) -> SqlPredicateProtocol:
    return _ValSqlPredicate(column, value, '=', False)

def gt(column: str | SqlExpressionProtocol, value: int | float | str) -> SqlPredicateProtocol:
    return _ValSqlPredicate(column, value, '>', False)

def ge(column: str | SqlExpressionProtocol, value: int | float | str) -> SqlPredicateProtocol:
    return _ValSqlPredicate(column, value, '>=', False)

def lt(column: str | SqlExpressionProtocol, value: int | float | str) -> SqlPredicateProtocol:
    return _ValSqlPredicate(column, value, '<', False)

def le(column: str | SqlExpressionProtocol, value: int | float | str) -> SqlPredicateProtocol:
    return _ValSqlPredicate(column, value, '<=', False)

def ne(column: str | SqlExpressionProtocol, value: int | float | str) -> SqlPredicateProtocol:
    return _ValSqlPredicate(column, value, '!=', False)

def between(column: str, start: str | float | int, end: str | float | int) -> SqlPredicateProtocol:
    return _BetweenSqlPredicate(column, start, end, False)
