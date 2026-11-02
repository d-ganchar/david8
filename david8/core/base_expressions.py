from dataclasses import dataclass, field

from ..protocols.dialect import DialectProtocol
from ..protocols.sql import DescProtocol, ExprProtocol
from .arg_convertors import to_col_or_expr
from .base_aliased import BaseAliased


@dataclass(slots=True)
class FullTableName(BaseAliased):
    table: str = ''
    db: str = ''

    def set_names(self, table: str, db: str = '') -> None:
        self.table = table
        self.db = db

    def _get_sql(self, dialect: DialectProtocol) -> str:
        if self.db:
            return f'{dialect.quote_ident(self.db)}.{dialect.quote_ident(self.table)}'

        if not self.table:
            return ''

        return dialect.quote_ident(self.table)


@dataclass(slots=True)
class BaseDesc(DescProtocol):
    items: tuple[str | int, ...] = field(default_factory=tuple)

    def get_sql(self, dialect: DialectProtocol) -> str:
        items = ()
        for item in self.items:
            items += (f'{dialect.quote_ident(item) if isinstance(item, str) else item} DESC',)

        return ', '.join(items)


@dataclass(slots=True)
class BaseDistinct(ExprProtocol):
    _items: tuple[str | ExprProtocol, ...] = field(default_factory=tuple)
    _on_items: tuple[str | ExprProtocol, ...] = field(default_factory=tuple)

    def get_sql(self, dialect: DialectProtocol) -> str:
        on = ''
        if self._on_items:
            on = f' ON ({", ".join(to_col_or_expr(i, dialect) for i in self._on_items)})'

        field = f' {", ".join(to_col_or_expr(i, dialect) for i in self._items)}'
        return f'DISTINCT{on}{field}'
