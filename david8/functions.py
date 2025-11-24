from david8.core.fn_generator import (
    OneArgDistinctCallableFactory as _AggDistinctCallableFactory,
)
from david8.core.fn_generator import (
    SeparatedStrArgsCallableFactory as _SeparatedStrArgsCallableFactory,
)
from david8.core.fn_generator import (
    StrArgCallableFactory as _StrArgCallableFactory,
)

# length('col_name') | length(val('MyVAR')) | length(param('myParam')) | length(concat('col1', 'col2'))
lower = _StrArgCallableFactory(name='lower')
upper = _StrArgCallableFactory(name='upper')
length = _StrArgCallableFactory(name='length')
trim = _StrArgCallableFactory(name='trim')

count = _AggDistinctCallableFactory(name='count')
avg = _AggDistinctCallableFactory(name='avg')
sum_ = _AggDistinctCallableFactory(name='sum')
max_ = _AggDistinctCallableFactory(name='max')
min_ = _AggDistinctCallableFactory(name='min')

concat = _SeparatedStrArgsCallableFactory(name='concat', separator=', ')
