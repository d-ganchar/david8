import unittest

from david8 import get_qb
from david8.core.base_dialect import BaseDialect
from david8.param_styles import PyFormatParamStyle
from david8.protocols.dialect import ParamStyleProtocol


class _TestDialect(BaseDialect):
    def __init__(self, is_quote_mode: bool = False, param_style: ParamStyleProtocol = None):
        self._is_quote_mode = is_quote_mode
        self._param_style = param_style or PyFormatParamStyle()


class BaseTest(unittest.TestCase):
    maxDiff = 1500

    qb = get_qb(_TestDialect())        # without quotes
    qb_w = get_qb(_TestDialect(True))  # with quotes
