from typing import Protocol

from david8.protocols.dialect import DialectProtocol


class QueryProtocol(Protocol):
    def get_sql(self) -> str:
        pass


class SqlExpressionProtocol:
    def get_sql(self, dialect: DialectProtocol) -> str:
        pass


class AsExpressionProtocol(SqlExpressionProtocol):
    def as_(self, value: str | SqlExpressionProtocol, alias: str):
        pass
