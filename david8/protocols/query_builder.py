from typing import Protocol

from ..protocols.dml import DeleteProtocol, InsertProtocol, SelectProtocol, UpdateProtocol
from .sql import AliasedProtocol, ExprProtocol, FunctionProtocol


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
