from typing import Protocol

from ..protocols.sql import DeleteProtocol, InsertProtocol, SelectProtocol, UpdateProtocol
from .sql import AliasedProtocol, CreateTableProtocol, ExprProtocol, FunctionProtocol


class QueryBuilderProtocol(Protocol):
    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol:
        pass

    def with_(self, *args: tuple[str, SelectProtocol]) -> SelectProtocol:
        pass

    def update(self) -> UpdateProtocol:
        pass

    def insert(self) -> InsertProtocol:
        pass

    def delete(self) -> DeleteProtocol:
        pass

    def create_table_as(self, query: SelectProtocol, table: str, db: str = '') -> CreateTableProtocol:
        pass
