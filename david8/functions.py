from .core.fn_generator import (
    CastFactory as _CastCallableFactory,
)
from .core.fn_generator import (
    FirstCol1StrArgFactory as _FirstCol1StrArgFactory,
)
from .core.fn_generator import (
    FirstCol1ValFactory as _FirstCol1ValFactory,
)
from .core.fn_generator import (
    FirstCol2IntArgFactory as _FirstCol2IntArgFactory,
)
from .core.fn_generator import (
    FirstCol2StrArgFactory as _FirstCol2StrArgFactory,
)
from .core.fn_generator import (
    GenerateSeriesFactory as _GenerateSeriesFactory,
)
from .core.fn_generator import OneArgDistinctWindowFactory as _OneArgDistinctWindowFactory
from .core.fn_generator import (
    SeparatedArgsFnFactory as _SeparatedArgsFnFactory,
)
from .core.fn_generator import (
    StrArgFactory as _StrArgCallableFactory,
)

lower = _StrArgCallableFactory(name='lower')
upper = _StrArgCallableFactory(name='upper')
length = _StrArgCallableFactory(name='length')
trim = _StrArgCallableFactory(name='trim')

count = _OneArgDistinctWindowFactory(name='count')
avg = _OneArgDistinctWindowFactory(name='avg')
sum_ = _OneArgDistinctWindowFactory(name='sum')
max_ = _OneArgDistinctWindowFactory(name='max')
min_ = _OneArgDistinctWindowFactory(name='min')

concat = _SeparatedArgsFnFactory(name='concat')
add = _SeparatedArgsFnFactory(name='', separator=' + ')
sub = _SeparatedArgsFnFactory(name='', separator=' - ')
mul = _SeparatedArgsFnFactory(name='', separator=' * ')
div = _SeparatedArgsFnFactory(name='', separator=' / ')

now_ = _SeparatedArgsFnFactory(name='now')
uuid_ = _SeparatedArgsFnFactory(name='uuid')

cast = _CastCallableFactory()

replace_ = _FirstCol2StrArgFactory(name='replace')
substring = _FirstCol2IntArgFactory(name='substring')
position = _FirstCol1StrArgFactory(name='position', separator=' IN ')
generate_series = _GenerateSeriesFactory()
null_if = _FirstCol1ValFactory(name='nullif')
