import dataclasses

from ..protocols.dialect import DialectProtocol
from ..protocols.sql import CreateTableProtocol, CreateViewProtocol, DropProtocol, QueryProtocol, SelectProtocol
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


@dataclasses.dataclass(slots=True)
class BaseCreateView(BaseQuery, CreateViewProtocol):
    query: SelectProtocol
    table: FullTableName = dataclasses.field(default_factory=FullTableName)
    or_replace: bool = False,
    if_not_exists: bool = False

    def _render_sql_prefix(self, dialect: DialectProtocol) -> str:
        if self.or_replace:
            return 'CREATE OR REPLACE VIEW '

        if self.if_not_exists:
            return 'CREATE VIEW IF NOT EXISTS '

        return 'CREATE VIEW '

    def _render_sql(self, dialect: DialectProtocol) -> str:
        return f'{self.table.get_sql(dialect)} AS {self.query.get_sql(dialect)}'


@dataclasses.dataclass(slots=True)
class BaseDropTableView(BaseQuery):
    _object_name: str
    _name: FullTableName = dataclasses.field(default_factory=FullTableName)
    _if_exists: bool = False

    def _render_sql_prefix(self, dialect: DialectProtocol) -> str:
        if self._if_exists:
            return f'{self._object_name} IF EXISTS '
        return f'{self._object_name} '

    def _render_sql(self, dialect: DialectProtocol) -> str:
        return self._name.get_sql(dialect)


@dataclasses.dataclass(slots=True)
class BaseDrop(BaseQuery, DropProtocol):
    query: QueryProtocol | None = None

    def _render_sql_prefix(self, dialect: DialectProtocol) -> str:
        return 'DROP '

    def _render_sql(self, dialect: DialectProtocol) -> str:
        if self.query:
            return f'{self.query.get_sql(dialect)}'
        return ''

    def table(self, table_name: str, db_name: str = '', if_exists: bool = False) -> DropProtocol:
        self.query = BaseDropTableView(
            _object_name='TABLE',
            dialect=self.dialect,
            _name=FullTableName(table_name, db_name),
            _if_exists=if_exists
        )
        return self

    def view(self, view_name: str, db_name: str = '', if_exists: bool = False) -> 'DropProtocol':
        self.query = BaseDropTableView(
            _object_name='VIEW',
            dialect=self.dialect,
            _name=FullTableName(view_name, db_name),
            _if_exists=if_exists
        )
        return self
