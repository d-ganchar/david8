import dataclasses
from typing import Self

from ..protocols.dialect import DialectProtocol
from ..protocols.sql import JoinProtocol, LogicalOperatorProtocol, PredicateProtocol, SelectProtocol, Sql92JoinProtocol


@dataclasses.dataclass(slots=True)
class Sql92Join(Sql92JoinProtocol):
    alias: str = ''
    join_type: str = ''
    on_expr: tuple[LogicalOperatorProtocol | PredicateProtocol, ...] = dataclasses.field(default_factory=tuple)
    using_expr: tuple[str, ...] = dataclasses.field(default_factory=tuple)
    from_table: tuple[str, str] = dataclasses.field(default_factory=tuple)  # ('table', 'db',)
    from_query: SelectProtocol = None

    def as_(self, alias: str) -> Self:
        self.alias = alias
        return self

    def get_sql(self, dialect: DialectProtocol) -> str:
        if self.from_query:
            source = f'({self.from_query.get_sql(dialect)})'
        else:
            table, db = self.from_table
            source = dialect.quote_ident(table)

        alias = f' AS {dialect.quote_ident(self.alias)}' if self.alias else ''
        if self.using_expr:
            using = ', '.join([dialect.quote_ident(u) for u in self.using_expr])
            return f'{self.join_type} {source}{alias} USING ({using})'

        on = f"{' AND '.join(on.get_sql(dialect) for on in self.on_expr)}"
        return f'{self.join_type} {source}{alias} ON ({on})'

    def on(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'JoinProtocol':
        self.on_expr += args
        self.using_expr = ()
        return self

    def table(self, name: str, db: str = '') -> 'JoinProtocol':
        self.from_table = (name, db, )
        return self

    def query(self, query: SelectProtocol) -> 'JoinProtocol':
        self.from_query = query
        return self

    def using(self, *args: str) -> 'JoinProtocol':
        self.using_expr = args
        self.on_expr = ()
        return self
