from dataclasses import dataclass

from ._dml.base_select import BaseSelect
from ._protocols.dml import SelectProtocol
from ._protocols.query_builder import QueryBuilderProtocol


@dataclass(slots=True)
class BaseQueryBuilder(QueryBuilderProtocol):
    def select(self, *args) -> SelectProtocol:
        return BaseSelect(_select_fields=args)
