from collections.abc import Callable

from david8.fn_generator import AggDistinctCallableFactory
from david8.protocols.sql import SqlFunctionProtocol

count: Callable[[str, bool | None], SqlFunctionProtocol] = AggDistinctCallableFactory('count')
avg: Callable[[str, bool | None], SqlFunctionProtocol] = AggDistinctCallableFactory('avg')
sum_: Callable[[str, bool | None], SqlFunctionProtocol] = AggDistinctCallableFactory('sum')
max_: Callable[[str, bool | None], SqlFunctionProtocol] = AggDistinctCallableFactory('max')
min_: Callable[[str, bool | None], SqlFunctionProtocol] = AggDistinctCallableFactory('min')
