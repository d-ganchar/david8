from typing import Protocol, Self

from ..protocols.dialect import DialectProtocol


class QueryProtocol(Protocol):
    """
    Full SQL query
    """
    def get_sql(self, dialect: DialectProtocol = None) -> str:
        pass

    def get_parameters(self) -> list | dict:
        pass


class ExprProtocol:
    """
    Common SQL expression
    """
    def get_sql(self, dialect: DialectProtocol) -> str:
        pass


class AliasedProtocol(ExprProtocol):
    def as_(self, alias: str) -> Self:
        pass


class PredicateProtocol(AliasedProtocol):
    pass


class FunctionProtocol(AliasedProtocol):
    pass


class LogicalOperatorProtocol(ExprProtocol):
    pass
