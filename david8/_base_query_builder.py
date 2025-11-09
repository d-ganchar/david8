from dataclasses import dataclass

from .core.base_select import BaseSelect
from .core.columns import WhereCondition
from .protocols.dml import SelectProtocol
from .protocols.query_builder import QueryBuilderProtocol
from .protocols.sql_statement import ColumnProtocol


@dataclass(slots=True)
class BaseQueryBuilder(QueryBuilderProtocol):
    def select(self, *args) -> SelectProtocol:
        return BaseSelect(_select=args)

    def cond(self) -> type[ColumnProtocol]:
        return WhereCondition
