from .core.base_dialect import BaseDialect
from .param_styles import FormatParamStyle, NamedParamStyle, PyFormatParamStyle, QMarkParamStyle
from .protocols.dialect import ParamStyleProtocol


class PostgresDialect(BaseDialect):
    def __init__(self, is_quote_mode: bool = False, param_style: ParamStyleProtocol = None):
        self._is_quote_mode = is_quote_mode
        self._param_style = param_style or PyFormatParamStyle()


class MySQLDialect(BaseDialect):
    def __init__(self, is_quote_mode: bool = False):
        self._is_quote_mode = is_quote_mode
        self._param_style = FormatParamStyle()


class ClickhouseDialect(BaseDialect):
    def __init__(self, is_quote_mode: bool = False):
        self._is_quote_mode = is_quote_mode
        self._param_style = PyFormatParamStyle()


class DuckDbDialect(BaseDialect):
    def __init__(self, is_quote_mode: bool = False):
        self._is_quote_mode = is_quote_mode
        self._param_style = QMarkParamStyle()


class SqliteDialect(BaseDialect):
    def __init__(self, is_quote_mode: bool = False, param_style: ParamStyleProtocol = None):
        self._is_quote_mode = is_quote_mode
        self._param_style = param_style or NamedParamStyle()
