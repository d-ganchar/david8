from dataclasses import dataclass

from ..protocols.dialect import DialectProtocol
from ..protocols.dml import SelectProtocol
from ..protocols.query_builder import QueryBuilderProtocol
from ..protocols.sql import AliasedProtocol, ExprProtocol, FunctionProtocol
from .base_dml import BaseSelect as _BaseSelect


@dataclass(slots=True)
class BaseQueryBuilder(QueryBuilderProtocol):
    def __init__(self, dialect: DialectProtocol):
        self._dialect = dialect

    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol:
        return _BaseSelect(select=args, dialect=self._dialect)

    def with_(self, *args: tuple[str, SelectProtocol]) -> SelectProtocol:
        return _BaseSelect(with_queries=args, dialect=self._dialect)
