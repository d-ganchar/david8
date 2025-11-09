from typing import Protocol

from ..protocols.dml import SelectProtocol
from .sql_statement import ColumnProtocol


class QueryBuilderProtocol(Protocol):
    def select(self, *args) -> SelectProtocol:
        pass

    def cond(self) -> type[ColumnProtocol]:
        """
        Where condition builder
        """
