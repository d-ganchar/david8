from .core.base_dialect import BaseDialect
from .core.base_params import BaseParams
from .protocols.dialect import ParamStyleProtocol


class NumericParamStyle(BaseParams):
    def _render_param(self, key: str) -> str:
        return f'${key}'

    def get_parameters(self) -> list:
        return list(self._params_bag.values())


class QMarkParamStyle(BaseParams):
    def _render_param(self, key: str) -> str:
        return '?'

    def get_parameters(self) -> list:
        return list(self._params_bag.values())


class FormatParamStyle(BaseParams):
    def _render_param(self, key: str) -> str:
        return '%s'

    def get_parameters(self) -> tuple:
        return tuple(self._params_bag.values())


class NamedParamStyle(BaseParams):
    def _render_param(self, key: str) -> str:
        return f':p{key}'

    def get_parameters(self) -> dict:
        return {
            f'p{key}': value
            for key, value in self._params_bag.items()
        }


class PyFormatParamStyle(BaseParams):
    def _render_param(self, key: str) -> str:
        return f'%(p{key})s'

    def get_parameters(self) -> dict:
        return {
            f'p{key}': value
            for key, value in self._params_bag.items()
        }


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
