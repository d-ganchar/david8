from copy import deepcopy
from dataclasses import dataclass

from .protocols.dialect import DialectProtocol
from .core.base_select import BaseSelect
from .protocols.dml import SelectProtocol
from .protocols.query_builder import QueryBuilderProtocol


@dataclass(slots=True)
class BaseQueryBuilder(QueryBuilderProtocol):
    _dialect: DialectProtocol

    def select(self, *args) -> SelectProtocol:
        # copy dialect to collect query parameters from zero
        return BaseSelect(_select=args, _dialect=deepcopy(self._dialect))
