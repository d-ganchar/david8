from copy import deepcopy
from dataclasses import dataclass

from .core.base_select import BaseSelect
from .protocols.dialect import DialectProtocol
from .protocols.dml import SelectProtocol
from .protocols.query_builder import QueryBuilderProtocol
from .protocols.sql import AsExpressionProtocol


@dataclass(slots=True)
class BaseQueryBuilder(QueryBuilderProtocol):
    _dialect: DialectProtocol

    def select(self, *args: str | AsExpressionProtocol) -> SelectProtocol:
        # copy dialect to collect query parameters from zero
        return BaseSelect(_select=args, _dialect=deepcopy(self._dialect))
