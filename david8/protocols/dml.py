from ..protocols.sql_statement import SqlStatementProtocol, PredicateProtocol


class SelectProtocol(SqlStatementProtocol):
    def select(self, *args) -> 'SelectProtocol':
        pass

    def where(self, *args) -> PredicateProtocol:
        pass

    def from_table(self, table_name: str) -> 'SelectProtocol':
        pass

    def group_by(self, *args) -> 'SelectProtocol':
        pass

    def limit(self, value: int) -> 'SelectProtocol':
        pass
