from dataclasses import dataclass

from ..protocols.dialect import DialectProtocol
from ..protocols.query_builder import QueryBuilderProtocol
from ..protocols.sql import (
    AliasedProtocol,
    CreateTableProtocol,
    DeleteProtocol,
    ExprProtocol,
    FunctionProtocol,
    InsertProtocol,
    SelectProtocol,
    UpdateProtocol,
)
from .base_ddl import BaseCreateTable as _CreateTable
from .base_dml import BaseDelete as _Delete
from .base_dml import BaseInsert as _Insert
from .base_dml import BaseUpdate as _Update
from .base_dql import BaseSelect as _Select
from .base_expressions import FullTableName


@dataclass(slots=True)
class BaseQueryBuilder(QueryBuilderProtocol):
    def __init__(self, dialect: DialectProtocol):
        self._dialect = dialect

    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol:
        return _Select(select_columns=args, dialect=self._dialect)

    def with_(self, *args: tuple[str, SelectProtocol]) -> SelectProtocol:
        return _Select(with_queries=args, dialect=self._dialect)

    def update(self) -> UpdateProtocol:
        return _Update(dialect=self._dialect)

    def insert(self) -> InsertProtocol:
        return _Insert(dialect=self._dialect)

    def delete(self) -> DeleteProtocol:
        return _Delete(dialect=self._dialect)

    def create_table_as(self, query: SelectProtocol, table: str, db: str = '') -> CreateTableProtocol:
        return _CreateTable(dialect=self._dialect, query=query, table=FullTableName(table, db))
