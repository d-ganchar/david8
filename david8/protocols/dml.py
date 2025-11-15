from ..protocols.sql import AsExpressionProtocol, QueryProtocol, SqlLogicalOperatorProtocol, SqlPredicateProtocol


class SelectProtocol(QueryProtocol):
    def select(self, *args: str | AsExpressionProtocol) -> 'SelectProtocol':
        pass

    def where(self, *args: SqlLogicalOperatorProtocol | SqlPredicateProtocol) -> 'SelectProtocol':
        pass

    def from_table(self, table_name: str, db_name: str = '') -> 'SelectProtocol':
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

    def having(self, *args: SqlPredicateProtocol) -> 'SelectProtocol':
        pass
