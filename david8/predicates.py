from .core.base_aliased import BetweenPredicate as _BetweenPredicate
from .core.base_aliased import InPredicate as _InPredicate
from .core.base_aliased import IsPredicate as _IsPredicate
from .core.base_aliased import LeftColRightColPredicate as _LeftColRightColPredicate
from .core.base_aliased import LeftColRightParamPredicate as _LeftColRightParamPredicate
from .protocols.sql import ExprProtocol, PredicateProtocol, SelectProtocol


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
