from typing import Any, Protocol, Union

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

    def get_dialect(self) -> DialectProtocol:
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


class JoinProtocol(AliasedProtocol):
    pass


class SelectProtocol(QueryProtocol):
    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> 'SelectProtocol':
        pass

    def where(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'SelectProtocol':
        pass

    def from_table(self, table_name: str, alias: str = '', db_name: str = '') -> 'SelectProtocol':
        pass

    def from_expr(self, expr: Union['SelectProtocol', FunctionProtocol], alias: str = '') -> 'SelectProtocol':
        pass

    def group_by(self, *args: str | int) -> 'SelectProtocol':
        pass

    def limit(self, value: int) -> 'SelectProtocol':
        pass

    def order_by(self, *args: str | int) -> 'SelectProtocol':
        pass

    def order_by_desc(self, *args: str | int) -> 'SelectProtocol':
        pass

    def union(self, *args: 'SelectProtocol', all_flag: bool = True) -> 'SelectProtocol':
        pass

    def having(self, *args: PredicateProtocol) -> 'SelectProtocol':
        pass

    def join(self, join: JoinProtocol) -> 'SelectProtocol':
        pass


class Sql92JoinProtocol(JoinProtocol):
    def on(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'Sql92JoinProtocol':
        pass

    def table(self, name: str, db: str = '') -> 'Sql92JoinProtocol':
        pass

    def query(self, query: SelectProtocol) -> 'Sql92JoinProtocol':
        pass

    def using(self, *args: str) -> 'Sql92JoinProtocol':
        pass


class UpdateProtocol(QueryProtocol):
    def table(self, table_name: str, alias: str = '', db_name: str = '') -> 'UpdateProtocol':
        pass

    def set_(self, column: str, value: str | int | float | ExprProtocol | SelectProtocol) -> 'UpdateProtocol':
        pass

    def where(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'UpdateProtocol':
        pass


class InsertProtocol(QueryProtocol):
    def into(self, table_name: str, db_name: str = '') -> 'InsertProtocol':
        pass

    def value(self, col_name: str, value: str | float | int) -> 'InsertProtocol':
        pass

    def columns(self, *args: str) -> 'InsertProtocol':
        pass

    def from_select(self, query: SelectProtocol) -> 'InsertProtocol':
        pass


class DeleteProtocol(QueryProtocol):
    def from_table(self, table_name: str, db_name: str = '') -> 'DeleteProtocol':
        pass

    def where(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'DeleteProtocol':
        pass


class CreateTableProtocol(QueryProtocol):
    def as_(self, query: SelectProtocol, table: str, db: str = '') -> 'CreateTableProtocol':
        pass
