from collections.abc import Callable

from david8.expressions import Column, Parameter
from david8.fn_generator import StrArgsFunction
from david8.protocols.sql import SqlFunctionProtocol

concat: Callable[
    [SqlFunctionProtocol | int | float | str | Column | Parameter, ...],
    SqlFunctionProtocol
] = StrArgsFunction('concat')
