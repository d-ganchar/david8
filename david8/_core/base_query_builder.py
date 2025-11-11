from dataclasses import dataclass

from ..protocols.dialect import DialectProtocol
from ..protocols.dml import SelectProtocol
from ..protocols.query_builder import QueryBuilderProtocol
from ..protocols.sql import AsExpressionProtocol
from .base_dml import BaseSelect


@dataclass(slots=True)
class BaseQueryBuilder(QueryBuilderProtocol):
    def __init__(self, dialect: DialectProtocol):
        self._dialect = dialect

    def select(self, *args: str | AsExpressionProtocol) -> SelectProtocol:
        return BaseSelect(select=args, dialect=self._dialect)

    def with_(self, *args: tuple[str, SelectProtocol]) -> SelectProtocol:  # type: ignore[override]
        return BaseSelect(select=(), with_queries=args, dialect=self._dialect)
