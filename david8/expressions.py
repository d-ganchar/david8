from .core.base_aliased import BaseCase as _BaseCase
from .core.base_aliased import BaseInterval as _BaseInterval
from .core.base_aliased import Column as _Column
from .core.base_aliased import create_parameter as _create_parameter
from .core.base_aliased import create_value
from .core.base_expressions import BaseDesc as _BaseDesc
from .core.base_frames import BaseOverClause as _BaseOverClause
from .protocols.sql import (
    AliasedProtocol,
    DescProtocol,
    ExprProtocol,
    FrameModeProtocol,
    FunctionProtocol,
    IntervalProtocol,
    LogicalOperatorProtocol,
    ParameterProtocol,
    PredicateProtocol,
    ValueProtocol,
    WindowSpecProtocol,
)


def val(value: str | int | float) -> ValueProtocol:
    return create_value(value)

def col(name: str) -> _Column:
    return _Column(name)

def param(value: str | int | float, fixed_name: bool = False) -> ParameterProtocol:
    return _create_parameter(value, fixed_name)

def case(
    *conditions: tuple[str | PredicateProtocol | LogicalOperatorProtocol, str | int | float | PredicateProtocol],
    else_: str | int | float | ExprProtocol,
) -> AliasedProtocol:
    return _BaseCase(conditions=conditions, else_=else_)

def interval(as_int: bool = True) -> IntervalProtocol:
    return _BaseInterval(as_int=as_int)

def desc(*args: str | int) -> DescProtocol:
    return _BaseDesc(items=args)

def window_spec(
    partition_by: list[str | FunctionProtocol] = None,
    order_by: list[str | DescProtocol] = None,
    window: str = '',
    frame_mode: FrameModeProtocol = None,
) -> WindowSpecProtocol:
    return _BaseOverClause(
        _window=window,
        _partition_by=partition_by,
        _order_by=order_by,
        _frame_mode=frame_mode,
    )
