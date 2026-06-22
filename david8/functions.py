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
from .core.fn_generator import (
    TwoArgIntWindowFactory as _TwoArgIntWindowFactory,
)
from .core.fn_generator import (
    TwoArgWindowFactory as _TwoArgWindowFactory,
)
from .core.fn_generator import (
    ZeroArgAggFactory as _ZeroArgAggFnFactory,
)

var_pop = _OneArgDistinctWindowFactory(name='var_pop')
var_samp = _OneArgDistinctWindowFactory(name='var_samp')
stddev_pop = _OneArgDistinctWindowFactory(name='stddev_pop')
stddev_samp = _OneArgDistinctWindowFactory(name='stddev_samp')
first_value = _OneArgDistinctWindowFactory(name='first_value')

nth_value = _TwoArgIntWindowFactory(name='nth_value')
lag = _TwoArgIntWindowFactory(name='lag')
lead = _TwoArgIntWindowFactory(name='lead')
percent_rank = _ZeroArgAggFnFactory(name='percent_rank')
rank = _ZeroArgAggFnFactory(name='rank')
cume_dist = _ZeroArgAggFnFactory(name='cume_dist')

corr = _TwoArgWindowFactory(name='corr')
covar_pop = _TwoArgWindowFactory(name='covar_pop')
covar_samp = _TwoArgWindowFactory(name='covar_samp')
regr_slope = _TwoArgWindowFactory(name='regr_slope')
regr_intercept = _TwoArgWindowFactory(name='regr_intercept')
regr_r2 = _TwoArgWindowFactory(name='regr_r2')
regr_count = _TwoArgWindowFactory(name='regr_count')
regr_avgx = _TwoArgWindowFactory(name='regr_avgx')
regr_sxx = _TwoArgWindowFactory(name='regr_sxx')
regr_syy = _TwoArgWindowFactory(name='regr_syy')

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
