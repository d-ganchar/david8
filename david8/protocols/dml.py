from ..protocols.sql import AsExprProtocol, LogicalOperatorProtocol, PredicateProtocol, QueryProtocol
from .sql import ExprProtocol


class JoinProtocol(ExprProtocol):
    def on(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'JoinProtocol':
        pass

    def table(self, name: str, db: str = '') -> 'JoinProtocol':
        pass

    def query(self, query: 'SelectProtocol') -> 'JoinProtocol':
        return self

    def as_(self, alias: str) -> 'JoinProtocol':
        return self


class SelectProtocol(QueryProtocol):
    def select(self, *args: str | AsExprProtocol) -> 'SelectProtocol':
        pass

    def where(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'SelectProtocol':
        pass

    def from_table(self, table_name: str, alias: str = '', db_name: str = '') -> 'SelectProtocol':
        pass

    def from_query(self, query: 'SelectProtocol', alias: str = '') -> 'SelectProtocol':
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
