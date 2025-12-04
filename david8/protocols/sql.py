from typing import Any, Protocol

from ..protocols.dialect import DialectProtocol


class QueryProtocol(Protocol):
    """
    Full SQL query
    """
    def get_sql(self, dialect: DialectProtocol = None) -> str:
        pass

    def get_parameters(self) -> dict:
        pass

    def get_list_parameters(self) -> list[Any]:
        pass

    def get_tuple_parameters(self) -> tuple[Any]:
        pass


class ExprProtocol:
    """
    Common SQL expression
    """
    def get_sql(self, dialect: DialectProtocol) -> str:
        pass


class AliasedProtocol(ExprProtocol):
    def as_(self, alias: str) -> 'AliasedProtocol':
        pass


class ParameterProtocol(AliasedProtocol):
    pass


class ValueProtocol(AliasedProtocol):
    pass


class PredicateProtocol(AliasedProtocol):
    pass


class FunctionProtocol(AliasedProtocol):
    pass


class LogicalOperatorProtocol(ExprProtocol):
    pass
