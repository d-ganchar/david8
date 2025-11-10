from typing import Protocol

from ..protocols.dml import SelectProtocol


class QueryBuilderProtocol(Protocol):
    def select(self, *args) -> SelectProtocol:
        pass
