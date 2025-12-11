import dataclasses

from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import ExprProtocol


@dataclasses.dataclass(slots=True)
class FullTableName(ExprProtocol):
    table: str = ''
    db: str = ''

    @property
    def from_db(self):
        # TODO: breaking changes. remove when major release
        return self.db

    @from_db.setter
    def from_db(self, value: str = ''):
        # TODO: breaking changes. remove when major release
        self.db = value

    @property
    def from_table(self):
        # TODO: breaking changes. remove when major release
        return self.table

    @from_table.setter
    def from_table(self, value: str = ''):
        # TODO: breaking changes. remove when major release
        self.table = value

    def set_names(self, table: str, db: str = '') -> None:
        self.table = table
        self.db = db

    def set_source(self, table: str, db: str = '') -> None:
        # TODO: breaking changes. remove when major release
        self.set_names(table, db)

    def get_sql(self, dialect: DialectProtocol) -> str:
        if self.db:
            return f'{dialect.quote_ident(self.db)}.{dialect.quote_ident(self.table)}'

        if not self.table:
            return ''

        return dialect.quote_ident(self.table)


@dataclasses.dataclass(slots=True)
class BaseExpression(ExprProtocol):
    def _render_prefix(self, dialect: DialectProtocol) -> str:
        return ''

    def _render_postfix(self, dialect: DialectProtocol) -> str:
        return ''

    def _render_main_expr(self, dialect: DialectProtocol) -> str:
        return ''

    def _get_sql(self, dialect: DialectProtocol) -> str:
        return f'{self._render_prefix(dialect)}{self._render_main_expr(dialect)}{self._render_postfix(dialect)}'

    def get_sql(self, dialect: DialectProtocol) -> str:
        return self._get_sql(dialect)
