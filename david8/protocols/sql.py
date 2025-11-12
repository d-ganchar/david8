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


class SqlPredicateProtocol(SqlExpressionProtocol):
    pass


class SqlFunctionProtocol(SqlExpressionProtocol):
    pass


class AsExpressionProtocol(SqlExpressionProtocol):
    def as_(self, value: str | int | float | SqlExpressionProtocol | SqlPredicateProtocol, alias: str):
        pass


class SqlLogicalOperatorProtocol(SqlExpressionProtocol):
    pass
