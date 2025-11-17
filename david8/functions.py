from david8.core.fn_generator import OneArgDistinctCallableFactory as _AggDistinctCallableFactory
from david8.core.fn_generator import StrArgsCallableFactory as _StrArgsCallableFactory

count = _AggDistinctCallableFactory('count')
avg = _AggDistinctCallableFactory('avg')
sum_ = _AggDistinctCallableFactory('sum')
max_ = _AggDistinctCallableFactory('max')
min_ = _AggDistinctCallableFactory('min')
concat = _StrArgsCallableFactory('concat')
