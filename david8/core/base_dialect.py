import dataclasses

from ..protocols.dialect import DialectProtocol, ParamStyleProtocol
from .base_expressions import FullTableName


@dataclasses.dataclass(slots=True)
class BaseDialect(DialectProtocol):
    def __init__(self, param_style: ParamStyleProtocol, is_quote_mode: bool = False):
        self._param_style = param_style
        self._is_quote_mode = is_quote_mode

    def quote_ident(self, name: str | FullTableName) -> str:
        if isinstance(name, FullTableName):
            return name.get_sql(self)

        if self._is_quote_mode:
            return '.'.join([f'"{c}"' for c in name.split('.')])
        return '.'.join([c for c in name.split('.')])

    def get_paramstyle(self) -> ParamStyleProtocol:
        return self._param_style
