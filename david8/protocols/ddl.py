from ..protocols.dml import SelectProtocol
from ..protocols.sql import QueryProtocol


class CreateTableProtocol(QueryProtocol):
    def as_(self, query: SelectProtocol, table: str, db: str = '') -> 'CreateTableProtocol':
        pass
