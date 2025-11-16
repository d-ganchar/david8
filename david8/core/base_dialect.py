import dataclasses

from ..protocols.dialect import DialectProtocol, ParamStyleProtocol


@dataclasses.dataclass(slots=True)
class BaseDialect(DialectProtocol):
    _param_style: ParamStyleProtocol
    _is_quote_mode: bool = False

    def quote_ident(self, name: str) -> str:
        if self._is_quote_mode:
            return f'"{name}"'

        return name

    def get_paramstyle(self) -> ParamStyleProtocol:
        return self._param_style
