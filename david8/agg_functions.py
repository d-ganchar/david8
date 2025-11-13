from collections.abc import Callable

from david8.fn_generator import AggDistinctFunction, CountFunction
from david8.protocols.sql import SqlFunctionProtocol

count: Callable[[str, bool | None], SqlFunctionProtocol] = CountFunction()
avg: Callable[[str, bool | None], SqlFunctionProtocol] = AggDistinctFunction('avg')
sum_: Callable[[str, bool | None], SqlFunctionProtocol] = AggDistinctFunction('sum')
max_: Callable[[str, bool | None], SqlFunctionProtocol] = AggDistinctFunction('max')
min_: Callable[[str, bool | None], SqlFunctionProtocol] = AggDistinctFunction('min')
