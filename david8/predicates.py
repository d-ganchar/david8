from .core.arg_convertors import to_col_or_expr
from .core.base_aliased import BaseAliased as _BaseAliased
from .expressions import param, val
from .protocols.dialect import DialectProtocol
from .protocols.sql import ExprProtocol, PredicateProtocol, SelectProtocol


class _IsPredicate(PredicateProtocol, _BaseAliased):
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
        if isinstance(self._left, ExprProtocol):
            col = self._left.get_sql(dialect)
        else:
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

class _InPredicate(PredicateProtocol, _BaseAliased):
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
                items += (param(item).get_sql(dialect), )
            else:
                items += (val(item).get_sql(dialect), )

        right = ', '.join(items)
        return f'{left} IN ({right})'

def eq(column: str | ExprProtocol, value: int | float | str | ExprProtocol) -> PredicateProtocol:
    return _LeftColRightParamPredicate(column, value, '=')

def gt(column: str | ExprProtocol, value: int | float | ExprProtocol) -> PredicateProtocol:
    return _LeftColRightParamPredicate(column, value, '>')

def ge(column: str | ExprProtocol, value: int | float | ExprProtocol) -> PredicateProtocol:
    return _LeftColRightParamPredicate(column, value, '>=')

def lt(column: str | ExprProtocol, value: int | float | ExprProtocol) -> PredicateProtocol:
    return _LeftColRightParamPredicate(column, value, '<')

def le(column: str | ExprProtocol, value: int | float | ExprProtocol) -> PredicateProtocol:
    return _LeftColRightParamPredicate(column, value, '<=')

def ne(column: str | ExprProtocol, value: int | float | str | ExprProtocol) -> PredicateProtocol:
    return _LeftColRightParamPredicate(column, value, '!=')

def between(
    column: str,
    start: str | float | int | ExprProtocol,
    end: str | float | int | ExprProtocol
) -> PredicateProtocol:
    return _BetweenPredicate(column, start, end)

def is_(left: str | ExprProtocol, right: str | ExprProtocol) -> PredicateProtocol:
    return _IsPredicate(left, right)

def is_false(value: str | ExprProtocol) -> PredicateProtocol:
    return _IsPredicate(value, False)

def is_true(value: str | ExprProtocol) -> PredicateProtocol:
    return _IsPredicate(value, True)

def is_not_false(value: str | ExprProtocol) -> PredicateProtocol:
    return _IsPredicate(value, False, True)

def is_not_true(value: str | ExprProtocol) -> PredicateProtocol:
    return _IsPredicate(value, True, True)

def is_null(value: str | ExprProtocol) -> PredicateProtocol:
    return _IsPredicate(value, None)

def is_not_null(value: str | ExprProtocol) -> PredicateProtocol:
    return _IsPredicate(value, None, True)

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

def in_(
    left_expr: str | ExprProtocol,
    right_expr: SelectProtocol | ExprProtocol | list[int | float | str | ExprProtocol],
    list_item_as_param: bool = False,
) -> PredicateProtocol:
    return _InPredicate(left_expr, right_expr, list_item_as_param)
