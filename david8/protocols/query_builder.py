from typing import Protocol

from ..protocols.dml import SelectProtocol
from .sql import AsExpressionProtocol


class QueryBuilderProtocol(Protocol):
    def select(self, *args: str | AsExpressionProtocol) -> SelectProtocol:
        pass

    def with_(self, *args: tuple[str, SelectProtocol]) -> SelectProtocol:
        pass
