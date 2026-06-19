from .core.fn_generator import OneArgWindowFactory as _OneArgWindowFactory
from .core.fn_generator import TwoArgWindowFactory as _TwoArgWindowFactory

var_pop = _OneArgWindowFactory(name='var_pop')
var_samp = _OneArgWindowFactory(name='var_samp')
stddev_pop = _OneArgWindowFactory(name='stddev_pop')
stddev_samp = _OneArgWindowFactory(name='stddev_samp')
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
