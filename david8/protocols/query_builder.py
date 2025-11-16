from typing import Protocol

from ..protocols.dml import SelectProtocol
from .sql import AsExprProtocol, FunctionProtocol


class QueryBuilderProtocol(Protocol):
    def select(self, *args: str | AsExprProtocol | FunctionProtocol) -> SelectProtocol:
        pass

    def with_(self, *args: tuple[str, SelectProtocol]) -> SelectProtocol:
        pass
