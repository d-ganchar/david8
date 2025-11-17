import dataclasses

from ..protocols.dialect import DialectProtocol, ParamStyleProtocol


@dataclasses.dataclass(slots=True)
class BaseDialect(DialectProtocol):
    def __init__(self, param_style: ParamStyleProtocol, is_quote_mode: bool = False):
        self._param_style = param_style
        self._is_quote_mode = is_quote_mode

    def quote_ident(self, name: str) -> str:
        if self._is_quote_mode:
            return f'"{name}"'

        return name

    def get_paramstyle(self) -> ParamStyleProtocol:
        return self._param_style

    def is_quote_mode(self) -> bool:
        return self._is_quote_mode

