
from ..protocols.sql import LogicalOperatorProtocol, QueryProtocol, SqlExpressionProtocol


class SelectProtocol(QueryProtocol):
    def select(self, *args: str) -> 'SelectProtocol':
        pass

    def where(self, *args: LogicalOperatorProtocol | SqlExpressionProtocol | ...) -> 'SelectProtocol':
        pass

    def from_table(self, table_name: str) -> 'SelectProtocol':
        pass

    def group_by(self, *args) -> 'SelectProtocol':
        pass

    def limit(self, value: int) -> 'SelectProtocol':
        pass

    def get_parameters(self) -> list | dict:
        pass
