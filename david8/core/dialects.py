import dataclasses
from typing import Any

from ..protocols.dialect import DialectProtocol, ParamStyleProtocol


@dataclasses.dataclass(slots=True)
class _BaseParams(ParamStyleProtocol):
    _params_bag: dict[str, Any] = dataclasses.field(default_factory=dict)

    def add_param(self, value: Any) -> str:
        key = str(len(self._params_bag) + 1)
        self._params_bag[key] = value
        return self._render_param(key)

    def reset_parameters(self):
        self._params_bag.clear()

    def get_parameters(self):
        return self._params_bag

    def _render_param(self, key: str) -> str:
        raise NotImplementedError


class NumericParamStyle(_BaseParams):
    def _render_param(self, key: str) -> str:
        return f'${key}'

    def get_parameters(self) -> list:
        return list(self._params_bag.values())


class QMarkParamStyle(_BaseParams):
    def _render_param(self, key: str) -> str:
        return '?'

    def get_parameters(self) -> list:
        return list(self._params_bag.values())


class FormatParamStyle(_BaseParams):
    def _render_param(self, key: str) -> str:
        return '%s'

    def get_parameters(self) -> tuple:
        return tuple(self._params_bag.values())


class NamedParamStyle(_BaseParams):
    def _render_param(self, key: str) -> str:
        return f':p{key}'

    def get_parameters(self) -> dict:
        return {
            f'p{key}': value
            for key, value in self._params_bag.items()
        }


class PyFormatParamStyle(_BaseParams):
    def _render_param(self, key: str) -> str:
        return f'%(p{key})s'

    def get_parameters(self) -> dict:
        return {
            f'p{key}': value
            for key, value in self._params_bag.items()
        }



@dataclasses.dataclass(slots=True)
class _BaseDialect(DialectProtocol):
    _param_style: ParamStyleProtocol
    _is_quote_mode: bool = False

    def quote_ident(self, name: str) -> str:
        if self._is_quote_mode:
            return f'"{name}"'

        return name

    def get_paramstyle(self) -> ParamStyleProtocol:
        return self._param_style


class PostgresDialect(_BaseDialect):
    def __init__(self, is_quote_mode: bool = False, param_style: ParamStyleProtocol = None):
        self._is_quote_mode = is_quote_mode
        self._param_style = param_style or PyFormatParamStyle()


class MySQLDialect(_BaseDialect):
    def __init__(self, is_quote_mode: bool = False):
        self._is_quote_mode = is_quote_mode
        self._param_style = FormatParamStyle()


class ClickhouseDialect(_BaseDialect):
    def __init__(self, is_quote_mode: bool = False):
        self._is_quote_mode = is_quote_mode
        self._param_style = PyFormatParamStyle()


class DuckDbDialect(_BaseDialect):
    def __init__(self, is_quote_mode: bool = False):
        self._is_quote_mode = is_quote_mode
        self._param_style = QMarkParamStyle()


class SqliteDialect(_BaseDialect):
    def __init__(self, is_quote_mode: bool = False, param_style: ParamStyleProtocol = None):
        self._is_quote_mode = is_quote_mode
        self._param_style = param_style or NamedParamStyle()
