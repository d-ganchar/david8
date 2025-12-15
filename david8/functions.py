from david8.core.fn_generator import (
    CastFactory as _CastCallableFactory,
)
from david8.core.fn_generator import (
    FirstCol1StrArgFactory as _FirstCol1StrArgFactory,
)
from david8.core.fn_generator import (
    FirstCol2IntArgFactory as _FirstCol2IntArgFactory,
)
from david8.core.fn_generator import (
    FirstCol2StrArgFactory as _FirstCol2StrArgFactory,
)
from david8.core.fn_generator import (
    GenerateSeriesFactory as _GenerateSeriesFactory,
)
from david8.core.fn_generator import (
    OneArgDistinctFactory as _OneArgDistinctCallableFactory,
)
from david8.core.fn_generator import (
    SeparatedArgsFnFactory as _SeparatedArgsFnFactory,
)
from david8.core.fn_generator import (
    StrArgFactory as _StrArgCallableFactory,
)

# length('col_name') | length(val('MyVAR')) | length(param('myParam')) | length(concat('col1', 'col2'))
lower = _StrArgCallableFactory(name='lower')
upper = _StrArgCallableFactory(name='upper')
length = _StrArgCallableFactory(name='length')
trim = _StrArgCallableFactory(name='trim')

# count('name', True) => count(DISTINCT name), min_('age', True) => min(DISTINCT age) = 33
count = _OneArgDistinctCallableFactory(name='count')
avg = _OneArgDistinctCallableFactory(name='avg')
sum_ = _OneArgDistinctCallableFactory(name='sum')
max_ = _OneArgDistinctCallableFactory(name='max')
min_ = _OneArgDistinctCallableFactory(name='min')

concat = _SeparatedArgsFnFactory(name='concat')

now_ = _SeparatedArgsFnFactory(name='now')
uuid_ = _SeparatedArgsFnFactory(name='uuid')

cast = _CastCallableFactory()

replace_ = _FirstCol2StrArgFactory(name='replace')
substring = _FirstCol2IntArgFactory(name='substring')
position = _FirstCol1StrArgFactory(name='position', separator=' IN ')
generate_series = _GenerateSeriesFactory()
