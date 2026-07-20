from dataclasses import dataclass

from ..protocols.dialect import DialectProtocol
from ..protocols.query_builder import QueryBuilderProtocol
from ..protocols.sql import (
    AliasedProtocol,
    CreateTableProtocol,
    DeleteProtocol,
    DropProtocol,
    ExprProtocol,
    FunctionProtocol,
    InsertProtocol,
    QueryProtocol,
    SelectProtocol,
    UpdateProtocol,
)
from .base_ddl import BaseCreateTable as _CreateTable
from .base_ddl import BaseDrop
from .base_dml import BaseDelete as _Delete
from .base_dml import BaseInsert as _Insert
from .base_dml import BaseUpdate as _Update
from .base_dql import BaseSelect as _Select
from .base_expressions import FullTableName
from .base_query import BaseQuery


@dataclass()
class ExprQuery(BaseQuery):
    _expr: ExprProtocol

    def _get_sql(self, dialect: DialectProtocol) -> str:
        return self._expr.get_sql(dialect)


@dataclass(slots=True)
class BaseQueryBuilder(QueryBuilderProtocol):
    def __init__(self, dialect: DialectProtocol):
        self._dialect = dialect

    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol:
        return _Select(select_columns=args, dialect=self._dialect)

    def with_(self, *args: tuple[str, SelectProtocol], recursive: bool = False) -> SelectProtocol:
        return _Select(with_queries=args, dialect=self._dialect, with_recursive=recursive)

    def update(self) -> UpdateProtocol:
        return _Update(dialect=self._dialect)

    def insert(self) -> InsertProtocol:
        return _Insert(dialect=self._dialect)

    def delete(self) -> DeleteProtocol:
        return _Delete(dialect=self._dialect)

    def create_table_as(self, query: SelectProtocol, table: str, db: str = '') -> CreateTableProtocol:
        return _CreateTable(dialect=self._dialect, query=query, table=FullTableName(table, db))

    def drop(self) -> DropProtocol:
        return BaseDrop(dialect=self._dialect)

    def query(self, expr: ExprProtocol) -> QueryProtocol:
        return ExprQuery(_expr=expr, dialect=self._dialect)
