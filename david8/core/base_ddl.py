import dataclasses

from ..protocols.dialect import DialectProtocol
from ..protocols.sql import CreateTableProtocol, SelectProtocol
from .base_expressions import FullTableName
from .base_query import BaseQuery


@dataclasses.dataclass(slots=True)
class BaseCreateTable(BaseQuery, CreateTableProtocol):
    query: SelectProtocol | None = None
    table: FullTableName = dataclasses.field(default_factory=FullTableName)

    def _render_sql_prefix(self, dialect: DialectProtocol) -> str:
        return 'CREATE TABLE '

    def _render_sql(self, dialect: DialectProtocol) -> str:
        if self.query:
            return f'{self.table.get_sql(dialect)} AS {self.query.get_sql(dialect)}'
        return ''

    def set_table(self, table: str, db: str = '') -> None:
        self.table.set_names(table, db)
