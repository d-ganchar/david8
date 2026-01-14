import dataclasses

from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import ExprProtocol


@dataclasses.dataclass(slots=True)
class FullTableName(ExprProtocol):
    table: str = ''
    db: str = ''

    def set_names(self, table: str, db: str = '') -> None:
        self.table = table
        self.db = db

    def get_sql(self, dialect: DialectProtocol) -> str:
        if self.db:
            return f'{dialect.quote_ident(self.db)}.{dialect.quote_ident(self.table)}'

        if not self.table:
            return ''

        return dialect.quote_ident(self.table)
