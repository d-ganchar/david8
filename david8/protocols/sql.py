from typing import Protocol

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


class PredicateProtocol(ExprProtocol):
    pass


class FunctionProtocol(ExprProtocol):
    pass


class AsExprProtocol(ExprProtocol):
    # TODO: ?
    # class AliasedProtocol(ExpressionProtocol):
    #     def as_(self, alias: str) -> ExpressionProtocol:
    #         pass
    def as_(self, value: str | int | float | ExprProtocol | PredicateProtocol, alias: str):
        pass


class LogicalOperatorProtocol(ExprProtocol):
    pass
