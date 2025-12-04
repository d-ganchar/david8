from ..protocols.sql import AliasedProtocol, LogicalOperatorProtocol, PredicateProtocol, QueryProtocol
from .sql import ExprProtocol, FunctionProtocol


class JoinProtocol(AliasedProtocol):
    pass


class SelectProtocol(QueryProtocol):
    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> 'SelectProtocol':
        pass

    def where(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'SelectProtocol':
        pass

    def from_table(self, table_name: str, alias: str = '', db_name: str = '') -> 'SelectProtocol':
        pass

    def from_query(self, query: 'SelectProtocol') -> 'SelectProtocol':
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
