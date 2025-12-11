import dataclasses
from typing import Any

from ..protocols.ddl import CreateTableProtocol
from ..protocols.dialect import DialectProtocol
from ..protocols.dml import SelectProtocol
from .base_expressions import BaseExpression, FullTableName


@dataclasses.dataclass(slots=True)
class BaseCreateTable(BaseExpression, CreateTableProtocol):
    dialect: DialectProtocol
    query: SelectProtocol | None = None
    table: FullTableName = dataclasses.field(default_factory=FullTableName)

    def _render_prefix(self, dialect: DialectProtocol) -> str:
        return 'CREATE TABLE '

    def _render_main_expr(self, dialect: DialectProtocol) -> str:
        if self.query:
            return f'{self.table.get_sql(dialect)} AS {self.query.get_sql(dialect)}'
        return ''

    def set_table(self, table: str, db: str = '') -> None:
        self.table.set_names(table, db)

    def get_sql(self, dialect: DialectProtocol = None) -> str:
        return self._get_sql(dialect or self.dialect)

    def get_parameters(self) -> dict:
        return self.dialect.get_paramstyle().get_parameters()

    def get_list_parameters(self) -> list[Any]:
        return self.dialect.get_paramstyle().get_list_parameters()

    def get_tuple_parameters(self) -> tuple[Any]:
        return self.dialect.get_paramstyle().get_tuple_parameters()
