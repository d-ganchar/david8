from .core.arg_convertors import to_col_or_expr
from .core.base_aliased import BaseAliased as _BaseAliased
from .protocols.dialect import DialectProtocol
from .protocols.sql import ExprProtocol, PredicateProtocol


class _IsPredicate(PredicateProtocol, _BaseAliased):
    def __init__(self, left: str | ExprProtocol, right: str | ExprProtocol):
        super().__init__()
        self._left = left
        self._right = right

    def _get_sql(self, dialect: DialectProtocol) -> str:
        left = to_col_or_expr(self._left, dialect)
        right = to_col_or_expr(self._right, dialect)
        return f'{left} IS {right}'


class _LeftColRightParamPredicate(PredicateProtocol, _BaseAliased):
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
        col = dialect.quote_ident(self._left)
        if isinstance(self._right, ExprProtocol):
            placeholder = self._right.get_sql(dialect)
            return f'{col} {self._operator} {placeholder}'

        _, placeholder = dialect.get_paramstyle().add_param(self._right)
        return f'{col} {self._operator} {placeholder}'


class _LeftColRightColPredicate(PredicateProtocol, _BaseAliased):
    def __init__(self, left_column: str, right_column: str, operator: str) -> None:
        super().__init__()
        self._left_column = left_column
        self._right_column = right_column
        self._operator = operator

    def _get_sql(self, dialect: DialectProtocol) -> str:
        left_col = dialect.quote_ident(self._left_column)
        right_col = dialect.quote_ident(self._right_column)

        return f'{left_col} {self._operator} {right_col}'


class _LeftExprRightExprPredicate(PredicateProtocol, _BaseAliased):
    def __init__(self, left_expr: ExprProtocol, right_expr: ExprProtocol, operator: str) -> None:
        super().__init__()
        self._left_expr = left_expr
        self._right_expr = right_expr
        self._operator = operator

    def _get_sql(self, dialect: DialectProtocol) -> str:
        return f'{self._left_expr.get_sql(dialect)} {self._operator} {self._right_expr.get_sql(dialect)}'


class _BetweenPredicate(PredicateProtocol, _BaseAliased):
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

# column <> parameter | value | sql expression. examples:
# WHERE category = %(p1)s
# WHERE category = 'test'
# WHERE category = concat(...)
def eq(column: str, value: int | float | str | ExprProtocol) -> PredicateProtocol:
    return _LeftColRightParamPredicate(column, value, '=')

def gt(column: str, value: int | float | ExprProtocol) -> PredicateProtocol:
    return _LeftColRightParamPredicate(column, value, '>')

def ge(column: str, value: int | float | ExprProtocol) -> PredicateProtocol:
    return _LeftColRightParamPredicate(column, value, '>=')

def lt(column: str, value: int | float | ExprProtocol) -> PredicateProtocol:
    return _LeftColRightParamPredicate(column, value, '<')

def le(column: str, value: int | float | ExprProtocol) -> PredicateProtocol:
    return _LeftColRightParamPredicate(column, value, '<=')

def ne(column: str, value: int | float | str | ExprProtocol) -> PredicateProtocol:
    return _LeftColRightParamPredicate(column, value, '!=')

def between(
    column: str,
    start: str | float | int | ExprProtocol,
    end: str | float | int | ExprProtocol
) -> PredicateProtocol:
    return _BetweenPredicate(column, start, end)

# .where(is_('is_active', false)) => WHERE is_active IS FALSE
# .where(is_('is_active', not_(false))) => WHERE is_active IS NOT FALSE
def is_(left: str | ExprProtocol, right: str | ExprProtocol) -> PredicateProtocol:
    return _IsPredicate(left, right)

# columns predicates. example: WHERE col_name = col_name2, col_name != col_name2 ...
def eq_c(left_column: str, right_column: str) -> PredicateProtocol:
    return _LeftColRightColPredicate(left_column, right_column, '=')

def gt_c(left_column: str, right_column: str) -> PredicateProtocol:
    return _LeftColRightColPredicate(left_column, right_column, '>')

def ge_c(left_column: str, right_column: str) -> PredicateProtocol:
    return _LeftColRightColPredicate(left_column, right_column, '>=')

def lt_c(left_column: str, right_column: str) -> PredicateProtocol:
    return _LeftColRightColPredicate(left_column, right_column, '<')

def le_c(left_column: str, right_column: str) -> PredicateProtocol:
    return _LeftColRightColPredicate(left_column, right_column, '<=')

def ne_c(left_column: str, right_column: str) -> PredicateProtocol:
    return _LeftColRightColPredicate(left_column, right_column, '!=')

# expression predicates. example: WHERE concat(...) = (SELECT ...), max(...) != min(...) ...
def eq_e(left_expr: ExprProtocol, right_expr: ExprProtocol) -> PredicateProtocol:
    return _LeftExprRightExprPredicate(left_expr, right_expr, '=')

def gt_e(left_expr: ExprProtocol, right_expr: ExprProtocol) -> PredicateProtocol:
    return _LeftExprRightExprPredicate(left_expr, right_expr, '>')

def ge_e(left_expr: ExprProtocol, right_expr: ExprProtocol) -> PredicateProtocol:
    return _LeftExprRightExprPredicate(left_expr, right_expr, '>=')

def lt_e(left_expr: ExprProtocol, right_expr: ExprProtocol) -> PredicateProtocol:
    return _LeftExprRightExprPredicate(left_expr, right_expr, '<')

def le_e(left_expr: ExprProtocol, right_expr: ExprProtocol) -> PredicateProtocol:
    return _LeftExprRightExprPredicate(left_expr, right_expr, '<=')

def ne_e(left_expr: ExprProtocol, right_expr: ExprProtocol) -> PredicateProtocol:
    return _LeftExprRightExprPredicate(left_expr, right_expr, '!=')
