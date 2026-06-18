import dataclasses

from ..protocols.dialect import DialectProtocol
from ..protocols.sql import DescProtocol, ExprProtocol


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


@dataclasses.dataclass(slots=True)
class BaseDesc(DescProtocol):
    items: tuple[str | int, ...] = dataclasses.field(default_factory=tuple)

    def get_sql(self, dialect: DialectProtocol) -> str:
        items = ()
        for item in self.items:
            items += (f'{dialect.quote_ident(item) if isinstance(item, str) else item} DESC',)

        return ', '.join(items)
