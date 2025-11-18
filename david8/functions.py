from david8.core.fn_generator import OneArgDistinctCallableFactory as _AggDistinctCallableFactory
from david8.core.fn_generator import SeparatedStrArgsCallableFactory as _SeparatedStrArgsCallableFactory

count = _AggDistinctCallableFactory(name='count')
avg = _AggDistinctCallableFactory(name='avg')
sum_ = _AggDistinctCallableFactory(name='sum')
max_ = _AggDistinctCallableFactory(name='max')
min_ = _AggDistinctCallableFactory(name='min')
concat = _SeparatedStrArgsCallableFactory(name='concat', separator=', ')
