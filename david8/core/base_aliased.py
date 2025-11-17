import dataclasses
from typing import Self

from .. import DialectProtocol
from ..protocols.sql import AliasedProtocol


@dataclasses.dataclass(slots=True)
class BaseAliased(AliasedProtocol):
    def __init__(self, _as: str = '') -> None:
        self._as = _as

    def as_(self, alias: str) -> Self:
        self._as = alias
        return self

    def _get_sql(self, dialect: DialectProtocol) -> str:
        raise NotImplementedError()

    def get_sql(self, dialect: DialectProtocol) -> str:
        sql = self._get_sql(dialect)
        if self._as:
            return f'{sql} AS {dialect.quote_ident(self._as)}'

        return sql
