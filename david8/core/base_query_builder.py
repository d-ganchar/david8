from dataclasses import dataclass

from ..protocols.dialect import DialectProtocol
from ..protocols.dml import DeleteProtocol, InsertProtocol, SelectProtocol, UpdateProtocol
from ..protocols.query_builder import QueryBuilderProtocol
from ..protocols.sql import AliasedProtocol, ExprProtocol, FunctionProtocol
from .base_dml import BaseDelete as _BaseDelete
from .base_dml import BaseInsert as _BaseInsert
from .base_dml import BaseSelect as _BaseSelect
from .base_dml import BaseUpdate as _BaseUpdate


@dataclass(slots=True)
class BaseQueryBuilder(QueryBuilderProtocol):
    def __init__(self, dialect: DialectProtocol):
        self._dialect = dialect

    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol:
        return _BaseSelect(select_columns=args, dialect=self._dialect)

    def with_(self, *args: tuple[str, SelectProtocol]) -> SelectProtocol:
        return _BaseSelect(with_queries=args, dialect=self._dialect)

    def update(self) -> UpdateProtocol:
        return _BaseUpdate(dialect=self._dialect)

    def insert(self) -> InsertProtocol:
        return _BaseInsert(dialect=self._dialect)

    def delete(self) -> DeleteProtocol:
        return _BaseDelete(dialect=self._dialect)
