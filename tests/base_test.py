import unittest

from david8 import get_qb
from david8.core.base_dialect import BaseDialect
from david8.param_styles import PyFormatParamStyle


class BaseTest(unittest.TestCase):
    maxDiff = 1500

    qb = get_qb(BaseDialect(PyFormatParamStyle()))          # without quotes
    qb_w = get_qb(BaseDialect(PyFormatParamStyle(), True))  # with quotes
