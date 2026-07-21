from typing import Protocol

from .sql import (
    AliasedProtocol,
    CreateTableProtocol,
    CreateViewProtocol,
    DeleteProtocol,
    DropProtocol,
    ExprProtocol,
    FunctionProtocol,
    InsertProtocol,
    QueryProtocol,
    SelectProtocol,
    UpdateProtocol,
)


class QueryBuilderProtocol(Protocol):
    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol: ...

    def with_(self, *args: tuple[str, SelectProtocol], recursive: bool = False) -> SelectProtocol: ...

    def update(self) -> UpdateProtocol: ...

    def insert(self) -> InsertProtocol: ...

    def delete(self) -> DeleteProtocol: ...

    def create_table_as(self, query: SelectProtocol, table: str, db: str = '') -> CreateTableProtocol: ...

    def create_view(
        self,
        query: SelectProtocol,
        view: str,
        db: str = '',
        or_replace: bool = False,
        if_not_exists: bool = False
    ) -> CreateViewProtocol: ...

    def drop(self) -> DropProtocol: ...

    def query(self, expr: ExprProtocol) -> QueryProtocol: ...
