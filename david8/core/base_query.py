import dataclasses
from typing import Any

from ..protocols.dialect import DialectProtocol
from ..protocols.sql import QueryProtocol
from .log import log_and_reset


@dataclasses.dataclass(slots=True)
class BaseQuery(QueryProtocol):
    dialect: DialectProtocol

    def _render_sql_prefix(self, dialect: DialectProtocol) -> str:
        return ''

    def _render_sql_postfix(self, dialect: DialectProtocol) -> str:
        return ''

    def _render_sql(self, dialect: DialectProtocol) -> str:
        return ''

    def _get_sql(self, dialect: DialectProtocol) -> str:
        return f'{self._render_sql_prefix(dialect)}{self._render_sql(dialect)}{self._render_sql_postfix(dialect)}'

    @log_and_reset
    def get_sql(self, dialect: DialectProtocol = None) -> str:
        return self._get_sql(dialect or self.dialect)

    def get_parameters(self) -> dict:
        return self.dialect.get_paramstyle().get_parameters()

    def get_list_parameters(self) -> list[Any]:
        return self.dialect.get_paramstyle().get_list_parameters()

    def get_tuple_parameters(self) -> tuple[Any]:
        return self.dialect.get_paramstyle().get_tuple_parameters()

    def get_dialect(self) -> DialectProtocol:
        return self.dialect
