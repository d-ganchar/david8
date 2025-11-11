from typing import Protocol

from ..protocols.dialect import DialectProtocol


class QueryProtocol(Protocol):
    def get_sql(self) -> str:
        pass

    def get_parameters(self) -> list | dict:
        pass


class SqlExpressionProtocol:
    def get_sql(self, dialect: DialectProtocol) -> str:
        pass


class AsExpressionProtocol(SqlExpressionProtocol):
    def as_(self, value: str | SqlExpressionProtocol, alias: str):
        pass


class LogicalOperatorProtocol(SqlExpressionProtocol):
    pass
