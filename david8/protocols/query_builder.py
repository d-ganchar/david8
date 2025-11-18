from typing import Protocol

from ..protocols.dml import SelectProtocol
from .sql import AliasedProtocol, ExprProtocol, FunctionProtocol


class QueryBuilderProtocol(Protocol):
    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol:
        pass

    def with_(self, *args: tuple[str, SelectProtocol]) -> SelectProtocol:
        pass
